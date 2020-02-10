module Yat where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Data.List
import Data.List.Split
import qualified Data.Map.Strict as Map
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
type State = Map.Map Name Integer  -- Список пар (имя переменной, значение). Новые значения дописываются в начало, а не перезаписываютсpя
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
showProgram :: Program -> String
showProgram (funcs, expr) = indentProgram $ concatMap showFunction' funcs ++ showExpression' expr

showFunction' :: FunctionDefinition -> String -- add \n to the end of string
showFunction' (funcname, argsnames, expr) = "func " ++ funcname ++ "(" ++ intercalate ", " argsnames ++ ") = " ++ showExpression' expr ++ "\n"

showExpression' :: Expression -> String -- no indentation
showExpression' (Number value)                          = show value
showExpression' (Reference name)                        = name
showExpression' (Assign varname expr)                   = "let " ++ varname ++ " = " ++ showExpression' expr ++ " tel"
showExpression' (BinaryOperation binop exprL exprR)     = "(" ++ showExpression' exprL ++ " " ++ showBinop binop ++ " " ++ showExpression' exprR ++ ")"
showExpression' (UnaryOperation unop expr)              = showUnop unop ++ showExpression' expr
showExpression' (FunctionCall funcname expressions)     = funcname ++ "(" ++ intercalate ", " (map showExpression' expressions) ++ ")"
showExpression' (Conditional exprIf exprThen exprElse)  = "if " ++ showExpression' exprIf ++ " then " ++ showExpression' exprThen ++ " else " ++ showExpression' exprElse ++ " fi"
showExpression' (Block expressions)                     = "{\n" ++ showExpressionBlock' expressions ++ "}"

showExpressionBlock' :: [Expression] -> String
showExpressionBlock' []         = "\n"
showExpressionBlock' [expr]     = showExpression' expr ++ "\n"
showExpressionBlock' (expr:exs) = showExpression' expr ++ ";\n" ++ showExpressionBlock' exs

indentProgram :: String -> String
indentProgram prog = indentProgram' (splitOn "\n" prog) 0

indentProgram' :: [String] -> Int -> String
indentProgram' [] depth                 = ""
indentProgram' ['}':line] depth         = indentLine ("}" ++ line) (depth - 1)
indentProgram' [line] depth             = indentLine line depth 
indentProgram' ("}":ls) depth           = indentLine "}" (depth - 1) ++ "\n" ++ indentProgram' ls (depth - 1)
indentProgram' (('}':line):ls) depth    = case last line of
                                            '{' -> indentLine ("}" ++ line) (depth - 1) ++ "\n" ++ indentProgram' ls depth
                                            _   -> indentLine ("}" ++ line) (depth - 1) ++ "\n" ++ indentProgram' ls (depth - 1)
indentProgram' ([]:ls) depth            = indentProgram' ls depth
indentProgram' (line:ls) depth          = case last line of
                                            '{' -> indentLine line depth ++ "\n" ++ indentProgram' ls (depth + 1)
                                            _   -> indentLine line depth ++ "\n" ++ indentProgram' ls depth

indentLine :: String -> Int -> String
indentLine line depth = fillTabs depth ++ line 

fillTabs :: Int -> String
fillTabs n = concat $ replicate n "\t"

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
eval :: Program -> Integer
eval (funcs, expr) = fst $ evalExpression expr funcs Map.empty 

evalExpression :: Expression -> [FunctionDefinition] -> State -> (Integer, State)
evalExpression (Number value) _ state               = (value, state)
evalExpression (Reference varname) _ state          = case Map.lookup varname state of
                                                        Just value  -> (value, state)
                                                        _           -> undefined -- variable not found
evalExpression (Assign varname expr) funcs state    = (exprValue, Map.insert varname exprValue returnedState)
    where (exprValue, returnedState) = evalExpression expr funcs state
evalExpression (BinaryOperation binop exprL exprR) funcs state = undefined