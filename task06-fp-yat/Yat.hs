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

showExpr :: Expression -> String
showExpr (Number numb) = show numb
showExpr (Reference ref) = ref
showExpr (Assign n expr) = "let " ++ n ++ " = " ++ showExpr expr ++ " tel"
showExpr (BinaryOperation op l r) = "(" ++ showExpr l ++ " " ++ showBinop op ++ " " ++ showExpr r ++ ")"
showExpr (UnaryOperation op expr) = showUnop op ++ showExpr expr
showExpr (FunctionCall n []) = n ++ "()"
showExpr (FunctionCall n expr) = n ++ "(" ++ intercalate ", " (map showExpr expr) ++ ")"
showExpr (Conditional expr t f) = "if " ++ showExpr expr ++ " then " ++ showExpr t ++ " else " ++ showExpr f ++ " fi"
showExpr (Block []) = "{\n}"
showExpr (Block expr) = "{\n" ++ intercalate ";\n" (map (intercalate "\n" . map ("\t"++) . lines . showExpr) expr) ++ "\n}"

showFunDecl :: FunctionDefinition -> String
showFunDecl (n, param, expr) = "func " ++ n ++ "(" ++ intercalate "," param ++ ") = " ++ showExpr expr

showProgram :: Program -> String
showProgram (funcdefs, expr) = concatMap ((++ "\n") . showFunDecl) funcdefs ++ showExpr expr

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

--eval realization

assignToScope :: Name -> Integer -> State -> State

findFuncSignature :: Name -> [FunctionDefinition] -> FunctionDefinition
findFuncSignature name = head . filter (\(func, param, expr) -> func == name)

addArgs :: [Name] -> [Integer] -> State -> State
addArgs [] args scope                  = scope
addArgs names [] scope                 = scope
addArgs (elem:names) (arg:args) scope  = assignToScope elem arg $ addArgs names args scope

processArgs :: [Expression] -> [FunctionDefinition] -> State -> ([Integer], State)
processArgs [] funcDef scope      = ([], scope)
processArgs (elem : args) funcDef scope = add' value $ processArgs args funcDef scope'
                                          where (value, scope') = evalFunction (funcDef, elem) scope
                                                add' x (xs, s) = (x:xs, s)

assignToScope name value scope = case findIndex ((==)name . fst) scope of
                                Just i     -> take i scope ++ [(name, value)] ++ drop (i + 1) scope
                                _          -> (name, value) : scope

evalFunction :: Program -> State -> (Integer, State)
evalFunction (funcDef, Number numb) scope                         = (numb, scope)
evalFunction (funcDef, Reference name) []                         = undefined
evalFunction (funcDef, Reference name) (elem : scope)             | fst elem == name = (snd elem, elem : scope)
                                                                  | otherwise        = (fst elem', elem : snd elem')
                                                                  where elem' = evalFunction (funcDef, Reference name) scope
evalFunction (funcDef, Assign name expr) scope                    = (value, assignToScope name value scope')
                                                                  where (value, scope')   = evalFunction (funcDef, expr) scope
evalFunction (funcDef, BinaryOperation op lOp rOp) scope          = (toBinaryFunction op lOp' rOp', scope'')
                                                                  where (lOp', scope')   = evalFunction (funcDef, lOp) scope
                                                                        (rOp', scope'') = evalFunction (funcDef, rOp) scope'
evalFunction (funcDef, UnaryOperation op expr) scope              = (toUnaryFunction op value, scope')
                                                                  where (value, scope')   = evalFunction (funcDef, expr) scope
evalFunction (funcDef, FunctionCall name args) scope              = (fst $ evalFunction (funcDef, expr) (addArgs param newArgs scope'), scope')
                                                                  where (_, param, expr) = findFuncSignature name funcDef
                                                                        (newArgs, scope')    = processArgs args funcDef scope
evalFunction (funcDef, Conditional expr t f) scope                | fst value /= 0 = evalFunction (funcDef, t) $ snd value
                                                                  | otherwise      = evalFunction (funcDef, f) $ snd value
                                                                  where value    = evalFunction (funcDef, expr) scope
evalFunction (funcDef, Block []) scope                            = (0, scope)
evalFunction (funcDef, Block [expr]) scope                        = evalFunction (funcDef, expr) scope
evalFunction (funcDef, Block (elem:expr)) scope                   = evalFunction (funcDef, Block expr) scope'
                                                                  where scope' = snd $ evalFunction (funcDef, elem) scope  

eval :: Program -> Integer
eval pr = fst (evalFunction pr [])