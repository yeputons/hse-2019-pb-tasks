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
tabulate :: String -> String
tabulate s = intercalate "\n\t" (lines s)

showExpression :: Expression -> String
showExpression (Number n)                          = show n
showExpression (Reference name)                    = name
showExpression (Assign name expr)                  = "let " ++ name ++ " = " ++ showExpression expr ++ " tel"
showExpression (BinaryOperation binop expr1 expr2) = "(" ++ showExpression expr1 ++ " " ++ showBinop binop ++ " " ++ showExpression expr2 ++ ")"
showExpression (UnaryOperation unop expr)          = showUnop unop ++ showExpression expr
showExpression (FunctionCall name exprs)           = name ++ "(" ++ intercalate ", " (map showExpression exprs) ++ ")"
showExpression (Conditional expr1 expr2 expr3)     = "if " ++ showExpression expr1 ++ " then " ++ showExpression expr2 ++ " else " ++ showExpression expr3 ++ " fi"
showExpression (Block [])                          = "{\n}"
showExpression (Block exprs)                       = "{\n\t" ++ tabulate (intercalate ";\n" (map showExpression exprs)) ++ "\n}"

showFunction :: FunctionDefinition -> String
showFunction (name, params, expr) = "func " ++ name ++ "(" ++ intercalate ", " params ++ ") = " ++ showExpression expr ++ "\n"
showProgram :: Program -> String
showProgram (funcs, expr) = concatMap showFunction funcs ++ showExpression expr

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
getValue :: State -> Name -> Integer
getValue [] _            = 0
getValue (var:vars) name
   |name == fst var      = snd var
   |otherwise            = getValue vars name

evalArgs :: [FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
evalArgs funcs scope [] = ([], scope)
evalArgs funcs scope (expr:exprs) = (value:values, newScope)
                                  where (value, tmpScope)  = evalExpression funcs scope expr
                                        (values, newScope) = evalArgs funcs tmpScope exprs

findFunction :: Name -> [FunctionDefinition] -> ([Name], Expression)
findFunction _ []    = undefined
findFunction funcName ((name, args, expr):funcs)
   |funcName == name = (args, expr)
   |otherwise        = findFunction funcName funcs

evalExpression :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpression funcs scope (Number n)                          = (n, scope)
evalExpression funcs scope (Reference name)                    = (getValue scope name, scope)
evalExpression funcs scope (Assign name expr)                  = (val, ((name, val) : newScope))
                                                               where (val, newScope) = evalExpression funcs scope expr
evalExpression funcs scope (BinaryOperation binop expr1 expr2) = ((toBinaryFunction binop) value1 value2, newScope)
                                                               where (value1, tmpScope) = evalExpression funcs scope expr1
                                                                     (value2, newScope) = evalExpression funcs tmpScope expr2
evalExpression funcs scope (UnaryOperation unop expr)          = (toUnaryFunction unop (value), newScope)  
                                                               where (value, newScope) = evalExpression funcs scope expr
evalExpression funcs scope (FunctionCall name args)            = (value, tmpScope)
                                                               where (values, tmpScope) = evalArgs funcs scope args
                                                                     (argNames, expr)   = findFunction name funcs
                                                                     tmpScope2          = zip argNames values ++ tmpScope
                                                                     (value, _)  = evalExpression funcs tmpScope2 expr
evalExpression funcs scope (Conditional expr1 expr2 expr3)
                                                              |toBool res1 = (res2, tmpScope2)
                                                              |otherwise   = (res3, tmpScope3)
                                                              where (res1, tmpScope)  = evalExpression funcs scope expr1
                                                                    (res2, tmpScope2) = evalExpression funcs tmpScope expr2
                                                                    (res3, tmpScope3) = evalExpression funcs tmpScope expr3 
evalExpression funcs scope (Block [])                         = (0, scope)
evalExpression funcs scope (Block [expr])                     = evalExpression funcs scope expr
evalExpression funcs scope (Block (expr:exprs))               = evalExpression funcs newScope (Block exprs)
                                                              where (_, newScope) = evalExpression funcs scope expr
eval :: Program -> Integer
eval program = fst (evalExpression (fst program) [] (snd program))

