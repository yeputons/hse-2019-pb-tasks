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

showExpression :: Expression -> String
showExpression (Number n)               = show n
showExpression (Reference name)         = name
showExpression (Assign name expr)       = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op l r) = concat ["(", showExpression l, " ", showBinop op, " ", showExpression r, ")"]
showExpression (UnaryOperation op expr) = showUnop op ++ showExpression expr
showExpression (FunctionCall name args) = concat [name, "(", intercalate ", " (map showExpression args), ")"]
showExpression (Conditional cond t f)   = concat ["if ", showExpression cond, " then ", showExpression t, " else ", showExpression f, " fi"]
showExpression (Block expr)             = concat ["{\n", concatMap (("\t" ++) . (++ "\n")) (lines $ intercalate ";\n" (map showExpression expr)), "}"]

-- Верните текстовое представление программы (см. условие).
showFunctionDefenition :: FunctionDefinition -> String
showFunctionDefenition (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expr, "\n"]


showProgram :: Program -> String

showProgram (funcs, expr) = concatMap showFunctionDefenition funcs ++ showExpression expr


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

--type Name = String
--type FunctionDefinition = (Name, [Name], Expression)  -- Имя функции, имена параметров, тело функции
--type State = [(String, Integer)]  -- Список пар (имя переменной, значение). Новые значения дописываются в начало, а не перезаписываютсpя
--type Program = ([FunctionDefinition], Expression)  -- Все объявленные функций и основное тело программы

getName:: FunctionDefinition -> Name
getName (name, _, _) = name

getArgs :: FunctionDefinition -> [Name]
getArgs (_, args, _) = args

getBody :: FunctionDefinition -> Expression
getBody (_, _, expr) = expr

getArgsScope :: State -> [FunctionDefinition] -> [(Name, Expression)] -> (State, State)
getArgsScope scope funcs args  = (new_scope, func_scope ++ new_scope)
                                 where (new_scope, func_scope) = foldl (\ (tmp_scope, func_scope) (name, expr) -> 
                                                                       let (cur_scope, res) = evalExpression scope funcs expr
                                                                       in (cur_scope, (name, res):func_scope)) (scope, []) args

evalExpression :: State -> [FunctionDefinition] -> Expression -> (State, Integer)
evalExpression scope funcs (Number n)               = (scope, n)

evalExpression scope funcs (Reference name)         = case lookup name scope of
                                                        Just numb -> (scope, numb)
                                                        _         -> (scope, 0)   

evalExpression scope funcs (Assign name expr)       = ((name, tmp_res):tmp_scope, tmp_res)
                                                            where (tmp_scope, tmp_res) = evalExpression scope funcs expr

evalExpression scope funcs (BinaryOperation op l r) = (scope_r, toBinaryFunction op res_l res_r)
                                                            where (scope_l, res_l) = evalExpression scope funcs l
                                                                  (scope_r, res_r) = evalExpression scope_l funcs r

evalExpression scope funcs (UnaryOperation op expr) = (scp, toUnaryFunction op res)
                                                            where (scp, res) = evalExpression scope funcs expr 

evalExpression scope funcs (FunctionCall name args) = (new_scope, snd $ evalExpression func_scope funcs (getBody func))
                                                                    where (new_scope, func_scope) = getArgsScope scope funcs $ zip (getArgs func) args 
                                                                          func = fromJust $ find ((== name) . getName) funcs

evalExpression scope funcs (Conditional cond t f)   | toBool cond_res = evalExpression cond_scope funcs t
                                                    | otherwise       = evalExpression cond_scope funcs f
                                                                    where (cond_scope, cond_res) = evalExpression scope funcs cond

evalExpression scope funcs (Block expressions)       = foldl (\ (scope, value) expr -> evalExpression scope funcs expr) (scope, 0)  expressions

eval :: Program -> Integer
eval (funcs, expr) = snd $ evalExpression [] funcs expr
    