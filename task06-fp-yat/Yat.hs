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

showExprList :: String -> [Expression] -> String
showExprList x = intercalate x . map showExpr
--showExprList []     _     = []
--showExprList [last] delim = [showExpr last]
--showExprList (e:es) delim = (showExpr e ++ delim):showExprList es delim

relines = intercalate "\n" --like unlines, but withot trailing \n

linemap f = unlines . map f . lines

showExpr :: Expression -> String
showExpr (Number n)               = show n
showExpr (Reference x)            = x
showExpr (Assign n e)             = "let " ++ n ++ " = " ++ showExpr e ++ " tel"
showExpr (BinaryOperation op l r) = "(" ++ showExpr l ++ " " ++ showBinop op ++ " " ++ showExpr r ++ ")"
showExpr (UnaryOperation op e)    = showUnop op ++ showExpr e
showExpr (Conditional e t f)      = "if " ++ showExpr e ++ " then " ++ showExpr t ++ " else " ++ showExpr f ++ " fi"
showExpr (Block [])               = "{\n}" -- General case results in extra \n
showExpr (Block es)               = "{\n" ++ (linemap ('\t':) $ showExprList ";\n" es) ++ "}"
showExpr (FunctionCall n es)      = n ++ "(" ++ showExprList "," es ++ ")"

showFunDecl :: FunctionDefinition -> String
showFunDecl (n, ps, e) = "func " ++ n ++ "(" ++ intercalate "," ps ++ ") = " ++ showExpr e

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (fs, e) = relines $ map showFunDecl fs ++ [showExpr e]

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
evaluated x = Eval $ \_ s -> (x, s)

readState :: Eval State  -- Возвращает состояние.
readState = Eval $ \_ s -> (s, s)

addToState :: String -> Integer -> a -> Eval a  -- Добавляет/изменяет значение переменной на новое и возвращает константу.
addToState n v a = Eval $ \_ s -> (a, (n,v):s)

readDefs :: Eval [FunctionDefinition]  -- Возвращает все определения функций.
readDefs = Eval (,)

andThen :: Eval a -> (a -> Eval b) -> Eval b  -- Выполняет сначала первое вычисление, а потом второе.
andThen cur next = Eval $ \fs s -> let (a, s') = runEval cur fs s 
                                   in runEval (next a) fs s'

(~>) = andThen

andEvaluated :: Eval a -> (a -> b) -> Eval b  -- Выполняет вычисление, а потом преобразует результат чистой функцией.
andEvaluated cur next = cur ~> (evaluated . next)

(~@) = andEvaluated

copyState :: Eval a -> Eval a
copyState f = Eval $ \fs s -> let (a, _) = runEval f fs s in (a, s)

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL f x = foldl (\acc e -> acc ~@ f ~> (e ~@)) (evaluated x) . map evalExpression


select :: String -> (a -> String) -> [a] -> a
select n f = fromJust . find ((n ==) . f)

readFromState :: String -> State -> Integer
readFromState n = snd . select n fst

selectFunction :: String -> [FunctionDefinition] -> FunctionDefinition
selectFunction n = select n (\(x, _, _) -> x)

withParams :: Eval a -> [Name] -> [Integer] -> Eval a
withParams e n v = copyState $ foldl (~>) (evaluated ()) (zipWith addToState n v) ~> const e

evalFunction :: FunctionDefinition -> [Integer] -> Eval Integer
evalFunction (f, n, e) = withParams (evalExpression e) n

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression (Number          n     ) = evaluated n
evalExpression (Reference       n     ) = readState ~@ readFromState n
evalExpression (Assign          n  e  ) = evalExpression e ~> \v -> addToState n v v
evalExpression (BinaryOperation op l r) = evalExpression l ~> \a -> evalExpression r ~@ toBinaryFunction op a
evalExpression (UnaryOperation  op e  ) = evalExpression e ~@ toUnaryFunction op
evalExpression (Conditional     e  t f) = evalExpression e ~> \r -> evalExpression $ if toBool r then t else f
evalExpression (Block           es    ) = evalExpressionsL (curry snd) 0 es
evalExpression (FunctionCall n  as    ) = readDefs ~@ selectFunction n
                                          ~> \f -> evalExpressionsL (flip (:)) [] as
                                          ~> evalFunction f

-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (fs, e) = fst $ runEval (evalExpression e) fs []