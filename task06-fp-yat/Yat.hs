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
showProgram :: Program -> String
showProgram ([]      , expr) = showExpression expr
showProgram (funcDefs, expr) = showFunctionDefinition (head funcDefs) ++ showProgram (tail funcDefs, expr)

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, args, expr) = "func " ++ name ++ "(" ++ showArgs args ++ ") = " ++ showExpression expr ++ "\n"
                                          where showArgs []     = ""
                                                showArgs [x]    = x
                                                showArgs (x:xs) = x ++ ", " ++ showArgs xs

showExpression :: Expression -> String
showExpression expr = showExpression' expr ""

showExpression' :: Expression -> String -> String
showExpression' (Number n)                       offset = show n
showExpression' (Reference name)                 offset = name
showExpression' (Assign name expr)               offset = "let " ++ name ++ " = " ++ showExpression' expr offset ++ " tel"
showExpression' (BinaryOperation op expr1 expr2) offset = "(" ++ showExpression' expr1 offset ++ " " ++ showBinop op ++ " " ++ showExpression' expr2 offset ++ ")"
showExpression' (UnaryOperation op expr)         offset = showUnop op ++ showExpression expr
showExpression' (FunctionCall name exprs)        offset = name ++ "(" ++ concatMap (`showExpression'` offset) exprs ++ ")"
showExpression' (Conditional expr1 expr2 expr3)  offset = "if " ++ showExpression' expr1 offset ++ " then " ++ showExpression' expr2 offset ++ " else " ++ showExpression' expr3 offset ++ " fi"
showExpression' (Block exprs)                    offset = "{\n" ++ showBlock exprs (offset ++ "\t") ++ offset ++ "}" 

showBlock :: [Expression] -> String -> String
showBlock []     _      = ""
showBlock [x]    offset = offset ++ showExpression' x offset ++ "\n"
showBlock (x:xs) offset = offset ++ showExpression' x offset ++ ";\n" ++ showBlock xs offset

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
eval :: Program -> Integer
eval (funcDefs, expr) = snd (eval' funcDefs expr [])

eval' :: [FunctionDefinition] -> Expression -> State -> (State, Integer)
eval' funcDefs (Number n)                        state = (state, n)
eval' funcDefs (Reference name)                  state = (state, findRef state name)
eval' funcDefs (Assign name expr)                state = first ((:) (name, snd evaluated)) evaluated
                                                       where evaluated = eval' funcDefs expr state
eval' funcDefs (BinaryOperation op l r)          state = second (toBinaryFunction op $ snd evaluated) (eval' funcDefs r $ fst evaluated)
                                                       where evaluated = eval' funcDefs l state
eval' funcDefs (UnaryOperation op expr)          state = second (toUnaryFunction op) (eval' funcDefs expr state)
eval' funcDefs (FunctionCall name exprs)         state = (retState, retValue)
                                                       where retValue      = snd $ eval' funcDefs getFuncExpr makeFuncState
                                                             getFuncExpr   = (\(a, b, c) -> c) $ findFunc funcDefs name
                                                             getFuncNames  = (\(a, b, c) -> b) $ findFunc funcDefs name
                                                             makeFuncState = eval'' funcDefs exprs getFuncNames state
                                                             retState      = fst (eval' funcDefs (Block exprs) state)
eval' funcDefs (Conditional e t f)   state = if toBool $ snd $ eval' funcDefs e state then 
                                                    eval' funcDefs t $ fst $ eval' funcDefs e state
                                             else
                                                    eval' funcDefs f $ fst $ eval' funcDefs e state
eval' funcDefs (Block []     )                   state = (state, 0)
eval' funcDefs (Block [e]    )                   state = eval' funcDefs e state
eval' funcDefs (Block (e:xpr))                   state = eval' funcDefs (Block xpr) (fst (eval' funcDefs e state))

eval'' :: [FunctionDefinition] -> [Expression] -> [Name] -> State -> State
eval'' funcDefs exprs names state = zip names (map (snd. flipSecondThird eval' funcDefs state) exprs) ++ fst (eval' funcDefs (Block exprs) state)

flipSecondThird :: (a -> b -> c -> d) -> a -> c -> b -> d
flipSecondThird f x y z = f x z y

findFunc :: [FunctionDefinition] -> Name -> FunctionDefinition
findFunc funcDefs name = fromJust (find (\(a, b, c) -> a == name) funcDefs)

findRef :: State -> Name -> Integer
findRef state name = snd $ fromJust (find (\(a, b) -> a == name) state)

                                 

