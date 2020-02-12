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
showExpression (Number n)                            = show n
showExpression (Reference name)                      = name
showExpression (Assign name expr)                    = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op l r)              = concat ["(", showExpression l, " ", showBinop op, " ", showExpression r, ")"]
showExpression (UnaryOperation op e)                 = showUnop op ++ showExpression e
showExpression (FunctionCall name args)              = concat [name, "(", intercalate ", " (map showExpression args), ")"]
showExpression (Conditional cond caseTrue caseFalse) = concat ["if ", showExpression cond, " then ", showExpression caseTrue, " else ", showExpression caseFalse, " fi"]
showExpression (Block expr)                          = concat ["{\n", concatMap (("\t" ++) . (++ "\n")) (lines $ intercalate ";\n" (map showExpression expr)), "}"]


-- Верните текстовое представление программы (см. условие).

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, params, expr) = concat ["func ", name, "(", intercalate ", " params, ") = ", showExpression expr, "\n"]

showProgram :: Program -> String
showProgram (functions, expr) = concatMap showFunctionDefinition functions ++ showExpression expr

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

addToState :: State -> [Name] -> [Integer] -> State
addToState state names vars = zip names vars ++ state

getDeclResult :: [FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
getDeclResult functions state  []     = ([], state)
getDeclResult functions state  (x:xs) = (fst fExprRes:fst rest, snd rest)
                                       where fExprRes = evalExpression    functions state      x
                                             rest     = getDeclResult functions (snd fExprRes) xs 

getFunctionDefinition :: Name -> [FunctionDefinition] -> ([Name], Expression)
getFunctionDefinition name functions = getter (head (filter (nameFilter name) functions)) 
                             where nameFilter name (n, names, e)    = name == n
                                   getter (n, name, e)              = (name, e)

evalExpression :: [FunctionDefinition] -> State -> Expression -> (Integer, State)

evalExpression functions state (Number n)                            = (n, state)
evalExpression functions state (Reference name)                      = case lookup name state of
                                                                       Just a  -> (a, state)
                                                                       Nothing -> (0, state)
evalExpression functions state (Assign name expr)                    = (fst expRes, (name, fst expRes):snd expRes)
                                                                       where expRes          = evalExpression functions state expr
evalExpression functions state (BinaryOperation op l r)              = (toBinaryFunction op (fst lRes) (fst rRes), snd rRes)
                                                                       where lRes            = evalExpression functions state l
                                                                             rRes            = evalExpression functions (snd lRes) r
evalExpression functions state (UnaryOperation op expr)              = (toUnaryFunction op (fst expRes), snd expRes)
                                                                       where expRes          = evalExpression functions state expr
evalExpression functions state (FunctionCall name args)              = (fst resF, snd argsRes) 
                                                                       where function        = getFunctionDefinition name functions
                                                                             argsRes         = getDeclResult functions state args
                                                                             newState        = addToState (snd argsRes) (fst function) (fst argsRes)
                                                                             resF            = evalExpression functions newState (snd function)
evalExpression functions state (Conditional cond caseTrue caseFalse) | toBool (fst condRes)  = evalExpression functions (snd condRes) caseTrue
                                                                     | otherwise             = evalExpression functions (snd condRes) caseFalse 
                                                                       where condRes         =  evalExpression functions state cond
evalExpression functions state (Block [])                            = (0, state)
evalExpression functions state (Block[exp])                          = evalExpression functions state exp
evalExpression functions state (Block(x:xs))                         = evalExpression functions (snd exprRes) (Block xs)
                                                                       where exprRes         = evalExpression functions state x  
-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval program = fst (evalExpression (fst program) [] (snd program))