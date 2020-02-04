module Yat where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Data.List
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
addTabs = intercalate "\n" . map ("\t"++) . lines

showExpression :: Expression -> String
showExpression (Number n)               = show n
showExpression (Reference name)         = name
showExpression (Assign name e)          = "let " ++ name ++ " = " ++ showExpression e ++ " tel"
showExpression (BinaryOperation op l r) = "(" ++ showExpression l ++ " " ++ showBinop op ++ " " ++ showExpression r ++ ")"
showExpression (UnaryOperation op e)    = showUnop op ++ showExpression e
showExpression (FunctionCall name es)   = name ++ "(" ++ intercalate ", " (map showExpression es) ++ ")"
showExpression (Conditional e t f)      = "if " ++ showExpression e ++ " then " ++ showExpression t ++ " else " ++ showExpression f ++ " fi"
showExpression (Block [])               = "{\n}"
showExpression (Block es)               = "{\n" ++ intercalate ";\n" (map (addTabs . showExpression) es) ++ "\n}"

showFunction :: FunctionDefinition -> String
showFunction (name, args, e) = "func " ++ name ++ "(" ++ intercalate ", " args ++ ") = " ++ showExpression e

showFunctions :: [FunctionDefinition] -> String
showFunctions = concatMap showFunction

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (functions, expression) = intercalate "\n" $ filter (not . null) [showFunctions functions, showExpression expression]

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

readFromState :: Name -> State -> Integer
readFromState _ []                                         = undefined
readFromState name ((val_name, val):xs) | name == val_name = val
                                        | otherwise        = readFromState name xs

addToState :: Name -> Integer -> State -> State
addToState name val state = case findIndex ((==)name . fst) state of
                                Just i     -> take i state ++ [(name, val)] ++ drop (i + 1) state
                                _          -> (name, val) : state

findFunction :: Name -> [FunctionDefinition] -> FunctionDefinition
findFunction name = head . filter (\(f_name, _, _) -> f_name == name)

addNamedArgsToState :: [Name] -> [Integer] -> State -> State
addNamedArgsToState [] _ state                         = state
addNamedArgsToState _ [] state                         = state
addNamedArgsToState (name:names) (value:values) state  = addToState name value $ addNamedArgsToState names values state

(++++) :: Integer -> ([Integer], State) -> ([Integer], State)
(++++) a (xs, state) = (a:xs, state)

getAllValuesAndEndState :: [Expression] -> [FunctionDefinition] -> State -> ([Integer], State)
getAllValuesAndEndState [] _ state      = ([], state)
getAllValuesAndEndState (e:es) fs state = val ++++ getAllValuesAndEndState es fs new_state
                                            where (val, new_state) = evalProgram (fs, e) state

callFuntion :: Name -> [FunctionDefinition] -> [Expression] -> State -> (Integer, State)
callFuntion name fs args state = (fst $ evalProgram (fs, func_e) (addNamedArgsToState args_name values new_state), new_state)
                                                    where (_, args_name, func_e) = findFunction name fs
                                                          (values, new_state)    = getAllValuesAndEndState args fs state

evalProgram :: Program -> State -> (Integer, State)
evalProgram (_, Number n) state                         = (n, state)
evalProgram (_, Reference name) state                   = (readFromState name state, state)
evalProgram (fs, Assign name e) state                   = (val, addToState name val new_state)
                                                            where (val, new_state)   = evalProgram (fs, e) state
evalProgram (fs, BinaryOperation op l r) state          = (toBinaryFunction op val val', new_state')
                                                            where (val, new_state)   = evalProgram (fs, l) state
                                                                  (val', new_state') = evalProgram (fs, r) new_state
evalProgram (fs, UnaryOperation unop e) state           = (toUnaryFunction unop val, new_state)
                                                            where (val, new_state)   = evalProgram (fs, e) state
evalProgram (fs, FunctionCall name args) state          = callFuntion name fs args state
evalProgram (fs, Conditional e t f) state | toBool cond = evalProgram (fs, t) new_state
                                          | otherwise   = evalProgram (fs, f) new_state
                                                            where (cond, new_state)  = evalProgram (fs, e) state
evalProgram (fs, Block es) state                        = foldl (\(_, new_state) e -> evalProgram (fs, e) new_state) (0, state) es


eval :: Program -> Integer
eval program = fst $ evalProgram program []
