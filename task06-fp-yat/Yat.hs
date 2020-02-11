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

showParams :: [Name] -> String
showParams [] = []
showParams [x] = x
showParams (p:params) = p ++ ", " ++ showParams params

showFunction :: FunctionDefinition -> String
showFunction (name, params, body) = "func " ++ name ++ "(" ++ (showParams params) ++ ") = " ++ showExpression body ++ "\n"

showExpression :: Expression -> String
showExpression (Number num)                     = show num
showExpression (Reference name)                 = name
showExpression (Assign name expression)         = "let " ++ name ++ " = " ++ showExpression expression ++ " tel"
showExpression (BinaryOperation op expr1 expr2) = "(" ++ showExpression expr1 ++ " " ++ showBinop op ++ " " ++ showExpression expr2 ++ ")"
showExpression (UnaryOperation op expr)         = showUnop op ++ showExpression expr
showExpression (FunctionCall name exprs)        = name ++ "(" ++ showParams (map showExpression exprs) ++ ")"
showExpression (Conditional cond expr1 expr2)   = "if " ++ showExpression cond ++ " then " ++ showExpression expr1 ++ " else " ++ showExpression expr2 ++ " fi"
showExpression (Block [])                       = "{\n}"
showExpression (Block exprs)                    = "{\n" ++ (intercalate "\n" . map ("\t" ++) . lines . intercalate ";\n" . map showExpression) exprs ++ "\n}"

showProgram :: Program -> String
showProgram (functions, expression) = (foldr (++) "" (map showFunction functions)) ++ showExpression expression

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

getVariable :: State -> Name -> Integer
getVariable [] _  = 0
getVariable (x:xs) name | name == fst x = snd x
                        | otherwise     = getVariable xs name

parseArgs :: [FunctionDefinition] -> State -> FunctionDefinition -> [Expression] -> (State, State)
parseArgs functions scope (_, [], _) _ = (scope, scope)
parseArgs functions scope (fName, argName : argNames, fExpr) (expr:exprs) = (fst result, fst evalResult ++ scope)
                                                                          where evalResult      = evalExpr functions scope expr
                                                                                function'       = (fName, argNames, fExpr) 
                                                                                scope'          = (argName, snd evalResult) : fst evalResult
                                                                                result          = parseArgs functions scope' function' exprs

solveBlock :: [FunctionDefinition] -> State -> [Expression] -> (State, Integer)
solveBlock functions scope []           = (scope, 0)
solveBlock functions scope [oneExpr]    = evalExpr functions scope oneExpr
solveBlock functions scope (expr:exprs) = solveBlock functions (fst (evalExpr functions scope expr)) exprs 



evalExpr :: [FunctionDefinition] -> State -> Expression -> (State, Integer)
evalExpr functions scope (Number num)                                                        = (scope, num) 
evalExpr functions scope (Reference name)                                                    = (scope, getVariable scope name)
evalExpr functions scope (Assign name expr)                                                  = ((name, snd result):fst result, snd result)
                                                                                               where result = evalExpr functions scope expr
evalExpr functions scope (BinaryOperation op left right)                                     = (fst result2, toBinaryFunction op (snd result1) (snd result2))
                                                                                               where result1 = evalExpr functions scope left
                                                                                                     result2 = evalExpr functions (fst result1) right
evalExpr functions scope (UnaryOperation op expr)                                            = (fst result, toUnaryFunction op (snd result)) 
                                                                                               where result = evalExpr functions scope expr
evalExpr ((fName, fArgs, fExpr):functions) scope (FunctionCall name args) | fName /= name    = evalExpr functions' scope (FunctionCall name args)
                                                                          | otherwise        = (snd scope', snd result)
                                                                            where func'      = (fName, fArgs, fExpr)
                                                                                  functions' = functions ++ [func']
                                                                                  scope'     = parseArgs functions' scope func' args
                                                                                  result     = evalExpr functions' (fst scope') fExpr
evalExpr functions scope (Conditional expr true false) | toBool (snd result)                 = evalExpr functions (fst result) true
                                                       | otherwise                           = evalExpr functions (fst result) false
                                                         where result                        = evalExpr functions scope expr
evalExpr functions scope (Block exprs)                                                       = solveBlock functions scope exprs 

eval :: Program -> Integer
eval (funcs, expr) = snd (evalExpr funcs [] expr)