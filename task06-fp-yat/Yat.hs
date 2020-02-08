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

type Function = ([Name], Expression)
type MyFunctionDefinition = (Name, Function)
type FullState = (State, [MyFunctionDefinition])

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

applyHead _ []        = undefined
applyHead head [x]    = [head x]
applyHead head (x:xs) = head x : xs 

applyEnd [] _       = undefined
applyEnd [x] end    = [end x]
applyEnd (x:xs) end = x : applyEnd xs end

merge xs []        = xs
merge [] xs        = xs
merge [x] (xx:xss) = (x ++ xx) : xss
merge (x:xs) xss   = x : merge xs xss

showExpr :: Expression -> [String]
showExpr (Number n)                                = [show n]
showExpr (Reference name)                          = [name]
showExpr (Assign name expr)                        = (("let " ++ name ++ " = ") ++) `applyHead` (showExpr expr) `applyEnd` (++ " tel")
showExpr (BinaryOperation binop expr1 expr2)       = (("(" ++) `applyHead` (showExpr expr1)) `merge` (((" " ++ showBinop binop ++ " ") ++) `applyHead` (showExpr expr2) `applyEnd` (++ ")"))
showExpr (UnaryOperation unop expr)                = (showUnop unop ++) `applyHead` (showExpr expr)
showExpr (FunctionCall fName [])                   = [fName ++ "()"]
showExpr (FunctionCall fName exprs)                = ((fName ++ "(") ++) `applyHead` (showExpr (head exprs)) `merge` (foldr (merge . applyHead (", " ++) . showExpr) [] (tail exprs)) `applyEnd` (++ ")")
showExpr (Conditional condExpr trueExpr falseExpr) = ("if " ++) `applyHead` (showExpr condExpr) `merge` ((" then " ++) `applyHead` (showExpr trueExpr)) `merge` ((" else " ++) `applyHead` (showExpr falseExpr) `applyEnd` (++ " fi"))
showExpr (Block [])                                = ["{","}"]
showExpr (Block exprs)                             = ["{"] ++ (map ("\t" ++) (foldr1 ((++) . (`applyEnd` (++ ";"))) (map showExpr exprs))) ++ ["}"]


showFunction :: FunctionDefinition -> [String]
showFunction (fName, paramsNames, expr) = (("func " ++ fName ++ "(" ++ (intercalate ", " paramsNames) ++ ") = ") ++) `applyHead` (showExpr expr)

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (funcList, expr) = intercalate "\n" $ (concatMap showFunction funcList) ++ (showExpr expr)

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

applyFst func (x,y) = (func x, y)


val :: Name -> FullState -> Integer
val name (state,_) = findByName name state

function :: Name -> FullState -> Function
function name (_,funcs) = findByName name funcs

findByName _ []        = undefined
findByName name [x]    | name == fst x = snd x
                       | otherwise     = undefined
findByName name (x:xs) | name == fst x = snd x
                       | otherwise     = findByName name xs


callFunction :: Function -> [Integer] -> FullState -> Integer
callFunction (names,expr) vals (state, funcs) = fst $ evalExpr expr state1
                                                where state1 = ((zip names vals) ++ state, funcs)


evalExprs :: [Expression] -> FullState -> ([Integer], FullState)
evalExprs [] state     = ([], state)
evalExprs [x] state    = ([value], state1)
                       where (value, state1) = evalExpr x state
evalExprs (x:xs) state = (value:valueList, state2)
                       where (value, state1) = evalExpr x state
                             (valueList, state2) = evalExprs xs state1


evalExpr :: Expression -> FullState -> (Integer, FullState)
evalExpr (Number n) state                                = (n, state)
evalExpr (Reference name) state                          = (val name state, state)
evalExpr (Assign name expr) state                        = (exprRet, applyFst ([(name, exprRet)] ++) stateRet)
                                                         where (exprRet, stateRet) = evalExpr expr state
evalExpr (BinaryOperation binop expr1 expr2) state       = (toBinaryFunction binop expr1Ret expr2Ret, state2)
                                                         where (expr1Ret, state1) = evalExpr expr1 state
                                                               (expr2Ret, state2) = evalExpr expr2 state1
evalExpr (UnaryOperation unop expr) state                = (toUnaryFunction unop exprRet, stateRet)
                                                         where (exprRet, stateRet) = evalExpr expr state
evalExpr (FunctionCall fName exprs) state                = (callFunction (function fName state) params state1, state1)
                                                         where (params, state1) = evalExprs exprs state
evalExpr (Conditional condExpr trueExpr falseExpr) state | condVal == 0 = evalExpr falseExpr state1
                                                         | otherwise    = evalExpr trueExpr state1
                                                         where (condVal, state1) = evalExpr condExpr state
evalExpr (Block []) state                                = (0, state)
evalExpr (Block exprs) state                             = applyFst last (evalExprs exprs state)

eval :: Program -> Integer
eval (funcDef, expr) = fst $ evalExpr expr ([], map (\(a, b, c) -> (a, (b, c))) funcDef)