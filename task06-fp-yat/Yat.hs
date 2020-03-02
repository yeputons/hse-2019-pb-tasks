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

putTabs :: String -> String
putTabs string = intercalate "\n\t" (lines string)

showExpr :: Expression -> String

showExpr (Number num)                  = show num
showExpr (Reference name)              = name
showExpr (Assign name expr)            = concat ["let ", name, " = ", showExpr expr, " tel"]
showExpr (BinaryOperation op l r)      = concat ["(", showExpr l, " ", showBinop op, " ", showExpr r, ")"]
showExpr (UnaryOperation unop expr)    = showUnop unop ++ showExpr expr
showExpr (FunctionCall name exprs)     = concat [name, "(", intercalate ", " (map showExpr exprs), ")"]
showExpr (Conditional expr true false) = concat ["if ", showExpr expr, " then ", showExpr true, " else ", showExpr false, " fi"]
showExpr (Block [])                    = "{\n}"
showExpr (Block exprs)                 = concat ["{\n\t", putTabs ( intercalate ";\n" $ map showExpr exprs), "\n}"]

showFuncDef :: FunctionDefinition -> String
showFuncDef (name, params, expr) = concat ["func ", name, "(", intercalate ", " params, ") = ", showExpr expr]

showProgram :: Program -> String
showProgram (functions, mainexpr) = concatMap ((++ "\n") . showFuncDef) functions ++ showExpr mainexpr 

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

parseArgs :: [FunctionDefinition] -> State -> FunctionDefinition -> [Expression] -> (State, State)
parseArgs functions scope (_, [], _) _ = (scope, scope)
parseArgs _ _ (_, _:_, _) []         = ([], [])
parseArgs functions scope (fName, argName : argNames, fExpr) (expr:exprs) = (state', st ++ scope)
                                                                          where (st, num)                  = evalExpr functions scope expr
                                                                                function'                  = (fName, argNames, fExpr) 
                                                                                scope'                     = (argName, num) : st
                                                                                (state', _)                = parseArgs functions scope' function' exprs

evalExpr :: [FunctionDefinition] -> State -> Expression -> (State, Integer)

evalExpr _ scope (Number num) = (scope, num) 

evalExpr functions scope (Reference name) = (scope, fromJust $ lookup name scope)

evalExpr functions scope (Assign name expr) = ((name, num):state, num)
                                              where (state, num) = evalExpr functions scope expr

evalExpr functions scope (BinaryOperation op left right) = (state'', toBinaryFunction op num' num'')
                                                            where (state', num')   = evalExpr functions scope left
                                                                  (state'', num'') = evalExpr functions state' right

evalExpr functions scope (UnaryOperation op expr) = (state', toUnaryFunction op num') 
                                                     where (state', num') = evalExpr functions scope expr

evalExpr [] _ (FunctionCall _ _) = ([], 0)

evalExpr ((fName, fArgs, fExpr):functions) scope (FunctionCall name args) | fName /= name    = evalExpr functions' scope (FunctionCall name args)
                                                                          | otherwise        = (state'', num'')
                                                                            where func'                 = (fName, fArgs, fExpr)
                                                                                  functions'            = functions ++ [func']
                                                                                  (state', state'')     = parseArgs functions' scope func' args
                                                                                  (_, num'')            = evalExpr functions' state' fExpr

evalExpr functions scope (Conditional expr true false) | toBool num'             = evalExpr functions state' true
                                                       | otherwise               = evalExpr functions state' false
                                                         where (state', num')    = evalExpr functions scope expr

evalExpr functions scope (Block exprs) = foldl (\(scope',foo) expr -> evalExpr functions scope' expr) (scope, 0) exprs  

eval :: Program -> Integer
eval (funcDefs, expr) = snd ( evalExpr funcDefs [] expr)
