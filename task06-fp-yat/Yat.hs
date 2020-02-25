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

showFunction :: FunctionDefinition -> String
showFunction (name, params, body) = "func " ++ name ++ "(" ++ intercalate ", " params ++ ") = " ++ showExpression body ++ "\n"

showExpression :: Expression -> String
showExpression (Number num)                     = show num
showExpression (Reference name)                 = name
showExpression (Assign name expression)         = "let " ++ name ++ " = " ++ showExpression expression ++ " tel"
showExpression (BinaryOperation op expr1 expr2) = "(" ++ showExpression expr1 ++ " " ++ showBinop op ++ " " ++ showExpression expr2 ++ ")"
showExpression (UnaryOperation op expr)         = showUnop op ++ showExpression expr
showExpression (FunctionCall name exprs)        = name ++ "(" ++ intercalate ", " (map showExpression exprs) ++ ")"
showExpression (Conditional cond expr1 expr2)   = "if " ++ showExpression cond ++ " then " ++ showExpression expr1 ++ " else " ++ showExpression expr2 ++ " fi"
showExpression (Block exprs)                    = "{" ++ concatMap ("\n\t" ++) (lines (intercalate ";\n" (map showExpression exprs))) ++ "\n}"

showProgram :: Program -> String
showProgram (functions, expression) = concatMap showFunction functions ++ showExpression expression

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

evalExpr :: [FunctionDefinition] -> State -> Expression -> (State, Integer)
evalExpr functions scope (Number num)                                     = (scope, num) 
evalExpr functions scope (Reference name)                                 = (scope, snd $ fromJust $ find ((== name) . fst) scope)
evalExpr functions scope (Assign name expr)                               = ((name, val) : state, val)
                                                                            where (state, val) = evalExpr functions scope expr
evalExpr functions scope (BinaryOperation op left right)                  = (state2, toBinaryFunction op val1 val2)
                                                                            where (state1, val1) = evalExpr functions scope left
                                                                                  (state2, val2) = evalExpr functions state1 right
evalExpr functions scope (UnaryOperation op expr)                         = (state, toUnaryFunction op val) 
                                                                            where (state, val) = evalExpr functions scope expr
evalExpr functions scope  (FunctionCall name args)                        = (scope', snd $ evalExpr functions fScope fBody)
                                                                            where (scope', valArgs)  = foldl (\(state, vals) expr -> let (newScope, val) = evalExpr functions scope expr in (newScope, val : vals)) (scope, []) args
                                                                                  (_ , fArgs, fBody) = fromJust $ find ((== name) . (\(x, _, _) -> x)) functions
                                                                                  fScope             = zip fArgs valArgs ++ scope'
evalExpr functions scope (Conditional expr true false) | toBool res       = evalExpr functions state true
                                                       | otherwise        = evalExpr functions state false
                                                       where (state, res) = evalExpr functions scope expr
evalExpr functions scope (Block exprs)                                    = foldl (\(res, _) expr -> evalExpr functions res expr) (scope, 0) exprs

eval :: Program -> Integer
eval (funcs, expr) = snd $ evalExpr funcs [] expr