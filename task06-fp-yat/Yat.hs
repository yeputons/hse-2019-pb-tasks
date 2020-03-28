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

addTabs :: String -> String 
addTabs [] = ""
addTabs (char:chars)
    | char == '\n' = concat [[char], "\t", addTabs chars]
    | otherwise    = char : addTabs chars

showExpression :: Expression -> String
showExpression (Number num)                  = show num
showExpression (Reference var)               = var
showExpression (Assign var_name val)         = concat ["let ", var_name, " = ", showExpression val, " tel"]
showExpression (BinaryOperation bin a b)     = concat ["(", showExpression a, " ", showBinop bin, " ", showExpression b, ")"]
showExpression (UnaryOperation un x)         = showUnop un ++ showExpression x
showExpression (FunctionCall name exprs)     = concat [name, "(", intercalate ", " (map showExpression exprs),  ")"]
showExpression (Conditional cond true false) = concat ["if ", showExpression cond, " then ", showExpression true, " else ", showExpression false, " fi"]
showExpression (Block [])                    = "{\n}"  --нельзя убрать, т.к. тут должен быть один перенос, а во втором случае два.
showExpression (Block exprs)                 = addTabs ("{\n" ++ intercalate ";\n" (map showExpression exprs)) ++ "\n}"

showFunctionDefintion :: FunctionDefinition -> String
showFunctionDefintion (name, vars, expr) = concat ["func ", name, "(", foldr1 (\x y -> concat [x, ", ", y]) vars, ") = ", showExpression expr] 

showState :: State -> String
showState = concatMap (\(var, val) -> concat [var, " == ", show val, "\n"])


-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram ([], expr) = showExpression expr 

showProgram (funcs, expr) = concat [concatMap showFunctionDefintion funcs, "\n", showExpression expr]


-- main :: IO()
-- main = putStrLn $ showProgram ([("sqr", ["x"], BinaryOperation Mul (Reference "x") (Reference "x"))], Block [Assign "x" (Number 20), BinaryOperation Add (Reference "x") (FunctionCall "sqr" [Reference "x"])])

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

getFunctionBody :: Maybe FunctionDefinition -> Expression
getFunctionBody (Just (_, _, body)) = body 
getFunctionBody _ = Number 0

getFunctionArguments :: Maybe FunctionDefinition -> [Name]
getFunctionArguments (Just (_, args, _)) = args
getFunctionArguments _ = []

getArgumentsValues :: [Expression] -> State -> [FunctionDefinition] -> [Integer]
getArgumentsValues [] _ _ = []
getArgumentsValues (expr:exprs) state defs = arg_value : getArgumentsValues exprs new_state defs
                                  where 
                                       (new_state, arg_value) = evalExpression expr state defs

evalExpression :: Expression -> State -> [FunctionDefinition] -> (State, Integer)
evalExpression (Number num) state _ = (state, num)
evalExpression (Reference var) state _ = (state, fromMaybe 0 (lookup var state))

evalExpression (Assign var_name val) state defs = ((var_name, value) : new_state, value)
                                                  where 
                                                       result = evalExpression val state defs
                                                       (new_state, value) = result

evalExpression (BinaryOperation bin a b) state defs = (new_state, value) 
                                                      where
                                                           first_result                  = evalExpression a state defs 
                                                           (first_state, first_value)    = first_result
                                                           second_result                 = evalExpression b first_state defs 
                                                           (second_state, second_value)  = second_result
                                                           value                         = toBinaryFunction bin first_value second_value
                                                           new_state                     = second_state

evalExpression (UnaryOperation un x) state defs = (new_state, value)
                                                  where 
                                                       (new_state, arg_value) = evalExpression x state defs 
                                                       value                  = toUnaryFunction un arg_value

evalExpression (Conditional cond true false) state defs 
    | toBool value = evalExpression true new_state defs 
    | otherwise     = evalExpression false new_state defs 
                                where 
                                     (new_state, value) = evalExpression cond state defs

evalExpression (Block exprs) state defs = (state, value)
                                          where 
                                               match (state_1, _) expr = evalExpression expr state_1 defs
                                               value                   = snd $ foldl match (state, 0) exprs 


evalExpression (FunctionCall name exprs) state defs = (new_state, value)
                                                       where 
                                                            match (state_1, _) expr = evalExpression expr state_1 defs
                                                            args_vals               = getArgumentsValues exprs state defs
                                                            new_state               = fst $ foldl match (state, 0) exprs
                                                            func_name (fname, _, _) = fname
                                                            function                = find (\x -> name == func_name x) defs
                                                            args_names              = getFunctionArguments function
                                                            func_state              = zip args_names args_vals ++ new_state 
                                                            value                   = snd $ evalExpression (getFunctionBody function) func_state defs 
                                                              


eval :: Program -> Integer
eval (defs, expr) = snd $ evalExpression expr [] defs



