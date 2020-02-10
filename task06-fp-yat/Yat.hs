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
showExpression (Number num)                           = show num
showExpression (Reference name)                       = name
showExpression (Assign name expr)                     = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation binop expr1 expr2)    = concat ["(", showExpression expr1, " ", showBinop binop, " ", showExpression expr2, ")"]
showExpression (UnaryOperation unop expr)             = showUnop unop ++ showExpression expr
showExpression (FunctionCall name args)               = concat [name, "(", intercalate ", " (map showExpression args), ")"]
showExpression (Conditional cond ifCond ifNotCond)    = concat ["if ", showExpression cond, " then ", showExpression ifCond, " else ", showExpression ifNotCond, " fi"]
showExpression (Block exprs)                          = concat ["{\n", concatMap (("\t" ++) . (++ "\n")) (lines $ intercalate ";\n" (map showExpression exprs)), "}"]

showFunction :: FunctionDefinition -> String
showFunction (name, params, expr) = concat ["func ", name, "(", intercalate ", " params, ") = ", showExpression expr, "\n"]

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (functions, expr) = concatMap showFunction functions ++ showExpression expr

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

fst3 :: FunctionDefinition -> Name
fst3 (name, _, _) = name

snd3 :: FunctionDefinition -> [Name]
snd3 (_, args, _) = args

trd3 :: FunctionDefinition -> Expression
trd3 (_, _, expr) = expr

getArgsValues :: State -> [FunctionDefinition] -> [Expression] -> (State, [Integer])
getArgsValues state funcs []        = (state, [])
getArgsValues state funcs [expr]    = (newState, [newVal])
                                        where (newState, newVal) = evalExpression state funcs expr

getArgsValues state funcs (expr:xs) = (finalState, val : newVals)
                                        where 
                                            (newState, val) = evalExpression state funcs expr
                                            (finalState, newVals) = getArgsValues newState funcs xs

evalExpression :: State -> [FunctionDefinition] -> Expression -> (State, Integer)

evalExpression state funcs (Number num)                        = (state, num)

evalExpression state funcs (Reference name)                    = (state, fromJust $ lookup name state)

evalExpression state funcs (Assign name expr)                  = ((name, newVal) : newState, newVal)
                                                                    where (newState, newVal) = evalExpression state funcs expr

evalExpression state funcs (BinaryOperation binop expr1 expr2) = (rightState, toBinaryFunction binop leftVal rightVal)
                                                                    where 
                                                                        (leftState, leftVal)   = evalExpression state funcs expr1
                                                                        (rightState, rightVal) = evalExpression leftState funcs expr2

evalExpression state funcs (UnaryOperation unop expr)          = (newState, toUnaryFunction unop val)
                                                                    where (newState, val) = evalExpression state funcs expr

evalExpression state funcs (FunctionCall name args)            = (newState, snd $ evalExpression funcState funcs (trd3 func))
                                                                    where
                                                                        (newState, argVals) = getArgsValues state funcs args
                                                                        funcState = zip (snd3 func) argVals ++ newState
                                                                        func = fromJust $ find ((== name) . fst3) funcs

evalExpression state funcs (Conditional cond ifCond ifNotCond) | toBool val = evalExpression newState funcs ifCond
                                                               | otherwise = evalExpression newState funcs ifNotCond
                                                                    where (newState, val) = evalExpression state funcs cond

evalExpression state funcs (Block exprs)                       = foldl (\(st, val) expr -> evalExpression st funcs expr) (state, 0) exprs
                                                                                                                             
-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (functions, expr) = snd $ evalExpression [] functions expr
