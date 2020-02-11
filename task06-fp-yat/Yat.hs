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

-- Тут будет что-то происходить

showExpression :: Expression -> String

showExpression (Number number)                                    = show number
showExpression (Reference name)                                   = name
showExpression (Assign name expression)                           = concat ["let ", name, " = ", showExpression expression, " tel"]
showExpression (BinaryOperation binop lExpression rExpression)    = concat ["(", showExpression lExpression, " ", showBinop binop, " ", showExpression rExpression, ")"]
showExpression (UnaryOperation unop expression )                  = concat [showUnop unop, showExpression expression]
showExpression (FunctionCall functname args)                      = concat [functname, "(", intercalate ", " (map showExpression args), ")"] -- побоялась здесь вместо скобок $ поставить... Хотя вроде как работало..
showExpression (Conditional expression happyPath sadPath)         = concat ["if ", showExpression expression, " then ", showExpression happyPath, " else ", showExpression sadPath, " fi"] -- вроде как эти термины были не совсем про это, но они такие классные ^^
showExpression (Block [])                                         = "{\n}"
showExpression (Block expressions)                                = concat ["{\n\t", addSpace $ intercalate ";\n" $ map showExpression expressions, "\n}"]
                                                                               where addSpace []                 = []
                                                                                     addSpace (x:xs) | x == '\n' = x:'\t':addSpace xs
                                                                                                     | otherwise = x:addSpace xs

showFunction :: FunctionDefinition -> String

showFunction (name, args, expression) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expression]

showProgram :: Program -> String
showProgram (functs, body) = concatMap ((++ "\n") . showFunction) functs ++ showExpression body 

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

getVariable :: State -> Name -> Integer

getVariable [] _                                                              = 0
getVariable ((variableName, variableValue):scope) name | name == variableName = variableValue
                                                       | otherwise            = getVariable scope name


getFunctionDefinition :: Name -> [FunctionDefinition] -> ([Name], Expression)

getFunctionDefinition name funcs = argsWithoutFst (head (filter (isEq name) funcs)) 
                             where isEq name (n, names, e)    = name == n
                                   argsWithoutFst (n, name, e)= (name, e)

makeFunctionScope :: State -> [Name] -> [Integer] -> State

makeFunctionScope scope parameters values = zip parameters values ++ scope


chainReaction :: [FunctionDefinition] -> State -> [Expression] -> ([Integer], State)

chainReaction funcs scope []         = ([], scope)
chainReaction funcs scope (arg:args) = (fst argresult:fst argsresult, snd argsresult)
                                      where argresult  = evalExpression  funcs scope arg
                                            argsresult = chainReaction funcs (snd argresult) args -- Ну... Мне так больше нравится (они же в действительности так тянут за собой)


evalExpression :: [FunctionDefinition] -> State -> Expression -> (Integer, State)

evalExpression funcs scope (Number number)                                              = (number, scope)
evalExpression funcs scope (Reference name)                                             = (getVariable scope name, scope)
evalExpression funcs scope (Assign name expression)                                     = (fst res, var:snd res)
                                                                                         where res = evalExpression funcs scope expression
                                                                                               var = (name, fst res)
                                                       
evalExpression funcs scope (BinaryOperation binop lExpression rExpression)              = (toBinaryFunction binop (fst lres) (fst rres), snd rres)
                                                                                                                 where lres = evalExpression funcs scope lExpression
                                                                                                                       rres = evalExpression funcs (snd lres) rExpression

evalExpression funcs scope (UnaryOperation unop expression)                             = (toUnaryFunction unop (fst res), snd res)
                                                                                                               where res = evalExpression funcs scope expression

evalExpression funcs scope (FunctionCall functname args)                                = (fst (evalExpression funcs (makeFunctionScope (snd res) (fst func) (fst res)) (snd func)), snd res) 
                                                                                                         where func = getFunctionDefinition functname funcs
                                                                                                               res = chainReaction funcs scope args
evalExpression funcs scope (Conditional expression happyPath sadPath) | toBool (fst er) = hp
                                                                      | otherwise       = sp
                                                                              where er = evalExpression funcs scope expression
                                                                                    hp = evalExpression funcs (snd er) happyPath
                                                                                    sp = evalExpression funcs (snd er) sadPath

evalExpression funcs scope (Block [])                                                   = (0, scope)
evalExpression funcs scope (Block [expressions])                                        = evalExpression funcs scope expressions                                      
evalExpression funcs scope (Block (expr:exprs))                                         = evalExpression funcs (snd (evalExpression funcs scope expr)) (Block exprs)


eval :: Program -> Integer
eval program = fst (evalExpression (fst program) [] (snd program))
