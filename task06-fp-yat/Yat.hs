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

insertSeparators :: [String] -> String -> [String]
insertSeparators []     sep = []
insertSeparators [x]    sep = [x]
insertSeparators (x:xs) sep = (x ++ sep) : insertSeparators xs sep

showExpr :: Expression -> String
showExpr (Number          n          ) = show n
showExpr (Reference       name       ) = name
showExpr (Assign          name expr  ) = "let " ++ name ++ " = " ++ showExpr expr ++ " tel"
showExpr (BinaryOperation op   l    r) = "(" ++ showExpr l ++ " " ++ showBinop op ++ " " ++ showExpr r ++ ")"
showExpr (UnaryOperation  op   expr  ) = showUnop op ++ showExpr expr
showExpr (FunctionCall    name args  ) = name ++ "(" ++ concat (insertSeparators (map showExpr args) ", ") ++ ")"
showExpr (Conditional     cond t    f) = "if " ++ showExpr cond ++ " then " ++ showExpr t ++ " else " ++ showExpr f ++ " fi"
showExpr (Block           []         ) = "{\n}"
showExpr (Block           exprs      ) = "{\n" ++ concatMap (("\t" ++) . (++ "\n")) (lines $ concat $ insertSeparators (map showExpr exprs) ";\n") ++ "}"

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, args, expr) = "func " ++ name ++ "(" ++ concat (insertSeparators args ", ") ++ ") = " ++ showExpr expr

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram ([], exprs) = showExpr exprs
showProgram (def:defs, exprs) = showFunctionDefinition def ++ "\n" ++ showProgram (defs, exprs)

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

getVar :: State -> Name -> Integer
getVar scope name = snd (head (filter ((==) name . fst) scope))

getName :: FunctionDefinition -> Name
getName (name, _, _) = name

getArgs :: FunctionDefinition -> [Name]
getArgs (_, args, _) = args

getExpr :: FunctionDefinition -> Expression
getExpr (_, _, expr) = expr

evalExpr :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpr funcs scope (Number          n           ) = (n, scope)
evalExpr funcs scope (Reference       name        ) = (getVar scope name, scope)

evalExpr funcs scope (Assign          name  expr  ) = (fst retVal, (name, fst retVal):snd retVal)
                                                      where retVal  = evalExpr funcs scope         expr

evalExpr funcs scope (BinaryOperation op    l    r) = (toBinaryFunction op (fst retVal1) (fst retVal2), snd retVal2)
                                                      where retVal1 = evalExpr funcs scope         l
                                                            retVal2 = evalExpr funcs (snd retVal1) r

evalExpr funcs scope (UnaryOperation  op    expr  ) = (toUnaryFunction  op (fst retVal), snd retVal)
                                                      where retVal  = evalExpr funcs         scope expr
 
evalExpr funcs scope (FunctionCall    name  args  ) = (fst (evalExpr funcs newScope (getExpr func)), newScope)
                                                      where newScope = zip (getArgs func) (map (fst . evalExpr funcs scope) args) ++ snd (evalExpr funcs scope (Block args))
                                                            func     = case find ((== name) . getName) funcs of 
                                                                       Just func' -> func'

evalExpr funcs scope (Conditional     cond  t    f) | toBool (fst retVal) = evalExpr funcs (snd retVal) t
                                                    | otherwise           = evalExpr funcs (snd retVal) f
                                                      where retVal        = evalExpr funcs scope        cond

evalExpr funcs scope (Block           []          ) = (0, scope)
evalExpr funcs scope (Block           [expr]      ) = evalExpr funcs scope expr
evalExpr funcs scope (Block           (e:es)      ) = evalExpr funcs (snd $ evalExpr funcs scope e) (Block es)

-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (definitions, expr) = fst (evalExpr definitions [] expr)
