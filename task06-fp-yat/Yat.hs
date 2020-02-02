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
chainFuncCall :: [Expression] -> String
chainFuncCall []     = ""
chainFuncCall [e]    = showExpression e ""
chainFuncCall (e:es) = showExpression e "" ++ ", " ++ chainFuncCall es

chainBlock :: [Expression] -> String -> String
chainBlock [] _          = ""
chainBlock [e] indent    = indent ++ showExpression e indent ++ "\n"
chainBlock (e:es) indent = indent ++ showExpression e indent ++ ";\n" ++ chainBlock es indent

showExpression :: Expression -> String -> String
showExpression (Number n) indent                       = show n
showExpression (Reference name) indent                 = name
showExpression (Assign name expr) indent               = "let " ++ name ++ " = " ++ showExpression expr indent ++ " tel"
showExpression (BinaryOperation op expr1 expr2) indent = "(" ++ showExpression expr1 indent ++ " " ++ showBinop op ++ " " ++ showExpression expr2 indent ++ ")"
showExpression (UnaryOperation op expr) indent         = showUnop op ++ showExpression expr indent
showExpression (FunctionCall name exprs) indent        = name ++ "(" ++ chainFuncCall exprs ++ ")"
showExpression (Conditional e t f) indent              = "if " ++ showExpression e indent ++ " then " ++ showExpression t indent ++ " else " ++ showExpression f indent ++ " fi"
showExpression (Block commands) indent                 = "{\n" ++ chainBlock commands (indent ++ "\t") ++ indent ++ "}"

chainFuncDef :: [Name] -> String
chainFuncDef []     = ""
chainFuncDef [n]    = n
chainFuncDef (n:ns) = n ++ ", " ++ chainFuncDef ns

showFuncDef :: FunctionDefinition -> String
showFuncDef (name, params, expr) = "func " ++ name ++ "(" ++ chainFuncDef params ++ ") = " ++ showExpression expr "" ++ "\n"

showProgram :: Program -> String
showProgram (definitions, expr) = foldr ((++) . showFuncDef) "" definitions ++ showExpression expr ""

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
getVariable [] _                             = 0
getVariable ((varName, varValue):scope) name | name == varName = varValue
                                             | otherwise       = getVariable scope name 

getFunctionBody :: [FunctionDefinition] -> Name -> Expression
getFunctionBody [] _                                        = Number 0
getFunctionBody ((funcName, funcArgs, funcBody):funcs) name | name == funcName = funcBody
                                                            | otherwise        = getFunctionBody funcs name 

getFunctionArgs :: [FunctionDefinition] -> Name -> [Name]
getFunctionArgs [] _                                        = []
getFunctionArgs ((funcName, funcArgs, funcBody):funcs) name | name == funcName = funcArgs
                                                            | otherwise        = getFunctionArgs funcs name 

evalChainFunc :: [Expression] -> [Name] -> State -> [FunctionDefinition] -> ([Integer], State)
evalChainFunc [_] [] _ _                             = ([0], [])
evalChainFunc (_:_:_) [] _ _                         = ([0], [])
evalChainFunc [] _ scope funcs                       = ([0], scope)
evalChainFunc [expr] [name] scope funcs              = ([fst result], snd result)
                                                      where result = evalExpression expr scope funcs
evalChainFunc (expr:others) (name:names) scope funcs = (fst result:fst next, snd next)
                                                      where result = evalExpression expr scope funcs
                                                            next   = evalChainFunc others names (snd result) funcs


makeScopeForFunction :: Expression -> State -> [FunctionDefinition] -> (State, State)
makeScopeForFunction (FunctionCall name exprs) scope funcs = (sscope, fscope)
                                                            where res    = evalChainFunc exprs (getFunctionArgs funcs name) scope funcs
                                                                  sscope = snd res
                                                                  fscope = zip (getFunctionArgs funcs name) (fst res) ++ sscope
makeScopeForFunction exp _ _                               = ([], [])

evalChainBlock :: [Expression] -> State -> [FunctionDefinition] -> (Integer, State)
evalChainBlock [] scope funcs              = (0, scope)
evalChainBlock [expr] scope funcs          = evalExpression expr scope funcs
evalChainBlock (expr:commands) scope funcs = evalChainBlock commands (snd (evalExpression expr scope funcs)) funcs

evalExpression :: Expression -> State -> [FunctionDefinition] -> (Integer, State)
evalExpression (Number n) scope funcs                       = (n, scope)
evalExpression (Reference name) scope funcs                 = (getVariable scope name, scope)
evalExpression (Assign name expr) scope funcs               = (fst result, (name, fst result):snd result)
                                                             where result = evalExpression expr scope funcs
evalExpression (BinaryOperation op expr1 expr2) scope funcs = (toBinaryFunction op (fst result1) (fst result2), snd result2)
                                                             where result1 = evalExpression expr1 scope funcs
                                                                   result2 = evalExpression expr2 (snd result1) funcs 
evalExpression (UnaryOperation op expr) scope funcs         = (toUnaryFunction op (fst result), snd result)
                                                             where result = evalExpression expr scope funcs
evalExpression (FunctionCall name exprs) scope funcs        = (rv, sscope)
                                                             where rv         = fst (evalExpression (getFunctionBody funcs name) fscope funcs)
                                                                   new_scopes = makeScopeForFunction (FunctionCall name exprs) scope funcs
                                                                   fscope     = snd new_scopes
                                                                   sscope     = fst new_scopes
evalExpression (Conditional e t f) scope funcs              | toBool(fst eres)         = tres
                                                            | otherwise                = fres
                                                             where eres = evalExpression e scope funcs
                                                                   tres = evalExpression t (snd eres) funcs
                                                                   fres = evalExpression f (snd eres) funcs

evalExpression (Block commands) scope funcs                 = evalChainBlock commands scope funcs

eval :: Program -> Integer
eval (definitions, expr) = fst (evalExpression expr [] definitions)
{--}  