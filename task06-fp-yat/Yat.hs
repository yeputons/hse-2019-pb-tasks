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
addTabs = intercalate "\n" . map ("\t" ++) . lines

showExpression :: Expression -> String
showExpression (Number num)                       = show num
showExpression (Reference name)                   = name
showExpression (Assign name expr)                 = "let " ++ name ++ " = " ++ showExpression expr ++ " tel"
showExpression (BinaryOperation binop left right) = "(" ++ showExpression left ++ " " ++ showBinop binop ++ " " ++ showExpression right ++ ")"
showExpression (UnaryOperation unop expr)         = showUnop unop ++ showExpression expr
showExpression (FunctionCall name args)           = name ++ "(" ++ intercalate ", " (map showExpression args) ++ ")"
showExpression (Conditional expr true false)      = "if " ++ showExpression expr ++ " then " ++ showExpression true ++ " else " ++ showExpression false ++ " fi"
showExpression (Block exprs)                      = "{\n" ++ intercalate ";\n" (map (addTabs . showExpression) exprs) ++ "}"

showFunction :: FunctionDefinition -> String
showFunction (name, params, expr) = "func " ++ name ++ "(" ++ intercalate ", " params ++ ") = " ++ showExpression expr

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (functions, exprs) = intercalate "\n" $ map showFunction functions ++ [showExpression exprs]

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
 
getVarFromScope :: String -> State -> Integer
getVarFromScope name scope = fromMaybe 0 $ lookup name scope

getFuncName :: FunctionDefinition -> Name
getFuncName (name, _, _) = name 

getFuncArgs :: FunctionDefinition -> [Name]
getFuncArgs (_, args, _) = args 

getFuncExpr :: FunctionDefinition -> Expression
getFuncExpr (_, _, expr) = expr

evalExpression :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpression funcs scope (Number num)                       = (num, scope)
evalExpression funcs scope (Reference name)                   = (getVarFromScope name scope, scope)
evalExpression funcs scope (Assign name expr)                 = (res, (name, res):new_scope)
                                                                where (res, new_scope) = evalExpression funcs scope expr 
evalExpression funcs scope (BinaryOperation binop left right) = (toBinaryFunction binop res1 res2, new_scope2 ++ scope)
                                                                where (res1, new_scope1) = evalExpression funcs scope                 left
                                                                      (res2, new_scope2) = evalExpression funcs (scope ++ new_scope1) right
evalExpression funcs scope (UnaryOperation unop expr)         = (toUnaryFunction unop res, new_scope)
                                                                where (res, new_scope) = evalExpression funcs scope expr
evalExpression funcs scope (FunctionCall name args)           = (fst $ evalExpression funcs new_scope (getFuncExpr func), new_scope)
                                                                where new_scope       = zip (getFuncArgs func) (map (fst . evalExpression funcs scope) args) ++ args_scope
                                                                      (_, args_scope) = evalExpression funcs scope (Block args)
                                                                      func            = fromJust $ find ((== name). getFuncName) funcs
evalExpression funcs scope (Conditional expr true false)        | toBool res = evalExpression funcs new_scope true
                                                                | otherwise  = evalExpression funcs new_scope false
                                                                where (res, new_scope)  = evalExpression funcs scope expr 
evalExpression funcs scope (Block exprs)                      = foldl (\(value, scope) expr -> evalExpression funcs scope expr) (0, scope) exprs

eval :: Program -> Integer
eval (functions, expr) = fst (evalExpression functions [] expr)