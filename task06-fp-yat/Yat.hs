module Yat where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Data.List
import Data.Maybe
import Data.Bifunctor
import Debug.Trace
import qualified Data.Map.Strict as Map

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
type State = Map.Map String Integer -- Список пар (имя переменной, значение). Новые значения дописываются в начало, а не перезаписываютсpя
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
showParams :: [String] -> String
showParams = ("("++) . (++")") . intercalate ", "


showTabs :: Int -> String
showTabs tabs = replicate tabs '\t' 

processLine :: String -> String
processLine line = concat["\t", line, "\n"]

showExpression :: Expression -> String 
showExpression (Number x)                              = show x
showExpression (Reference var)                         = var
showExpression (Assign var expr)                       = "let " ++ var ++ " = " ++ showExpression expr ++ " tel" 
showExpression (BinaryOperation op expr1 expr2)        = "(" ++ showExpression expr1 ++ " " ++ showBinop op ++ " " ++ showExpression expr2 ++ ")"
showExpression (UnaryOperation op expr)                = showUnop op ++ showExpression expr
showExpression (FunctionCall fn_name params)           = fn_name ++ showParams (map showExpression params)
showExpression (Conditional stat expr_true expr_false) = "if " ++ showExpression stat ++ " then " ++ showExpression expr_true ++ " else " ++ showExpression expr_false ++ " fi"
showExpression (Block exprs)                           = "{\n" ++ concatMap processLine (lines $ intercalate ";\n" $ map showExpression exprs) ++ "}" 

showFunction :: FunctionDefinition -> String
showFunction (fn_name, params, expr) = "func " ++ fn_name ++ showParams params ++ " = " ++ showExpression expr

showProgram :: Program -> String
showProgram (funcs, expr) = unlines (map showFunction funcs) ++ showExpression expr

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

newtype Eval a = Eval ([FunctionDefinition] -> State -> (a, State))  -- Как data, только эффективнее в случае одного конструктора.

runEval :: Eval a -> [FunctionDefinition] -> State -> (a, State)
runEval (Eval f) = f

evaluated :: a -> Eval a  -- Возвращает значение без изменения состояния.
evaluated x = Eval $ \_ state -> (x, state)

readState :: Eval State  -- Возвращает состояние.
readState = Eval $ \_ state -> (state, state)

addToState :: String -> Integer -> a -> Eval a  -- Добавляет/изменяет значение переменной на новое и возвращает константу.
addToState name val x = Eval $ \funcs state -> (x, Map.insert name val state)

readDefs :: Eval [FunctionDefinition]  -- Возвращает все определения функций.
readDefs = Eval $ \funcs state -> (funcs, state)

andThen :: Eval a -> (a -> Eval b) -> Eval b  -- Выполняет сначала первое вычисление, а потом второе.
andThen f1 f2 = Eval (\funcs state ->
                        let (f1_result, new_state) = runEval f1 funcs state
                        in runEval (f2 f1_result) funcs new_state
                     )
(~~>) = andThen

andEvaluated :: Eval a -> (a -> b) -> Eval b  -- Выполняет вычисление, а потом преобразует результат чистой функцией.
andEvaluated eval func = Eval (\funcs state -> 
                                 let (eval_result, new_state) = runEval eval funcs state
                                 in (func eval_result, new_state)
                              )
(~!>) = andEvaluated

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a  -- Вычисляет список выражений от первого к последнему.
evalExpressionsL func x = foldl (\y expr -> y ~!> func ~~> (evalExpression expr ~!>)) (evaluated x)

evalAssign name expr = evalExpression expr ~~> (\value -> addToState name value value)

chooseDef :: Name -> [FunctionDefinition] -> FunctionDefinition
chooseDef name fs = Data.Maybe.fromJust $ find (\(name1,_,_) -> name1 == name) fs

assignParams :: [Name] -> [Integer] -> Eval Integer
assignParams names values = evalExpression $ Block $ zipWith Assign names (map Number values)

evalExprs :: [Expression] -> Eval [Integer]
evalExprs = evalExpressionsL (flip (:)) []

saveState :: Eval a -> Eval a 
saveState eval = Eval $ \funcs state -> (fst $ runEval eval funcs state, state)

evalFunction :: FunctionDefinition -> [Expression] -> Eval Integer
evalFunction (name, param_names, body) param_exprs = evalExprs param_exprs ~~> (\values -> saveState (assignParams param_names values ~~> (\_ -> evalExpression body)))
 

evalExpression :: Expression -> Eval Integer  -- Вычисляет выражение.
evalExpression (Number x)                              = evaluated x
evalExpression (Reference name)                        = Eval (\funcs state -> (Data.Maybe.fromJust $ Map.lookup name state, state))
evalExpression (Assign name expr)                      = evalAssign name expr
evalExpression (BinaryOperation op expr1 expr2)        = evalExpression expr1 ~~> (\expr1_res -> evalExpression expr2 ~!> toBinaryFunction op expr1_res)
evalExpression (UnaryOperation op expr)                = evalExpression expr ~!> toUnaryFunction op
evalExpression (FunctionCall name param_exprs)         = readDefs ~!> chooseDef name ~~> (\func -> evalFunction func param_exprs)
evalExpression (Conditional stat expr_true expr_false) = evalExpression stat ~~> (\cond -> evalExpression (if toBool cond then expr_true else expr_false))
evalExpression (Block exprs)                           = evalExpressionsL (curry snd) 0 exprs 

-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval (funcs, expr) = fst (runEval (evalExpression expr) funcs Map.empty)
