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

interpose :: String -> [String] -> String
interpose _ []             = ""
interpose _ [s]            = s
interpose separator (x:xs) = x ++ separator ++ interpose separator xs

addTabs :: String -> String
addTabs = interpose "\n" . map ("\t" ++) . lines

showExpression :: Expression -> String
showExpression (Number num)                               = show num
showExpression (Reference ref)                            = ref
showExpression (Assign name expr)                         = "let " ++ name ++ " = " ++ showExpression expr ++ " tel"
showExpression (BinaryOperation binop leftExpr rightExpr) = "(" ++ showExpression leftExpr ++ " " ++ showBinop binop ++ " " ++ showExpression rightExpr ++ ")"
showExpression (UnaryOperation unop expr)                 = showUnop unop ++ showExpression expr
showExpression (FunctionCall name exprs)                  = name ++ "(" ++ interpose ", " (map showExpression exprs) ++ ")"
showExpression (Conditional expr exprIfTrue exprIfFalse)  = "if " ++ showExpression expr ++ " then " ++ showExpression exprIfTrue ++ " else " ++ showExpression exprIfFalse ++ " fi"
showExpression (Block [])                                 = "{\n}"
showExpression (Block exprs)                              = "{\n" ++ addTabs (interpose ";\n" (map showExpression exprs)) ++ "\n}"

showFunction :: FunctionDefinition -> String
showFunction (name, args, expr) = "func " ++ name ++ "(" ++ interpose "," args ++ ") = " ++ showExpression expr

showFunctions :: [FunctionDefinition] -> String
showFunctions []    = ""
showFunctions funcs = interpose "\n" (map showFunction funcs) ++ "\n"

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (funcs, body) = showFunctions funcs ++ showExpression body

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
--} -- Удалите эту строчку, если решаете бонусное задание.

-- Реализуйте eval: запускает программу и возвращает её значение.

fst3 :: (a, b, c) -> a
fst3 (a, _, _) = a

snd3 :: (a, b, c) -> b
snd3 (_, b, _) = b

thd3 :: (a, b, c) -> c
thd3 (_, _, c) = c

getVariableFromState :: String -> State -> Integer
getVariableFromState name []                     = undefined
getVariableFromState name ((variable, value):xs) | variable == name = value 
                                                 | otherwise        = getVariableFromState name xs

assignVarInState :: String -> Integer -> State -> (Integer, State)
assignVarInState name val state = case find ((==) name . fst) state of
                                    Just indx   -> (val, filter ((/=) name . fst) state ++ [(name, val)]) 
                                    _           -> (val, state ++ [(name, val)])

evalArgsFunction :: State -> [FunctionDefinition] -> [Expression] -> (State, [Integer])
evalArgsFunction state funcs []           = (state, [])
evalArgsFunction state funcs [expr]       = (state', [val])
                                              where
                                                  (val, state') = evalPart (funcs, expr) state
evalArgsFunction state funcs (expr:exprs) = (state'', val : vals)
                                              where
                                                  (val, state') = evalPart (funcs, expr) state
                                                  (state'', vals) = evalArgsFunction state' funcs exprs

evalPart :: Program -> State -> (Integer, State)
evalPart (funcs, Number num) state                               = (num, state)
evalPart (funcs, Reference name) state                           = (getVariableFromState name state, state)
evalPart (funcs, Assign name expr) state                         = assignVarInState name val state'
                                                                     where
                                                                         (val, state') = evalPart (funcs, expr) state
evalPart (funcs, BinaryOperation binop leftExpr rightExpr) state = (toBinaryFunction binop leftVal rightVal, state'')
                                                                     where
                                                                         (leftVal, state') = evalPart (funcs, leftExpr) state
                                                                         (rightVal, state'') = evalPart (funcs, rightExpr) state'
evalPart (funcs, UnaryOperation unop expr) state                 = (toUnaryFunction unop value, state')
                                                                     where
                                                                         (value, state') = evalPart (funcs, expr) state
evalPart (funcs, FunctionCall name args) state                   = (fst $ evalPart (funcs, thd3 func) funcState, state')
                                                                     where
                                                                         (state', argsValues) = evalArgsFunction state funcs args
                                                                         func                 = fromJust $ find ((==) name . fst3) funcs
                                                                         funcState            = zip (snd3 func) argsValues ++ state'
evalPart (funcs, Conditional exprCond exprTrue exprFalse) state  | toBool (fst retCond) = evalPart (funcs, exprTrue) (snd retCond)
                                                                 | otherwise            = evalPart (funcs, exprFalse) (snd retCond)
                                                                     where
                                                                         retCond = evalPart (funcs, exprCond) state
evalPart (funcs, Block exprs) state                              = foldl (\(val, state') expr -> evalPart (funcs, expr) state') (0, state) exprs

eval :: Program -> Integer
eval program = fst $ evalPart program [] 
