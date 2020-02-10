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

showExpr :: Expression -> String
showExpr (Number val)                            = show val
showExpr (Reference name)                        = name 
showExpr (Assign name expr)                      = concat ["let ", name, " = ", showExpr expr, " tel"]
showExpr (BinaryOperation op leftExpr rightExpr) = concat ["(", showExpr leftExpr, " ", showBinop op, " ", showExpr rightExpr, ")"]
showExpr (UnaryOperation op expr)                = showUnop op ++ showExpr expr
showExpr (FunctionCall name args)                = concat [name, "(", intercalate ", " (map showExpr args), ")"]
showExpr (Conditional e t f)                     = concat ["if ", showExpr e, " then ", showExpr t, " else ", showExpr f, " fi"]
showExpr (Block exprs)                           = concat ["{\n", concatMap (("\t" ++) . (++ "\n")) (lines $ intercalate ";\n" (map showExpr exprs)), "}"]

showFunc :: FunctionDefinition -> String
showFunc (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpr expr]

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (funcs, expr) = concatMap ((++ "\n") . showFunc) funcs ++ showExpr expr

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

evalExprsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExprsL = undefined

evalExpr :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpr = undefined
-} -- Удалите эту строчку, если решаете бонусное задание.

-- Реализуйте eval: запускает программу и возвращает её значение.

getName:: FunctionDefinition -> Name
getName (name, _, _) = name

getArgs :: FunctionDefinition -> [Name]
getArgs (_, args, _) = args

getBody :: FunctionDefinition -> Expression
getBody (_, _, expr) = expr

evalExpr :: State -> [FunctionDefinition] -> Expression -> (State, Integer)

evalExpr state _     (Number val)                            = (state, val)
evalExpr state _     (Reference name)                        = (state, snd $ fromJust $ find ((== name) . fst) state)
evalExpr state funcs (Assign name expr)                      = ((name, val) : newState, val)
                                                                  where (newState, val) = evalExpr state funcs expr
evalExpr state funcs (BinaryOperation op leftExpr rightExpr) = (rightState, toBinaryFunction op leftVal rightVal)
                                                                  where (leftState, leftVal)     = evalExpr state funcs leftExpr
                                                                        (rightState, rightVal)   = evalExpr (union state leftState) funcs rightExpr
evalExpr state funcs (UnaryOperation op expr)                = (newState, toUnaryFunction op val)
                                                                  where (newState, val) = evalExpr state funcs expr
evalExpr state funcs (FunctionCall name args)                = (newState, snd $ evalExpr newState funcs (getBody func))
                                                                  where
                                                                      newState = zip (getArgs func) (map (snd . evalExpr state funcs) args) ++ fst (evalExpr state funcs (Block args))
                                                                      func     = fromJust $ find ((== name) . getName) funcs
evalExpr state funcs (Conditional e t f)                     | toBool cond = evalExpr newState funcs t
                                                             | otherwise   = evalExpr newState funcs f
                                                                  where (newState, cond) = evalExpr state funcs e
evalExpr state funcs (Block exprs)                           = foldl (\(st, val) expr -> evalExpr st funcs expr) (state, 0) exprs


eval :: Program -> Integer
eval (funcs, expr) = snd $ evalExpr [] funcs expr
