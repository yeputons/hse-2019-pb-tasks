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

(/+) = BinaryOperation Add
(/*) = BinaryOperation Mul
(/-) = BinaryOperation Sub
(|||) = BinaryOperation Or
(===) = BinaryOperation Eq
iff = Conditional
(=:=) = Assign
c = Number
r = Reference
call = FunctionCall

infixl 6 /+
infixl 6 /-
infixl 7 /*
infixr 2 |||
infix 4 ===
infixr 1 =:=

showList' :: [a] -> String -> (a -> String) -> String
showList' [] _ _ = ""
showList' [x] _ sh = sh x
showList' (x:xs) next sh = sh x ++ next ++ (showList' xs next sh)

showExpression :: Expression -> String
showExpression (Number a) = show a
showExpression (Reference a) = a
showExpression (Assign var a) = "let " ++ var ++ " = " ++ showExpression a ++ " tel"
showExpression (BinaryOperation op a b) = "(" ++ showExpression a ++ " " ++ showBinop op ++ " " ++ showExpression b ++ ")"
showExpression (UnaryOperation uop a) = showUnop uop ++ showExpression a
showExpression (FunctionCall fun a) = fun ++ "(" ++ (showList' a ", " showExpression) ++ ")"
showExpression (Conditional cond a b) = "if " ++ showExpression cond ++ " then " ++ showExpression a ++ " else " ++ showExpression b ++ " fi"
showExpression (Block []) = "{\n}"
showExpression (Block a) = "{\n\t" ++ (showList' a ";\n\t" showExpression) ++ "\n}"

showFunction :: FunctionDefinition -> String
showFunction (fun, names, a) = "func " ++ fun ++ "(" ++ (showList' names ", " (\s -> s)) ++ ") = " ++ showExpression a

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram ([], body) = showExpression body
showProgram (funcs, body) = (showList' funcs "\n" showFunction) ++ "\n" ++ showExpression body

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
modifyScope :: State -> String -> Integer -> State
modifyScope scope var val = filter (\s -> var /= fst s) scope ++ zip (replicate 1 var) (replicate 1 val)

functionScope :: State -> State -> State
functionScope scope [] = scope
functionScope scope (x:xs) = functionScope (modifyScope scope (fst x) (snd x)) xs

getValue :: State -> String -> Integer
getValue scope var = case lookup var scope of
                                Just a -> a
                                _       -> 0

getResult :: Expression -> State -> [FunctionDefinition] -> Integer
getResult expr scope funcs = snd $ evalExpression scope funcs expr

getName :: FunctionDefinition -> Name
getName (name, _, _) = name

getArgs :: FunctionDefinition -> [Name]
getArgs (_, args, _) = args

getFunExpr :: FunctionDefinition -> Expression
getFunExpr (_, _, expr) = expr

evalList' :: State -> [FunctionDefinition] -> [Expression] -> [Integer]
evalList' _ _ [] = []
evalList' scope funcs (x:xs) = (replicate 1 (snd $ evalExpression scope funcs x)) ++ evalList' scope funcs xs

workBitch :: [FunctionDefinition] -> [FunctionDefinition] -> State -> Name -> [Expression] -> Integer
workBitch [] _ _ _ _ = undefined
workBitch (x:xs) funcs scope funcName oper | getName x == funcName = snd $ evalExpression (functionScope scope (zip (getArgs x) (evalList' scope funcs oper))) funcs (getFunExpr x)
                                           | otherwise = workBitch xs funcs scope funcName oper

evalExpression :: State -> [FunctionDefinition] -> Expression -> (State, Integer)
evalExpression scope _ (Number a) = (scope, a)
evalExpression scope _ (Reference a) = (scope, getValue scope a)
evalExpression scope funcs (Assign var val) = (modifyScope scope var (snd $ evalExpression scope funcs val), 0)
evalExpression scope funcs (BinaryOperation op a b) = (scope, toBinaryFunction op (getResult a scope funcs) (getResult b scope funcs))
evalExpression scope funcs (UnaryOperation uop a) = (scope, toUnaryFunction uop (getResult a scope funcs))
evalExpression scope funcs  (FunctionCall fun a) = (scope, workBitch funcs funcs scope fun a)
evalExpression scope funcs (Conditional cond a b) | (snd $ evalExpression scope funcs cond) == 0 = evalExpression scope funcs b
                                                  | otherwise = evalExpression scope funcs a
evalExpression scope _ (Block []) = (scope, 0)
evalExpression scope funcs (Block [x]) = (scope, snd $ evalExpression scope funcs x)
evalExpression scope funcs (Block (x:xs)) = evalExpression (fst $ evalExpression scope funcs x) funcs (Block xs)

eval :: Program -> Integer
eval prog = snd $ evalExpression [] (fst prog) (snd prog)
