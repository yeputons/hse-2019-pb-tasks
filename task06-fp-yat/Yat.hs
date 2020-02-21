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

addTabs :: String -> String
addTabs []      = []
addTabs (s:str) | s == '\n' = s:'\t':addTabs str
                | otherwise = s:addTabs str

showExpression :: Expression -> String
showExpression (Number n)                      = show n
showExpression (Reference name)                = name
showExpression (Assign name expr)              = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op left right) = concat ["(", showExpression left, " ", showBinop op, " ", showExpression right, ")"]
showExpression (UnaryOperation op expr)        = showUnop op ++ showExpression expr
showExpression (FunctionCall name args)        = concat [name, "(", intercalate ", " (map showExpression args), ")"]
showExpression (Conditional expr ifT ifF)      = concat ["if ", showExpression expr, " then ", showExpression ifT, " else ", showExpression ifF, " fi"]
showExpression (Block [])                      = "{\n}"
showExpression (Block exprs)                   = concat ["{\n\t", addTabs $ intercalate ";\n" $ map showExpression exprs, "\n}"]


showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expr]

showProgram :: Program -> String
showProgram (funcs, body) = concatMap ((++ "\n") . showFunctionDefinition) funcs ++ showExpression body 

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

--{- -- Удалите эту строчку, если решаете бонусное задание.
newtype Eval a = Eval ([FunctionDefinition] -> State -> (a, State))  -- Как data, только эффективнее в случае одного конструктора.

runEval :: Eval a -> [FunctionDefinition] -> State -> (a, State)
runEval (Eval f) = f

evaluated :: a -> Eval a  -- Возвращает значение без изменения состояния.
evaluated a = Eval $ \_ state -> (a, state)

readState :: Eval State  -- Возвращает состояние.
readState = Eval $ \_ state -> (state, state)

addToState :: String -> Integer -> a -> Eval a  -- Добавляет/изменяет значение переменной на новое и возвращает константу.
addToState name val a = Eval $ \_ state -> (a, (name, val) : state)

readDefs :: Eval [FunctionDefinition]  -- Возвращает все определения функций.
readDefs = Eval $ \funcs state -> (funcs, state)

andThen :: Eval a -> (a -> Eval b) -> Eval b  -- Выполняет сначала первое вычисление, а потом второе.
andThen f1 f2 = Eval $ \fs state -> let (f1_result, new_state) = runEval f1 fs state 
                                    in runEval (f2 f1_result) fs new_state

(~>) = andThen

andEvaluated :: Eval a -> (a -> b) -> Eval b  -- Выполняет вычисление, а потом преобразует результат чистой функцией.
andEvaluated cur next = cur ~> (evaluated . next)

(~~>) = andEvaluated

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL f x = foldl (\acc e -> acc ~~> f ~> (e ~~>)) (evaluated x) . map evalExpression

copyState :: Eval a -> Eval a
copyState f = Eval $ \fs s -> let (a, _) = runEval f fs s in (a, s)

getValue :: String -> State -> Integer
getValue str state = fromMaybe 0 $ lookup str state

select :: String -> (a -> String) -> [a] -> a
select n f = fromJust . find ((n ==) . f)

readFromState :: String -> State -> Integer
readFromState name = snd . select name fst

selectFunction :: String -> [FunctionDefinition] -> FunctionDefinition
selectFunction name = select name (\(x, _, _) -> x)

withParams :: Eval a -> [Name] -> [Integer] -> Eval a
withParams expr name v = copyState $ foldl (~>) (evaluated ()) (zipWith addToState name v) ~> const expr

evalFunction :: FunctionDefinition -> [Integer] -> Eval Integer
evalFunction (f, name, expr) = withParams (evalExpression expr) $ reverse name


evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression (Number          n)              = evaluated n
evalExpression (Reference       name)           = readState ~~> (getValue name)
evalExpression (Assign          name  expr)     = evalExpression expr ~> \v -> addToState name v v
evalExpression (BinaryOperation op left right)  = evalExpression left ~> \a -> evalExpression right ~~> toBinaryFunction op a
evalExpression (UnaryOperation  op expr)        = evalExpression expr ~~> toUnaryFunction op
evalExpression (Conditional     c ifT ifF)      = evalExpression c ~> \a -> evalExpression $ if toBool a then ifT else ifF
evalExpression (Block           exprs)          = evalExpressionsL (curry snd) 0 exprs 

evalExpression (FunctionCall    name args)      = readDefs ~~> selectFunction name
                                                  ~> \f -> evalExpressionsL (flip (:)) [] args
                                                  ~> evalFunction f
-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (fds, expr) = fst $ runEval (evalExpression expr) fds []
