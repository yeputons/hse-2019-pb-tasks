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

-- scopeContains :: State -> Name -> Bool
-- scopeContains []         _     = False
-- scopeContains (sc:xscope) name | (fst sc) == name = True
--                                | otherwise        = scopeContains xscope name 

-- showExpression :: State -> Expression -> String
-- showExpression _          (Number num)       = show num
-- showExpression (sc:xscope) (Reference name)  | (fst sc) == name = show (snd sc)
--                                              | otherwise       = showExpression xscope (Reference name)

-- showExpression scope (Assign name expr) | scopeContains scope name = 

dropLast :: Int -> [a] -> [a]
dropLast n x = take ((length x) - n) x

showArgs :: [String] -> String
showArgs []    = ""
showArgs args  = dropLast 2 . concat $ map (++ ", ") args

addTabs :: String -> String
addTabs []      = []
addTabs (s:str) | s == '\n' = s:'\t':(addTabs str)
                | otherwise = s:addTabs str

showExpression :: Expression -> String
showExpression (Number num)                      = show num
showExpression (Reference name)                  = name
showExpression (Assign name expr)                = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op left right)   = concat ["(", showExpression left, " ", showBinop op, " ", showExpression right, ")"]
showExpression (UnaryOperation op expr)          = concat [showUnop op, showExpression expr]
showExpression (FunctionCall name [])            = concat [name, "()"]
showExpression (FunctionCall name args)          = concat [name, "(", showArgs $ map (showExpression) args, ")"]
showExpression (Conditional expr ifTrue ifFalse) = concat ["if ", showExpression expr, " then ", showExpression ifTrue, " else ", showExpression ifFalse, " fi"]
showExpression (Block [])                        = "{\n}"
showExpression (Block exprs)                     = concat ["{\n\t", addTabs . dropLast 2 . concat $ (map ((++ ";\n") . showExpression) exprs), "\n}"]


showFunction :: FunctionDefinition -> String
showFunction (name, args, expr) = concat ["func ", name, "(", showArgs args, ") = ", showExpression expr]

showProgram :: Program -> String
showProgram (funcs, body) = concat [concat $ map ((++ "\n") . showFunction) funcs, showExpression body]  

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

evalBinop :: Binop -> Integer -> Integer -> Integer
evalBinop Add a b = (+) a b 
evalBinop Mul a b = (*) a b
evalBinop Sub a b = (-) a b
evalBinop Div a b = div a b
evalBinop Mod a b = mod a b
evalBinop Lt a b  = toInteger $ fromEnum $ (<) a b
evalBinop Le a b  = toInteger $ fromEnum $ (<=) a b
evalBinop Gt a b  = toInteger $ fromEnum $ (>) a b
evalBinop Ge a b  = toInteger $ fromEnum $ (>=) a b
evalBinop Eq a b  = toInteger $ fromEnum $ (==) a b
evalBinop Ne a b  = toInteger $ fromEnum $ (/=) a b
evalBinop And _ 0 = 0
evalBinop And 0 _ = 0
evalBinop And _ _ = 1
evalBinop Or 0 0  = 0
evalBinop Or _ _  = 1 

evalUnop :: Unop -> Integer -> Integer
evalUnop Neg a = -a
evalUnop Not 0 = 1
evalUnop Not _ = 0

prepareScopeForFunction :: State -> [FunctionDefinition] -> FunctionDefinition -> [Expression] -> State
prepareScopeForFunction scope funcs (_, [], _)       _     = scope
prepareScopeForFunction scope funcs (fName, name:names, fExpr) (expr:exprs) = prepareScopeForFunction (name, snd value):scope funcs (fName, names, fExpr) exprs
                                                                            where value = evalExpression scope funcs expr

evalExpression :: State -> [FunctionDefinition] -> Expression -> (State, Integer)
evalExpression scope funcs (Number num) = (scope, num)
evalExpression (sc:scope) funcs (Reference name) | (fst sc) == name = (scope, snd sc)
                                                 | otherwise        = evalExpression scope funcs (Reference name)

evalExpression scope funcs (Assign name expr) = ((name, snd value):(fst value), snd value) 
                                              where value = evalExpression scope funcs expr

evalExpression scope funcs (BinaryOperation op left right) = (scope, evalBinop op (snd leftValue) (snd rightValue))
                                                           where leftValue  = evalExpression scope funcs left
                                                                 rightValue = evalExpression scope funcs right 

evalExpression scope funcs (UnaryOperation op expr) = (scope, evalUnop op (snd $ value))
                                                    where value = evalExpression scope funcs expr

-- evalExpression scope ((fName, fArgs, fExpr):funcs) (FunctionCall name args) | fName /= name = evalExpression scope funcs (FunctionCall name args)
--                                                                             | otherwise     = 
--                                                                             where value = eval 

eval :: Program -> Integer
eval (funcs, body) = snd $ evalExpression [] funcs body
