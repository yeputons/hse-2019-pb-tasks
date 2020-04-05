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

showFunctionWithParams :: Name -> [a] -> (a -> String) -> String
showFunctionWithParams name params showParam = concat [name, "(", intercalate ", " (map showParam params), ")"]

addTabs :: String -> String
addTabs = concatMap (\line -> "\t" ++ line ++ "\n") . lines

showExpression :: Expression -> String
showExpression (Number n)               = show n
showExpression (Reference name)         = name
showExpression (Assign name e)          = concat ["let ", name, " = ", showExpression e,  " tel"]
showExpression (BinaryOperation op l r) = concat ["(", showExpression l, " ", showBinop op, " ", showExpression r, ")"]
showExpression (UnaryOperation op e)    = showUnop op ++ showExpression e
showExpression (FunctionCall name es)   = showFunctionWithParams name es showExpression
showExpression (Conditional e t f)      = concat ["if ", showExpression e, " then ", showExpression t, " else ", showExpression f, " fi"]
showExpression (Block es)               = "{\n" ++ addTabs (intercalate ";\n" (map showExpression es)) ++ "}"

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, params, e) = concat ["func ", showFunctionWithParams name params id, " = ", showExpression e, "\n"]

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (fs, e) = concatMap showFunctionDefinition fs ++ showExpression e

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

getFuncName :: FunctionDefinition -> String
getFuncName (name, _, _) = name

evalParams :: [(Name, Expression)] -> [FunctionDefinition] -> State -> ([(Name, Integer)], State)
evalParams params fds startState = 
  foldl evalParam ([], startState) params
  where
    evalParam :: ([(Name, Integer)], State) -> (Name, Expression) -> ([(Name, Integer)], State)
    evalParam (paramsVals, state) (name, e) = let (val, newState) = evalExpression e fds state
                                              in ((name, val):paramsVals, newState)

evalExpression :: Expression -> [FunctionDefinition] -> State -> (Integer, State)
evalExpression (Number n)               fds state = (n, state)
evalExpression (Reference name)         fds state = (fromJust $ lookup name state, state) 
evalExpression (Assign name  e)         fds state = let (val, newState) = evalExpression e fds state
                                                    in (val, (name, val):newState)
evalExpression (BinaryOperation op l r) fds state = let (lVal, newStateAfterLeft)  = evalExpression l fds state
                                                        (rVal, newStateAfterRight) = evalExpression r fds newStateAfterLeft
                                                    in (toBinaryFunction op lVal rVal, newStateAfterRight)
evalExpression (UnaryOperation op e)    fds state = let (val, newState) = evalExpression e fds state
                                                    in (toUnaryFunction op val, newState) 
evalExpression (FunctionCall name es)   fds state = let (_, params, body)        = fromJust $ find (\fd -> getFuncName fd == name) fds
                                                        (evaledParams, newState) = evalParams (zip params es) fds state
                                                        getOnlyValueFromEvaled (val, _) = val
                                                    in (getOnlyValueFromEvaled $ evalExpression body fds $ evaledParams ++ newState, newState)
evalExpression (Conditional e t f)      fds state = let (cond, newState) = evalExpression e fds state
                                                    in evalExpression (if toBool cond then t else f) fds newState
evalExpression (Block es)               fds state = foldl (\(val, st) e -> evalExpression e fds st) (0, state) es

-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (fds, e) = let getOnlyValueFromEvaled (val, _) = val
                in getOnlyValueFromEvaled $ evalExpression e fds []
