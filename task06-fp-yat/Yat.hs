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

showExpression :: Expression -> String
showExpression (Number n)                 = show n
showExpression (Reference n)              = n 
showExpression (Assign name e)            = "let " ++ name ++ " = " ++ showExpression e ++ " tel" 
showExpression (BinaryOperation bi e1 e2) = "(" ++ showExpression e1 ++ " " ++ showBinop bi ++ " " ++ showExpression e2 ++ ")"
showExpression (UnaryOperation un n)      = showUnop un ++ showExpression n
showExpression (FunctionCall name es)     = name ++ showParams (map showExpression es)
showExpression (Conditional cnd i e)      = "if " ++ showExpression cnd ++ " then " ++ showExpression i ++ " else " ++ showExpression e ++ " fi"
showExpression (Block [])                 = "{\n}"
showExpression (Block es)                 = "{\n" ++ (intercalate "\n" . map ("\t" ++) . lines . intercalate ";\n" . map showExpression) es ++ "\n}"


showParams :: [Name] -> String
showParams []  = "()"
showParams [n] = "(" ++ n ++ ")"
showParams ns  = "(" ++ intercalate ", " (map show ns) ++ ")"

fst3 :: (a, b, c) -> a
fst3 (a, _, _ ) = a
snd3 :: (a, b, c) -> b
snd3 (_, b, _) = b
thd3 :: (a, b, c) -> c
thd3 (_, _, c) = c

showFunctionDef :: FunctionDefinition -> String
showFunctionDef fd = "func " ++ fst3 fd ++ showParams (snd3 fd) ++ " = " ++ showExpression (thd3 fd)
 
-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram prog = concatMap (("\n" ++ ) . showFunctionDef) (fst prog) ++ showExpression (snd prog)

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
evaluated val = Eval (\_ state -> (val, state))

readState :: Eval State  -- Возвращает состояние.
readState = Eval (\_ state -> (state, state))


addToState :: String -> Integer -> a -> Eval a  -- Добавляет/изменяет значение переменной на новое и возвращает константу.
addToState name val a = Eval (\_ state -> (a, ((:) (name, val) . filter ((not.(==) name ) . fst)) state))


readDefs :: Eval [FunctionDefinition]  -- Возвращает все определения функций.
readDefs = Eval (\ fds state -> (fds, state))

andThen :: Eval a -> (a -> Eval b) -> Eval b  -- Выполняет сначала первое вычисление, а потом второе.
andThen evl f = Eval (\ fds state -> let res = runEval evl fds state in runEval (f (fst res)) fds (snd res))

andEvaluated :: Eval a -> (a -> b) -> Eval b  -- Выполняет вычисление, а потом преобразует результат чистой функцией.
andEvaluated evl f = Eval (\ fds state -> let res = runEval evl fds state in (f (fst res), snd res))

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL f ini = foldl (apply' f) (evaluated ini) . map evalExpression

apply' :: (a -> b -> a) -> Eval a -> Eval b -> Eval a
apply' f ea eb = andThen (andEvaluated ea f) (andEvaluated eb)

getValue :: String -> State -> Integer
getValue str state = fromMaybe 0 $ lookup str state 

runWithNewState :: Eval a -> Eval a
runWithNewState evl = Eval (\fds state -> let res = runEval evl fds state in (fst res, state))

getArgs :: [Expression] -> Eval [Integer]
getArgs = evalExpressionsL (flip (:)) []

addToStateL :: [Name] -> [Integer] -> a -> Eval a
addToStateL names ints a = foldl andThen (evaluated a) (zipWith addToState names ints)


evalFunction' :: Eval [Integer] -> FunctionDefinition -> Eval Integer
evalFunction' ei fd = ei `andThen` evalFunction'' fd
evalFunction'' :: FunctionDefinition -> [Integer] -> Eval Integer
evalFunction'' (n, params, expr) ints = runWithNewState (addToStateL params ints () `andThen` const (evalExpression expr)) 


evalFunction :: String -> [Expression] -> Eval [FunctionDefinition] -> Eval Integer
evalFunction nm exps fds = fds `andEvaluated` getFunction nm `andThen` evalFunction' (getArgs exps)




getFunction :: String -> [FunctionDefinition] -> FunctionDefinition
getFunction nm fds = fromMaybe ("", [], Number 0) (find ((==) nm . fst3) fds)

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression (Number n)                 = evaluated n 
evalExpression (Reference nm)             = andEvaluated readState (getValue nm)
evalExpression (Assign nm val)            = andThen (evalExpression val) (\ res -> addToState nm res res)
evalExpression (BinaryOperation bo e1 e2) = andThen (evalExpression e1) (andEvaluated (evalExpression e2) . toBinaryFunction bo)
evalExpression (UnaryOperation uo e1)     = andEvaluated (evalExpression e1) (toUnaryFunction uo)
evalExpression (Conditional cond e1 e2)   = andThen (evalExpression cond) (\ res -> if res /= 0 then evalExpression e1 else evalExpression e2) 
evalExpression (FunctionCall nm elist)    = evalFunction nm elist readDefs
evalExpression (Block es)                 = evalExpressionsL (flip const) 0 es
-- Реализуйте eval: запускает программу и возвращает её значение.


eval :: Program -> Integer
eval (fds, mn) = fst (runEval (evalExpression mn) fds [])
eval' :: Program -> (Integer, State)
eval' (fds, mn) = runEval (evalExpression mn) fds []
