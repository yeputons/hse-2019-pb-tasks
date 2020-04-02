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
addTab :: String -> String
addTab = unlines . map ('\t':) . lines

{-# ANN module "HLint: ignore Use ++" #-}
{-# ANN module "HLint: ignore Evaluate" #-}
showExpression :: Expression -> String
showExpression (Number n)               = concat [show n]
showExpression (Reference name)         = concat [name]
showExpression (Assign name expr)       = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op l r) = concat ["(", concat [showExpression l, " ", showBinop op, " ", showExpression r], ")"]
showExpression (UnaryOperation op expr) = concat [showUnop op, showExpression expr]
showExpression (FunctionCall name fs)   = concat [name, "(", intercalate ", " $ map showExpression fs, ")"]
showExpression (Conditional expr t f)   = concat ["if ", showExpression expr, " then ", showExpression t, " else ", showExpression f, " fi"]
showExpression (Block fs)               = concat ["{\n", addTab $ intercalate ";\n" $ map showExpression fs, "}"]

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expr, "\n"]

showProgram :: Program -> String
showProgram (fs, expr) = concatMap showFunctionDefinition fs ++ showExpression expr

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

newtype Eval a = Eval ([FunctionDefinition] -> State -> (a, State))  -- Как data, только эффективнее в случае одного конструктора.

runEval :: Eval a -> [FunctionDefinition] -> State -> (a, State)
runEval (Eval f) = f

evaluated :: a -> Eval a  -- Возвращает значение без изменения состояния.
evaluated a = Eval $ \_ st -> (a, st)

readState :: Eval State  -- Возвращает состояние.
readState = Eval $ \_ st -> (st, st)

addToState :: String -> Integer -> a -> Eval a  -- Добавляет/изменяет значение переменной на новое и возвращает константу.
addToState name value a = Eval $ \_ st -> (a, (name, value):st)

readDefs :: Eval [FunctionDefinition]  -- Возвращает все определения функций.
readDefs = Eval $ \fds st -> (fds, st)

andThen :: Eval a -> (a -> Eval b) -> Eval b  -- Выполняет сначала первое вычисление, а потом второе.
andThen ea fe = Eval $ \fds st -> let (eb, newSt) = runEval ea fds st
                                  in  runEval (fe eb) fds newSt 

andEvaluated :: Eval a -> (a -> b) -> Eval b  -- Выполняет вычисление, а потом преобразует результат чистой функцией.
andEvaluated ea f = andThen ea $ \eb -> evaluated $ f eb

-- честно подсмотрел идею у Игоря :)
(&=>) = andThen
(&==) = andEvaluated

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL f a = foldl' ff (evaluated a)
                       where ff ea expr = ea &=> \a -> evalExpression expr &== f a

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression (Number n)                 = evaluated n
evalExpression (Reference name)           = readState &== \st -> fromJust $ lookup name st
evalExpression (Assign name expr)         = evalExpression expr &=> \res -> addToState name res res
evalExpression (BinaryOperation op e1 e2) = evalExpression e1 &=> \a -> evalExpression e2 &== toBinaryFunction op a
evalExpression (UnaryOperation op expr)   = evalExpression expr &== \a -> toUnaryFunction op a
evalExpression (FunctionCall name args)   = let evalArgs = evalExpressionsL (flip (:)) [] args &== reverse
                                                func     = readDefs &== \fdsEv -> fromJust $ find (\(fName, _, _) -> fName == name) fdsEv
                                                fState   = evalArgs &=> \valuesEv -> func &=> \(_, fArgNamesEv, _) -> Eval $ \_ st -> (zip fArgNamesEv valuesEv ++ st, st)
                                                in fState &=> \fStateEv -> func &=> \(_, _, fBodyEv) -> Eval $ \fds st -> (fst $ runEval (evalExpression fBodyEv) fds fStateEv, st)
evalExpression (Conditional c e1 e2)      = evalExpression c &=> \b -> evalExpression $ if toBool b then e1 else e2
evalExpression (Block es)                 = evalExpressionsL (\_ a -> a) 0 es 


-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (fds, expr) = fst $ runEval (evalExpression expr) fds []
