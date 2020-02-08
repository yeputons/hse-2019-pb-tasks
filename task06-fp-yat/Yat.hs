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


functionsCall :: [Expression] -> String
functionsCall []     = ""
functionsCall [expr]    = showExpression expr ""
functionsCall (expr:es) = showExpression expr "" ++ ", " ++ functionsCall es

showListBlock :: [Expression] -> String -> String
showListBlock [] _          = ""
showListBlock [expr] indent    = indent ++ showExpression expr indent ++ "\n"
showListBlock (expr:es) indent = indent ++ showExpression expr indent ++ ";\n" ++ showListBlock es indent

showExpression :: Expression -> String -> String
showExpression (Number n)                       indent = show n
showExpression (Reference name)                 indent = name
showExpression (Assign name expr)               indent = "let " ++ name ++ " = " ++ showExpression expr indent ++ " tel"
showExpression (BinaryOperation op expr1 expr2) indent = "(" ++ showExpression expr1 indent ++ " " ++ showBinop op ++ " " ++ showExpression expr2 indent ++ ")"
showExpression (UnaryOperation op expr)         indent = showUnop op ++ showExpression expr indent
showExpression (FunctionCall name expr)         indent = name ++ "(" ++ functionsCall expr ++ ")"
showExpression (Conditional cond x y)           indent = "if " ++ showExpression cond indent ++ " then " ++ showExpression x indent ++ " else " ++ showExpression y indent ++ " fi"
showExpression (Block expr)                     indent = "{\n" ++ showListBlock expr (indent ++ "\t") ++ indent ++ "}"

funcDefinitions :: [Name] -> String
funcDefinitions []     = ""
funcDefinitions [name]    = name
funcDefinitions (name:ns) = name ++ ", " ++ funcDefinitions ns

showFunctionDefenition :: FunctionDefinition -> String
showFunctionDefenition (name, varnames, expr) = "func " ++ name ++ "(" ++ funcDefinitions varnames ++ ") = " ++ showExpression expr "" ++ "\n"

showProgram :: Program -> String
showProgram (definitions, expr) = (foldr ((++) . showFunctionDefenition) "" definitions) ++ showExpression expr ""


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

getVar :: State -> Name -> Integer
getVar [] _                                               = 0
getVar ((varName, varValue):state) name | name == varName = varValue
                                        | otherwise       = getVar state name 

getBody :: [FunctionDefinition] -> Name -> Expression
getBody [] _                                                           = Number 0
getBody ((funcName, funcArgs, funcBody):funcs) name | name == funcName = funcBody
                                                    | otherwise        = getBody funcs name 

getFunctionArgs :: [FunctionDefinition] -> Name -> [Name]
getFunctionArgs [] _                                                           = []
getFunctionArgs ((funcName, funcArgs, funcBody):funcs) name | name == funcName = funcArgs
                                                            | otherwise        = getFunctionArgs funcs name 

evalFuncList :: [Expression] -> [Name] -> State -> [FunctionDefinition] -> ([Integer], State)
evalFuncList [_] [] _ _                             = ([0], [])
evalFuncList (_:_:_) [] _ _                         = ([0], [])
evalFuncList [] _ state funcs                       = ([0], state)
evalFuncList [expr] [name] state funcs              = ([fst result], snd result)
                                                      where result = evalExpression expr state funcs
evalFuncList (expr:others) (name:names) state funcs = (fst result:fst next, snd next)
                                                      where result = evalExpression expr state funcs
                                                            next   = evalFuncList others names (snd result) funcs


makeStates :: Expression -> State -> [FunctionDefinition] -> (State, State)
makeStates (FunctionCall name exprs) state funcs = (sstate, fstate)
                                                            where res    = evalFuncList exprs (getFunctionArgs funcs name) state funcs
                                                                  sstate = snd res
                                                                  fstate = zip (getFunctionArgs funcs name) (fst res) ++ sstate
makeStates exp _ _                               = ([], [])

evalBlock :: [Expression] -> State -> [FunctionDefinition] -> (Integer, State)
evalBlock [] state funcs              = (0, state)
evalBlock [expr] state funcs          = evalExpression expr state funcs
evalBlock (expr:commands) state funcs = evalBlock commands (snd (evalExpression expr state funcs)) funcs

evalExpression :: Expression -> State -> [FunctionDefinition] -> (Integer, State)
evalExpression (Number n) state funcs                       = (n, state)
evalExpression (Reference name) state funcs                 = (getVar state name, state)
evalExpression (Assign name expr) state funcs               = (fst result, (name, fst result):snd result)
                                                             where result = evalExpression expr state funcs
evalExpression (BinaryOperation op expr1 expr2) state funcs = (toBinaryFunction op (fst result1) (fst result2), snd result2)
                                                             where result1 = evalExpression expr1 state funcs
                                                                   result2 = evalExpression expr2 (snd result1) funcs 
evalExpression (UnaryOperation op expr) state funcs         = (toUnaryFunction op (fst res), snd res)
                                                             where res = evalExpression expr state funcs
evalExpression (FunctionCall name exprs) state funcs        = (rv, sstate)
                                                             where rv         = fst (evalExpression (getBody funcs name) (snd states) funcs)
                                                                   states = makeStates (FunctionCall name exprs) state funcs
                                                                   sstate     = fst states
evalExpression (Conditional cond x y) state func            | toBool(fst condres)      = evalExpression x (snd condres) func
                                                            | otherwise                = evalExpression y (snd condres) func
                                                             where condres = evalExpression cond state func                                                         
evalExpression (Block commands) state funcs                 = evalBlock commands state funcs

eval :: Program -> Integer
eval (definitions, expr) = fst (evalExpression expr [] definitions)