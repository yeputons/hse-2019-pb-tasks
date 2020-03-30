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
showExpr :: Expression -> String
showExpr (Number num)                       = show num
showExpr (Reference name)                   = name 
showExpr (Assign name expr)                 = concat ["let ", name, " = ", showExpr expr, " tel"]
showExpr (BinaryOperation oper left right)  = concat ["(", showExpr left, " ", showBinop oper, " ",  showExpr right, ")"]
showExpr (UnaryOperation oper expr)         = showUnop oper ++ showExpr expr
showExpr (FunctionCall name args)           = concat [name, "(", intercalate ", " $ map showExpr args, ")"]
showExpr (Conditional expr true false)      = concat ["if ", showExpr expr, " then ", showExpr true, " else ", showExpr false, " fi"]
showExpr (Block exprs)                      = concat ["{\n", concatMap (("\t" ++) . (++ "\n")) (lines $ intercalate ";\n" (map showExpr exprs)), "}"]

showFunc :: FunctionDefinition -> String
showFunc (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpr expr]

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

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL = undefined

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression = undefined
-} -- Удалите эту строчку, если решаете бонусное задание.

-- Реализуйте eval: запускает программу и возвращает её значение.
evalArgs :: [FunctionDefinition] -> State -> FunctionDefinition -> [Expression] -> (State, State)
evalArgs _ _ (_,  _:_ , _) []                                          = ([], []) 
evalArgs funcs scope (_, [], _) _                                      = (scope, scope)
evalArgs funcs scope (funcName, nameArg:nameArgs, funcExpr) (arg:args) = let (value, state) = evalExpr funcs scope arg
                                                                             func         = (funcName, nameArgs, funcExpr) 
                                                                             newScope     = (nameArg, value) : state
                                                                             (res, _)     = evalArgs funcs newScope func args
                                                                         in  (res, state ++ scope)



evalExpr :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpr funcs scope (Number num)                   = (num, scope)

evalExpr funcs scope (Reference name)               = let (Just value) = lookup name scope
                                                      in  (value, scope)

evalExpr funcs scope (Assign name expr)             = let (value, state) = evalExpr funcs scope expr
                                                      in  (value, (name, value):state)

evalExpr funcs scope (BinaryOperation oper fst snd) = let (value1, state1) = evalExpr funcs scope fst
                                                          (value2, state2) = evalExpr funcs state1 snd
                                                      in  (toBinaryFunction oper value1 value2, state2)

evalExpr funcs scope (UnaryOperation oper expr)     = let (value, state) = evalExpr funcs scope expr
                                                      in  (toUnaryFunction oper value, state)

evalExpr funcs scope (FunctionCall name exprs)      = let Just (funcName, funcArgs, funcExpr) = find (\(funcName, _, _) -> funcName == name) funcs
                                                          (funcScope, newScope)               = evalArgs funcs scope (funcName, funcArgs, funcExpr) exprs
                                                          (res, _)                            = evalExpr funcs funcScope funcExpr
                                                      in  (res, newScope)


evalExpr funcs scope (Conditional expr true false)  = let (value, state) = evalExpr funcs scope expr
                                                          result         = if toBool value then true else false
                                                      in  evalExpr funcs state result

evalExpr funcs scope (Block exprs)                  = foldl (\(_, res) expr -> evalExpr funcs res expr) (0, scope) exprs


eval :: Program -> Integer
eval (functions, expr) = fst (evalExpr functions [] expr)
