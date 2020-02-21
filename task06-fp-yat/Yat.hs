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

showExpression :: Expression -> String
showExpression (Number n)               = show n
showExpression (Reference name)         = name
showExpression (Assign name expr)       = unwords ["let", name, "=", showExpression expr, "tel"]
showExpression (BinaryOperation op l r) = concat ["(", unwords [showExpression l, showBinop op, showExpression r], ")"]
showExpression (UnaryOperation op expr) = showUnop op ++ showExpression expr
showExpression (FunctionCall name fs)   = concat [name, "(", intercalate ", " (map showExpression fs), ")"]
showExpression (Conditional expr t f)   = unwords ["if", showExpression expr, "then", showExpression t, "else", showExpression f, "fi"]
showExpression (Block fs)               = concat ["{", "\n", addTab $ block' fs, "}"]
                                          where block' []     = ""
                                                block' [f]    = showExpression f
                                                block' (f:fs) = concat [showExpression f, ";", "\n", block' fs]

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

-- {- -- Удалите эту строчку, если решаете бонусное задание.
newtype Eval a = Eval ([FunctionDefinition] -> State -> (a, State))  -- Как data, только эффективнее в случае одного конструктора.

runEval :: Eval a -> [FunctionDefinition] -> State -> (a, State)
runEval (Eval f) = f

evaluated :: a -> Eval a  -- Возвращает значение без изменения состояния.
evaluated a = Eval (\_ st -> (a, st))

readState :: Eval State  -- Возвращает состояние.
readState = Eval (\_ st -> (st, st))

addToState :: String -> Integer -> a -> Eval a  -- Добавляет/изменяет значение переменной на новое и возвращает константу.
addToState name value a = Eval (\_ st -> (a, (name, value):st))

readDefs :: Eval [FunctionDefinition]  -- Возвращает все определения функций.
readDefs = Eval readDefs'
           where readDefs' fds st = (fds, st)

andThen :: Eval a -> (a -> Eval b) -> Eval b  -- Выполняет сначала первое вычисление, а потом второе.
andThen ea fe = Eval $ \fds st -> let (eb, newSt) = runEval ea fds st
                                  in runEval (fe eb) fds newSt 

andEvaluated :: Eval a -> (a -> b) -> Eval b  -- Выполняет вычисление, а потом преобразует результат чистой функцией.
andEvaluated ea f = Eval andEvaluated'
                    where andEvaluated' fds st = first f $ runEval ea fds st

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL _ a []     = Eval evalExpressionsL' 
                              where evalExpressionsL' _ st = (a, st)
evalExpressionsL f a (e:es) = Eval evalExpressionsL'
                              where evalExpressionsL' fds st = runEval (evalExpressionsL f newA es) fds newSt
                                                               where newA          = f a valE
                                                                     (valE, newSt) = runEval (evalExpression e) fds st

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression (Number    n   )           = evaluated n
evalExpression (Reference name)           = Eval evalExpression'
                                            where evalExpression' _ st = (snd $ fromJust $ find (\(x, _) -> x == name) st, st)

evalExpression (Assign    name expr)      = Eval evalExpression'
                                            where evalExpression' fds st = runEval (addToState name valE valE) fds newSt
                                                                           where (valE, newSt) = runEval (evalExpression expr) fds st
evalExpression (BinaryOperation op e1 e2) = Eval evalExpression'
                                            where evalExpression' fds st = (binF valE1 valE2, newSt2)
                                                                           where binF            = toBinaryFunction op
                                                                                 (valE1, newSt1) = runEval          (evalExpression e1) fds st
                                                                                 (valE2, newSt2) = runEval          (evalExpression e2) fds newSt1
evalExpression (UnaryOperation op expr)   = Eval evalExpression'
                                            where evalExpression' fds st = (unF valE, newSt)
                                                                           where unF  = toUnaryFunction op
                                                                                 (valE, newSt) = runEval (evalExpression expr) fds st
evalExpression (FunctionCall name args)   = Eval evalExpression'
                                            where evalExpression' fds st = (fRet, newSt)
                                                                           where (fRet, _)                              = runEval (evalExpression fBody) fds fState
                                                                                 (_, fArgNames, fBody)                  = fromJust $ find (\(x,_,_) -> x == name) fds
                                                                                 (fState, newSt)                        = fromJust $ extendState fArgNames args st
                                                                                 extendState [] []                   st = Just (st, st)
                                                                                 extendState [] _                    _  = Nothing
                                                                                 extendState _  []                   _  = Nothing
                                                                                 extendState (name:names) (arg:args) st = Just (snd $ runEval (addToState name valE 0) fds fState', newSt')
                                                                                                                          where (valE, tmpSt)     = runEval (evalExpression arg) fds st
                                                                                                                                (fState', newSt') = fromJust $ extendState names args tmpSt
evalExpression (Conditional c e1 e2)      = Eval evalExpression'
                                            where evalExpression' fds st = if toBool valC then valE1 else valE2
                                                                           where (valC, newSt)  = runEval (evalExpression c)  fds st
                                                                                 valE1          = runEval (evalExpression e1) fds newSt
                                                                                 valE2          = runEval (evalExpression e2) fds newSt

evalExpression (Block es)                 = Eval evalExpression'
                                            where evalExpression' = runEval (evalExpressionsL (\_ a -> a) 0 es) 

-- -} -- Удалите эту строчку, если решаете бонусное задание.

-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (fds, expr) = fst $ runEval (evalExpression expr) fds []
