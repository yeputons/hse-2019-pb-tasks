module Yat where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Data.List
import Data.Maybe
import Data.Bifunctor
import Debug.Trace

{-# ANN module "HLint: ignore Use first" #-}
{-# ANN module "HLint: ignore Use second" #-}

-- В логических операциях 0 считается ложью, всё остальное - истиной.
-- При этом все логические операции могут вернуть только 0 или 1.

-- Все возможные бинарные операции: сложение, умножение, вычитание, деление, взятие по модулю, <, <=, >, >=, ==, !=, логическое &&, логическое ||
data Binop = Add | Mul | Sub | Div | Mod | Lt | Le | Gt | Ge | Eq | Ne | And | Or

-- Все возможные унарные операции: смена знака числа и логическое "не".
data Unop = Neg | Not

data Expression = Number Integer  -- Возвращает число, побочных эффектов нет.
                | Reference Name  -- Возвращает значение соответствующей переменной в текущем state, побочных эффектов нет.
                | Assign Name Expression  -- Вычисляет операнд, а потом изменяет значение соответствующей переменной и возвращает его. Если соответствующей переменной нет, она создаётся.
                | BinaryOperation Binop Expression Expression  -- Вычисляет сначала левый операнд, потом правый, потом возвращает результат операции. Других побочных эффектов нет.
                | UnaryOperation Unop Expression  -- Вычисляет операнд, потом применяет операцию и возвращает результат. Других побочных эффектов нет.
                | FunctionCall Name [Expression]  -- Вычисляет аргументы от первого к последнему в текущем state, потом создаёт новый state для дочерней функции (копию текущего с добавленными параметрами), возвращает результат работы функции.
                | Conditional Expression Expression Expression -- Вычисляет первый Expression, в случае истины вычисляет второй Expression, в случае лжи - третий. Возвращает соответствующее вычисленное значение.
                | Block [Expression] -- Вычисляет в текущем state все выражения по очереди от первого к последнему, результат вычисления -- это результат вычисления последнего выражения или 0, если список пуст.

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

-- Верните текстовое представление программы (см. условие).

showExpression :: Expression -> String
showExpression (Number num)                      = show num
showExpression (Reference name)                  = name
showExpression (Assign name expr)                = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op left right)   = concat ["(", showExpression left, " ", showBinop op, " ", showExpression right, ")"]
showExpression (UnaryOperation op expr)          = showUnop op ++ showExpression expr
showExpression (FunctionCall name args)          = concat [name, "(", intercalate ", " $ map showExpression args, ")"]
showExpression (Conditional expr ifTrue ifFalse) = concat ["if ", showExpression expr, " then ", showExpression ifTrue, " else ", showExpression ifFalse, " fi"]
showExpression (Block exprs)                     = concat ["{\n", concatMap (("\t" ++) . (++ "\n")) (lines $ intercalate ";\n" (map showExpression exprs)), "}"]


showFunction :: FunctionDefinition -> String
showFunction (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expr]

showProgram :: Program -> String
showProgram (funcs, body) = concatMap ((++ "\n") . showFunction) funcs ++ showExpression body  

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

parseArgs :: State -> [FunctionDefinition] -> FunctionDefinition -> [Expression] -> (State, State)

parseArgs state funcs (_, fNames, _) args = (intoFunc ++ newState, newState)
                                              where (newState, intoFunc) = foldl (\(state, intoFunc) (name, arg) ->
                                                                                  let (resState, resValue) = evalExpression state funcs arg
                                                                                  in (resState, (name, resValue):intoFunc)) (state, []) (zip fNames args)

evalExpression :: State -> [FunctionDefinition] -> Expression -> (State, Integer)
evalExpression state funcs (Number num)                      = (state, num)

evalExpression state _     (Reference name)                  = (state, resValue)
                                                                 where (Just resValue) = lookup name state

evalExpression state funcs (Assign name expr)                = ((name, resValue):resState, resValue) 
                                                                 where (resState, resValue) = evalExpression state funcs expr

evalExpression state funcs (BinaryOperation op left right)   = (rightResState, toBinaryFunction op leftResValue rightResValue)
                                                                 where (leftResState, leftResValue)  = evalExpression state funcs left
                                                                       (rightResState, rightResValue) = evalExpression leftResState funcs right 

evalExpression state funcs (UnaryOperation op expr)          = (resState, toUnaryFunction op resValue)
                                                                 where (resState, resValue) = evalExpression state funcs expr

evalExpression state funcs (FunctionCall name args)          = (newState, resValue)
                                                                 where (Just func)              = find (\(fName, _, _) -> fName == name) funcs 
                                                                       (newFuncState, newState) = parseArgs state funcs func args
                                                                       (_, resValue)            = evalExpression newFuncState funcs funcExpr
                                                                       (_, _, funcExpr)         = func

evalExpression state funcs (Conditional cond ifTrue ifFalse) = evalExpression resState funcs resExpr
                                                                 where resExpr = if toBool resValue then ifTrue else ifFalse
                                                                       (resState, resValue) = evalExpression state funcs cond

evalExpression state funcs (Block exprs)                     = foldl (\(curState, _) expr -> evalExpression curState funcs expr) (state, 0) exprs 

eval :: Program -> Integer
eval (funcs, body) = snd $ evalExpression [] funcs body
