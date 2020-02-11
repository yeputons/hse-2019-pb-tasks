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

showExpression :: Expression -> String
showExpression (Number num)                     = show num
showExpression (Reference name)                 = name
showExpression (Assign name expr)               = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op expr1 expr2) = concat ["(", showExpression expr1, " ", showBinop op, " ", showExpression expr2, ")"]
showExpression (UnaryOperation op expr)         = concat [showUnop op, showExpression expr]
showExpression (FunctionCall name exprs)        = concat [name, "(", intercalate ", " (map showExpression exprs), ")"]
showExpression (Conditional cond expr1 expr2)   = concat ["if ", showExpression cond, " then ", showExpression expr1, " else ", showExpression expr2, " fi"]
showExpression (Block exprs)                    = concat ["{\n", concatMap (("\t" ++) . (++ "\n")) (lines (intercalate ";\n" (map showExpression exprs))), "}"]

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expr, "\n"]

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (funcs, expr) = concat [concatMap showFunctionDefinition funcs, showExpression expr]

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

args' :: FunctionDefinition -> [Name]
args' (_, args, _) = args

expr' :: FunctionDefinition -> Expression
expr' (_, _, expr) = expr

count' :: [FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
count' _ state []               = ([] , state)
count' funcs state [expr]       = ([newNum], newState)
                                    where (newNum, newState)  = evalExpression funcs state expr
count' funcs state (expr:exprs) = (newNum : newNums, finalState)
                                    where
                                        (newNum, newState)    = evalExpression funcs state expr
                                        (newNums, finalState) = count' funcs newState exprs


evalExpression :: [FunctionDefinition] -> State -> Expression -> (Integer, State)

evalExpression _ state (Number num)                         = (num, state)

evalExpression _ state (Reference name)                     = (snd $ fromJust $ find (\(x, _) -> x == name) state, state)

evalExpression funcs state (Assign name expr)               = (newNum, (name, newNum) : newState)
                                                                where (newNum, newState)  = evalExpression funcs state expr

evalExpression funcs state (BinaryOperation op expr1 expr2) = (toBinaryFunction op num1 num2, secondState)
                                                                where (num1, firstState)  = evalExpression funcs state expr1
                                                                      (num2, secondState) = evalExpression funcs firstState expr2

evalExpression funcs state (UnaryOperation op expr)         = (toUnaryFunction op num, newState)
                                                                where (num, newState)     = evalExpression funcs state expr

evalExpression funcs state (FunctionCall name exprs)        = (newNum, newState)
                                                                where 
                                                                    params       = args' $ fromJust $ find (\(x, _, _) -> x == name) funcs
                                                                    count_params = count' funcs state exprs
                                                                    newNums      = fst count_params
                                                                    newState     = snd count_params
                                                                    (newNum, _)  = evalExpression funcs (zip params newNums ++ newState) (expr' $ fromJust $ find (\(x, _, _) -> x == name) funcs)

evalExpression funcs state (Conditional cond expr1 expr2)   | toBool num = evalExpression funcs newState expr1
                                                            | otherwise = evalExpression funcs newState expr2
                                                                where (num, newState) = evalExpression funcs state cond

evalExpression _ state (Block [])                           = (0, state)
evalExpression funcs state (Block [expr])                   = evalExpression funcs state expr
evalExpression funcs state (Block (expr:exprs))             = evalExpression funcs newState (Block exprs)
                                                                where (_, newState) = evalExpression funcs state expr

-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (funcs, expr) = fst $ evalExpression funcs [] expr