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

-- Верните текстовое представление программы (см. условие).

indentation :: String -> String
indentation []                 = []
indentation (s:tr) | s == '\n' = [s] ++ "\t" ++ indentation tr
                   | otherwise = s:indentation tr

showExpression (Number n)                    = show n
showExpression (Reference name)              = name
showExpression (Assign name val)             = "let " ++ name ++ " = " ++ showExpression val ++ " tel"
showExpression (BinaryOperation oper x y)    = "(" ++ showExpression x ++ " " ++ showBinop oper ++ " " ++ showExpression y ++ ")"
showExpression (UnaryOperation uop val)      = showUnop uop ++ showExpression val
showExpression (FunctionCall fun [])         = fun ++ "()"
showExpression (FunctionCall fun (x:xs))     = fun ++ "(" ++ showExpression x ++ concatMap ((++) ", " . showExpression) xs ++ ")"
showExpression (Conditional cond true false) = "if " ++ showExpression cond ++ " then " ++ showExpression true ++ " else " ++ showExpression false ++ " fi"
showExpression (Block [])                    = "{\n}"
showExpression (Block (x:xs))                = indentation ("{\n" ++ showExpression x ++ concatMap ((++) ";\n" . showExpression) xs) ++ "\n}"

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, [], definition)           = "func " ++ name ++ "() = " ++ showExpression definition
showFunctionDefinition (name , cur:others, definition)  = "func " ++ name ++ "(" ++ cur ++ concatMap (", " ++) others ++ ") = " ++ showExpression definition

showProgram :: Program -> String
showProgram prog = concatMap ((++ "\n") . showFunctionDefinition) (fst prog) ++ showExpression (snd prog)

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

-- Реализуйте eval: запускает программу и возвращает её значение.

modifyScope :: State -> String -> Integer -> State
modifyScope scope var val = filter (\s -> var /= fst s) scope ++ zip (replicate 1 var) (replicate 1 val)

functionScope :: State -> State -> State
functionScope = foldl (\ scope x -> uncurry (modifyScope scope) x)

getValue :: State -> String -> Integer
getValue scope var = case lookup var scope of
                                Just a -> a
                                _      -> 0

evaluateArgs :: [Name] -> State -> [FunctionDefinition] -> [Expression] -> State
evaluateArgs []     _     _     _            = undefined
evaluateArgs _      _     _     []           = undefined
evaluateArgs [a]    scope funcs [expr]       = modifyScope (fst (evalExpression scope funcs expr)) a (snd (evalExpression scope funcs expr))
evaluateArgs (x:xs) scope funcs (expr:exprs) = evaluateArgs xs (modifyScope (fst (evalExpression scope funcs expr)) x (snd (evalExpression scope funcs expr))) funcs exprs

getFunctionName :: FunctionDefinition -> Name
getFunctionName (name, _, _) = name

getFunctionArgs :: FunctionDefinition -> [Name]
getFunctionArgs (_, args, _) = args

getFunctionExpression :: FunctionDefinition -> Expression
getFunctionExpression (_, _, expr) = expr


findFunction :: [FunctionDefinition] -> [FunctionDefinition] -> State -> Name -> [Expression] -> (State, Integer)
findFunction []     _     _     _        _    = undefined
findFunction (x:xs) funcs scope funcName oper | getFunctionName x == funcName = (fst $ evalExpression scope funcs (Block oper), snd $ evalExpression (evaluateArgs (getFunctionArgs x) scope funcs oper) funcs (getFunctionExpression x))
                                              | otherwise                     = findFunction xs funcs scope funcName oper


evalExpression :: State -> [FunctionDefinition] -> Expression -> (State, Integer)
evalExpression scope _     (Number a)               = (scope, a)
evalExpression scope _     (Reference a)            = (scope, getValue scope a)
evalExpression scope funcs (Assign var val)         = (modifyScope (fst (evalExpression scope funcs val)) var (snd (evalExpression scope funcs val)), snd (evalExpression scope funcs val))
evalExpression scope funcs (BinaryOperation op a b) = second (toBinaryFunction op (snd (evalExpression scope funcs a)))(evalExpression (fst (evalExpression scope funcs a)) funcs b)
evalExpression scope funcs (UnaryOperation uop a)   = second (toUnaryFunction uop) (evalExpression scope funcs a)
evalExpression scope funcs (FunctionCall fun a)     = findFunction funcs funcs scope fun a
evalExpression scope funcs (Conditional cond a b)   | toBool(snd (evalExpression scope funcs cond))     = evalExpression (fst (evalExpression scope funcs cond)) funcs a
                                                    | otherwise                                         = evalExpression (fst (evalExpression scope funcs cond)) funcs b

evalExpression scope _     (Block [])               = (scope, 0)
evalExpression scope funcs (Block [x])              = evalExpression scope funcs x
evalExpression scope funcs (Block (x:xs))           = evalExpression (fst $ evalExpression scope funcs x) funcs (Block xs)

eval :: Program -> Integer
eval programm = snd (uncurry (evalExpression []) programm)
