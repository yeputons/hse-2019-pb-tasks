module Yat where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Data.List
import Data.Maybe
import Data.Bifunctor
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

addTabs :: String -> String
addTabs = intercalate "\n" . map ("\t"++) . lines


showExpr :: Expression -> String
showExpr (Number n)                        = show n
showExpr (Reference name)                  = name
showExpr (Assign name e)                   = "let " ++ name ++ " = " ++ showExpr e ++ " tel"
showExpr (BinaryOperation op l r)          = "(" ++ showExpr l ++ " " ++ showBinop op ++ " " ++ showExpr r ++ ")"
showExpr (UnaryOperation op e)             = showUnop op ++ showExpr e
showExpr (FunctionCall name args)          = name ++ "(" ++ concat (intersperse ", " (map showExpr args)) ++ ")"
showExpr (Conditional e t f)               = "if " ++ showExpr e ++ " then " ++ showExpr t ++ " else " ++ showExpr f ++ " fi"
showExpr (Block [])                        = "{\n}"
showExpr (Block exprs)                     = "{\n" ++ concat (intersperse ";\n" (map (addTabs . showExpr) exprs)) ++ "\n}"

showFunc :: FunctionDefinition -> String
showFunc (name, args, expr) = "func " ++ name ++ "(" ++ concat (intersperse ", " args) ++ ") = " ++ showExpr expr

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (funcs, body) = concatMap ((++ "\n") . showFunc) funcs ++ showExpr body

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

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL = undefined

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression = undefined
-} -- Удалите эту строчку, если решаете бонусное задание.

-- Реализуйте eval: запускает программу и возвращает её значение.

getVar :: State -> Name -> Integer
getVar [] _                                           = 0
getVar ((var_name, value):xs) name | name == var_name = value
                                   | otherwise        = getVar xs name 

getFunc :: [FunctionDefinition] -> Name -> ([Name], Expression)
getFunc funcs name = res (head (filter (equal name) funcs)) 
                        where res   (n, name, expr)       = (name, expr)
                              equal name (n, names, expr) = name == n
                              

getFuncScope :: State -> [Name] -> [Integer] -> State
getFuncScope scope name value = zip name value ++ scope

chainFunc :: [Expression] -> State -> [FunctionDefinition] -> ([Integer], State)
chainFunc []           scope  funcs = ([], scope)
chainFunc (expr:exprs) scope  funcs = (fst value:fst values, snd values)
                                    where value  = evalExpr  expr   scope         funcs
                                          values = chainFunc exprs  (snd value)   funcs

evalExpr :: Expression -> State -> [FunctionDefinition] -> (Integer, State)
evalExpr (Number n) scope funcs                       = (n, scope)
evalExpr (Reference name) scope funcs                 = (getVar scope name, scope)
evalExpr (Assign name expr) scope funcs               = (fst value, (name, fst value):snd value) 
                                                        where value = evalExpr expr scope funcs
evalExpr (BinaryOperation op l r) scope funcs = (toBinaryFunction op (fst lvalue) (fst rvalue), snd rvalue)
                                                             where lvalue = evalExpr l scope        funcs
                                                                   rvalue = evalExpr r (snd lvalue) funcs 
evalExpr (UnaryOperation op expr) scope funcs         = (toUnaryFunction op (fst value), snd value)
                                                             where value = evalExpr expr scope funcs
evalExpr (FunctionCall name exprs) scope funcs = (fst value, snd res) 
                                               where func  = getFunc   funcs      name
                                                     res   = chainFunc exprs      scope         funcs 
                                                     value = evalExpr  (snd func) (getFuncScope (snd res) (fst func) (fst res)) funcs 

evalExpr (Conditional e t f) scope funcs | toBool(fst res) = evalExpr t (snd res) funcs
                                         | otherwise       = evalExpr f (snd res) funcs
                                                            where res = evalExpr e scope funcs


evalExpr (Block [])           scope   _                    = (0, scope)
evalExpr (Block [expr])       scope   funcs                = evalExpr expr          scope funcs
evalExpr (Block (expr:exprs)) scope   funcs                = evalExpr (Block exprs) res   funcs 
                                                              where res = snd (evalExpr expr scope funcs)
eval :: Program -> Integer
eval (funcs, expr) = fst (evalExpr expr [] funcs)