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
addTabs []      = []
addTabs (s:str) | s == '\n' = s:'\t':addTabs str
                | otherwise = s:addTabs str

showExpression :: Expression -> String
showExpression (Number x)                       = show x
showExpression (Reference name)                 = name 
showExpression (Assign name expr)               = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op expr1 expr2) = concat ["(", showExpression expr1, " ", showBinop op, " ", showExpression expr2, ")"]
showExpression (UnaryOperation op expr)         = showUnop op ++ showExpression expr
showExpression (FunctionCall name args)         = concat [name, "(", intercalate ", " $ map showExpression args, ")"]
showExpression (Conditional cond expr1 expr2)   = concat ["if ", showExpression cond, " then ", showExpression expr1, " else ", showExpression expr2, " fi"]
showExpression (Block [])                       = "{\n}"
showExpression (Block exprs)                    = concat ["{\n\t", addTabs $ intercalate ";\n" $ map showExpression exprs, "\n}"]

showFunc :: FunctionDefinition -> String
showFunc (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expr]

showProgram :: Program -> String
showProgram (funcs, exprs) = concatMap ((++ "\n") . showFunc) funcs ++ showExpression exprs  

-- Верните текстовое представление программы (см. условие).
--showProgram :: Program -> String
--showProgram = undefined

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
--eval :: Program -> Integer
--eval = undefined


getVariable :: State -> Name -> Integer
getVariable [] _                             = 0
getVariable ((varName, varValue):scope) name | name == varName = varValue
                                             | otherwise       = getVariable scope name 


getFuncBody :: [FunctionDefinition] -> Name -> Expression
getFuncBody [] _                                        = Number 0
getFuncBody ((funcName, funcArgs, funcBody):funcs) name | name == funcName = funcBody
                                                            | otherwise    = getFuncBody funcs name 

getFuncArgs :: [FunctionDefinition] -> Name -> [Name]
getFuncArgs [] _                                                           = []
getFuncArgs ((funcName, funcArgs, funcBody):funcs) name | name == funcName = funcArgs
                                                            | otherwise    = getFuncArgs funcs name 

evalFunc :: [Expression] -> [Name] -> State -> [FunctionDefinition] -> ([Integer], State)
evalFunc [_] [] _ _                             = ([0], [])
evalFunc (_:_:_) [] _ _                         = ([0], [])
evalFunc [] _ scope funcs                       = ([0], scope)
evalFunc [expr] [name] scope funcs              = ([resultInt], resultState)
                                                   where (resultInt, resultState) = evalExpression expr scope funcs
evalFunc (expr:others) (name:names) scope funcs = (resultInt:nextInt, nextState)
                                                   where (resultInt, resultState) = evalExpression expr scope funcs
                                                         (nextInt, nextState)     = evalFunc others names resultState funcs


makeScopeForFunction :: Expression -> State -> [FunctionDefinition] -> (State, State)
makeScopeForFunction (FunctionCall name exprs) scope funcs = (sscope, fscope)
                                                            where res    = evalFunc exprs (getFuncArgs funcs name) scope funcs
                                                                  sscope = snd res
                                                                  fscope = zip (getFuncArgs funcs name) (fst res) ++ sscope
makeScopeForFunction exp _ _                               = ([], [])


evalChainBlock :: [Expression] -> State -> [FunctionDefinition] -> (Integer, State)
evalChainBlock [] scope funcs              = (0, scope)
evalChainBlock [expr] scope funcs          = evalExpression expr scope funcs
evalChainBlock (expr:commands) scope funcs = evalChainBlock commands (snd (evalExpression expr scope funcs)) funcs


evalExpression :: Expression -> State -> [FunctionDefinition] -> (Integer, State)
evalExpression (Number n) scope funcs                       = (n, scope)
evalExpression (Reference name) scope funcs                 = (getVariable scope name, scope)
evalExpression (Assign name expr) scope funcs               = (resultInt, (name, resultInt):resultState)
                                                             where (resultInt, resultState) = evalExpression expr scope funcs
evalExpression (BinaryOperation op expr1 expr2) scope funcs = (toBinaryFunction op (fst result1) (fst result2), snd result2)
                                                             where result1 = evalExpression expr1 scope funcs
                                                                   result2 = evalExpression expr2 (snd result1) funcs
evalExpression (UnaryOperation op expr) scope funcs         = (toUnaryFunction op (fst result), snd result)
                                                             where result = evalExpression expr scope funcs
evalExpression (FunctionCall name exprs) scope funcs        = (expr, sscope)
                                                             where expr       = fst (evalExpression (getFuncBody funcs name) fscope funcs)
                                                                   new_scopes = makeScopeForFunction (FunctionCall name exprs) scope funcs
                                                                   fscope     = snd new_scopes
                                                                   sscope     = fst new_scopes
evalExpression (Conditional e t f) scope funcs              | toBool(fst res)          = evalExpression t (snd res) funcs
                                                            | otherwise                = evalExpression f (snd res) funcs
                                                             where res = evalExpression e scope funcs
evalExpression (Block exprs) scope funcs                    = foldl (\(int, state) e -> evalExpression e state funcs) (0, scope) exprs


eval :: Program -> Integer
eval (definitions, expr) = fst (evalExpression expr [] definitions)