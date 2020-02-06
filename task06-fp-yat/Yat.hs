module Yat where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Data.List
import Data.Maybe
import Data.Bifunctor
import Data.Tuple.Extra
import Debug.Trace

-- В логических операциях 0 считается ложью, всё остальное - истиной.
-- При этом все логические операции могут вернуть только 0 или 1.

-- Все возможные бинарные операции: сложение, умножение, вычитание, деление, взятие по модулю, <, <=, >, >=, ==, !=, логическое &&, логическое ||
data Binop = Add | Mul | Sub | Div | Mod | Lt | Le | Gt | Ge | Eq | Ne | And | Or

-- Все возможные унарные операции: смена знака числа и логическое "не".
data Unop = Neg | Not

data Expression = Number Integer  -- Возвращает число, побочных эффектов нет.
                | Reference Name  -- Возвращает значение соответствующей переменной в текущем scope, побочных эффектов нет.
                | Assign Name Expression  -- Вычисляет операнд, а потом изменяет значение соответствующей переменной и возвращает его. Если соответствующей переменной нет, она создаётся.
                | BinaryOperation Binop Expression Expression  -- Вычисляет сначала левый операнд, потом правый, потом возвращает результат операции. Других побочных эффектов нет.
                | UnaryOperation Unop Expression  -- Вычисляет операнд, потом применяет операцию и возвращает результат. Других побочных эффектов нет.
                | FunctionCall Name [Expression]  -- Вычисляет аргументы от первого к последнему в текущем scope, потом создаёт новый scope для дочерней функции (копию текущего с добавленными параметрами), возвращает результат работы функции.
                | Conditional Expression Expression Expression -- Вычисляет первый Expression, в случае истины вычисляет второй Expression, в случае лжи - третий. Возвращает соответствующее вычисленное значение.
                | Block [Expression] -- Вычисляет в текущем scope все выражения по очереди от первого к последнему, результат вычисления -- это результат вычисления последнего выражения или 0, если список пуст.

type Name = String
type FunctionDefinition = (Name, [Name], Expression)  -- Имя функции, имена параметров, тело функции
type State = [(String, Integer)]  -- Список пар (имя переменной, значение). Новые значения дописываются в начало, а не перезаписываютсpя
type Program = ([FunctionDefinition], Expression)  -- Все объявленные функций и основное тело программы

showBinop :: Binop -> String
showBinop Add = "+"
showBinop Mul = "*"
showBinop Sub = "-"
showBinop Div = "/"
showBinop Mod = "%"
showBinop Lt  = "<"
showBinop Le  = "<="
showBinop Gt  = ">"
showBinop Ge  = ">="
showBinop Eq  = "=="
showBinop Ne  = "/="
showBinop And = "&&"
showBinop Or  = "||"

showUnop :: Unop -> String
showUnop Neg = "-"
showUnop Not = "!"

showWordsList :: [String] -> String -> String
showWordsList []     _        = ""
showWordsList (w:ws) splitter = case length (w:ws) of
                                  0 -> ""
                                  1 -> w
                                  _ -> w ++ splitter ++ showWordsList ws splitter

showExpr :: Expression -> String-> String
showExpr (Number n)               lineBegin = show n
showExpr (Reference name)         lineBegin = name
showExpr (Assign name e)          lineBegin = "let " ++ name ++ " = " ++ showExpr e lineBegin ++ " tel"
showExpr (BinaryOperation op l r) lineBegin = "(" ++ showExpr l lineBegin ++ " "
                                                  ++ showBinop op ++ " " ++ showExpr r lineBegin ++ ")"
showExpr (UnaryOperation op e)    lineBegin = showUnop op ++ showExpr e lineBegin
showExpr (FunctionCall name args) lineBegin = name ++ "(" ++ showWordsList (map (\a -> showExpr a lineBegin) args) ", " ++ ")"
showExpr (Conditional e t f)      lineBegin = "if " ++ showExpr e lineBegin ++ " then " ++ showExpr t lineBegin ++ 
                                              " else " ++ showExpr f lineBegin ++ " fi"
showExpr (Block exprs)            lineBegin = "{" ++ "\n" ++ lineBegin ++ addInBegin "\t" ++
                                              showWordsList (map (\e -> showExpr e (lineBegin ++ "\t")) exprs) (";\n" ++ lineBegin ++ "\t") ++
                                              addInBegin ("\n" ++ lineBegin) ++ "}"
                                              where
                                                addInBegin str | null exprs = ""
                                                               | otherwise  = str

showFuncDef :: FunctionDefinition -> String
showFuncDef (funcName, argnames, block) = "func " ++ funcName ++ "(" ++ showWordsList argnames ", " ++ ") = " ++ showExpr block ""

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (funcs, body) = showWordsList (map showFuncDef funcs ++ [showExpr body ""]) "\n"

toBool :: Integer -> Bool
toBool = (/=) 0

fromBool :: Bool -> Integer
fromBool False = 0
fromBool True  = 1

toBinaryFunction :: Binop -> Integer -> Integer -> Integer
toBinaryFunction Add = (+)
toBinaryFunction Mul = (*)
toBinaryFunction Sub = (-)
toBinaryFunction Div = div
toBinaryFunction Mod = mod
toBinaryFunction Lt  = (.) fromBool . (<)
toBinaryFunction Le  = (.) fromBool . (<=)
toBinaryFunction Gt  = (.) fromBool . (>)
toBinaryFunction Ge  = (.) fromBool . (>=)
toBinaryFunction Eq  = (.) fromBool . (==)
toBinaryFunction Ne  = (.) fromBool . (/=)
toBinaryFunction And = \l r -> fromBool $ toBool l && toBool r
toBinaryFunction Or  = \l r -> fromBool $ toBool l || toBool r

toUnaryFunction :: Unop -> Integer -> Integer
toUnaryFunction Neg = negate
toUnaryFunction Not = fromBool . not . toBool

-- Если хотите дополнительных баллов, реализуйте
-- вспомогательные функции ниже и реализуйте evaluate через них.
-- По минимуму используйте pattern matching для `Eval`, функции
-- `runEval`, `readState`, `readDefs` и избегайте явной передачи состояния.

{- -- Удалите эту строчку, если решаете бонусное задание.
newtype Eval a = Eval ([FunctionDefinition] -> State -> (a, State))  -- Как data, только эффективнее в случае одного конструктора.

runEval :: Eval a -> [FunctionDefinition] -> State -> (a, State)
runEval (Eval f) = f

evaluated :: a -> Eval a  -- Возвращает значение без изменения состояния.
evaluated = undefined

readState :: Eval State  -- Возвращает состояние.
readState = undefined

addToState :: String -> Integer -> a -> Eval a  -- Добавляет/изменяет значение переменной на новое и возвращает константу.
addToState = undefined

readDefs :: Eval [FunctionDefinition]  -- Возвращает все определения функций.
readDefs = undefined

andThen :: Eval a -> (a -> Eval b) -> Eval b  -- Выполняет сначала первое вычисление, а потом второе.
andThen = undefined

andEvaluated :: Eval a -> (a -> b) -> Eval b  -- Выполняет вычисление, а потом преобразует результат чистой функцией.
andEvaluated = undefined

evalExprsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL = undefined

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression = undefined
-} -- Удалите эту строчку, если решаете бонусное задание.

-- Реализуйте eval: запускает программу и возвращает её значение.

changeInScope :: State -> String -> Integer -> State
changeInScope []    _    _ = []
changeInScope (s:scope) name n | name == fst s = (name, n):scope
                               | otherwise     = s:changeInScope scope name n

getFunc :: [FunctionDefinition] -> String -> FunctionDefinition
getFunc []        _    = undefined
getFunc (f:funcs) name | fst3 f == name = f
                       | otherwise      = getFunc funcs name

addToScope :: [String] -> [Expression] -> State -> [FunctionDefinition] -> State
addToScope _            []        scope _     = scope
addToScope []           _         scope _     = scope
addToScope (name:names) (e:exprs) scope funcs = case lookup name scope of
                                                  Just n -> addToScope names exprs (changeInScope (fst res) name (snd res)) funcs
                                                  _      -> (name, snd res):addToScope names exprs (fst res) funcs
                                                where
                                                  res = evalExpr e scope funcs

getSubscopeFromScope :: State -> State -> State
getSubscopeFromScope [] scope = []
getSubscopeFromScope (sb:sbscope) scope = case lookup (fst sb) scope of
                                            Just n -> (fst sb, n):getSubscopeFromScope sbscope scope
                                            _      -> undefined

evalExpr :: Expression -> State -> [FunctionDefinition] -> (State, Integer)
evalExpr (Number n)               scope funcs = (scope, n)
evalExpr (Reference name)         scope funcs = case lookup name scope of
                                                        Just n -> (scope, n)
                                                        _      -> undefined
evalExpr (Assign name e)          scope funcs = case lookup name scope of
                                                        Just n -> (changeInScope (fst res) name (snd res), snd res)
                                                        _      -> ((name, snd res):fst res, snd res)
                                                        where res = evalExpr e scope funcs
evalExpr (BinaryOperation op l r) scope funcs = (fst rRes, toBinaryFunction op (snd lRes) (snd rRes))
                                                where
                                                  lRes = evalExpr l scope funcs
                                                  rRes = evalExpr r (fst lRes) funcs
evalExpr (UnaryOperation op e)    scope funcs = (fst res, toUnaryFunction op (snd res))
                                                where res = evalExpr e scope funcs
evalExpr (FunctionCall name args) scope funcs = (fst newScope, snd res) 
                                                where
                                                  func = getFunc funcs name
                                                  newScope = evalExpr (Block args) scope funcs
                                                  funcScope = addToScope (snd3 func) args scope funcs 
                                                  res = evalExpr (thd3 func) funcScope funcs
evalExpr (Conditional e t f)      scope funcs | toBool(snd res) = evalExpr t (fst res) funcs
                                              | otherwise       = evalExpr f (fst res) funcs
                                                where res = evalExpr e scope funcs
evalExpr (Block [])               scope _     = (scope, 0)
evalExpr (Block (e:exprs))        scope funcs = case length (e:exprs) of
                                                  1 -> evalExpr e scope funcs
                                                  _ -> evalExpr (Block exprs) (fst fstRes) funcs
                                                  where fstRes = evalExpr e scope funcs

eval :: Program -> Integer
eval (funcs, expr) = snd (evalExpr expr [] funcs)
