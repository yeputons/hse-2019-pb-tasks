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
addTabs (char:chars) | char == '\n' = concat [[char], "\t", addTabs chars]
                     | otherwise    = char : addTabs chars

showExpression :: Expression -> String
showExpression (Number number)                 = show number
showExpression (Reference name)                = name
showExpression (Assign name exp)               = "let " ++ name ++ " = " ++ showExpression exp ++ " tel"
showExpression (BinaryOperation op left right) = "(" ++ showExpression left ++ " " ++ showBinop op ++ " " ++showExpression right ++ ")"
showExpression (UnaryOperation op x)           = showUnop op ++ showExpression x
showExpression (Conditional cond true false)   = "if " ++ showExpression cond ++ " then " ++ showExpression true ++ " else " ++ showExpression false ++ " fi"
showExpression (FunctionCall name exp)         = name ++ "(" ++ intercalate ", " (map showExpression exp) ++ ")"
showExpression (Block [])                      = "{\n}"
showExpression (Block exp)                     = addTabs ("{\n" ++ foldr1 (\x y -> concat [x, ";\n", y]) (map showExpression exp)) ++ "\n}"

showFunctionDef :: FunctionDefinition -> String
showFunctionDef (name, vars, exp) = "func " ++ name ++ "(" ++ intercalate ", " vars ++ ") = " ++ showExpression exp 

showProgram :: Program -> String
showProgram (function, exp) = concatMap ((++ "\n") . showFunctionDef) function ++ showExpression exp

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

getName::FunctionDefinition -> Name
getName (name, _, _) = name

getArguments::FunctionDefinition -> [Name]
getArguments (_, vars, _) = vars

getExpression::FunctionDefinition -> Expression
getExpression (_, _, exp) = exp

getFun::FunctionDefinition -> ([Name],Expression)
getFun (_, vars, exp) = (vars, exp)

getFunDef::[FunctionDefinition] -> Name -> ([Name], Expression)
getFunDef function name  = func (head (filter (equal name) function))
                             where equal name function = name == getName function
                                   func                = getFun 

makeScope::State -> [Name] -> [Integer] -> State
makeScope scope names value = zip names value ++ scope

chainCall::[FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
chainCall function scope []         = ([], scope)
chainCall function scope (exp:exps) = (fst x:fst xs, snd xs)
                                        where x  = evalExpression function scope exp
                                              xs = chainCall function (snd x) exps


evalExpression::[FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpression function state (Number number) = (number, state)
evalExpression function state (Reference name)                = case lookup name state of 
                                                                  Just a  -> (a, state)
                                                                  Nothing -> (0, state)
evalExpression function state (Assign name exp)               = second ((:) (name, fst result)) result
                                                                  where result = evalExpression function state exp
evalExpression function state (BinaryOperation op left right) = first (toBinaryFunction op (fst left')) right'
                                                                  where left'  = evalExpression function state left
                                                                        right' = evalExpression function (snd left') right
evalExpression function state (UnaryOperation op x)           = first (toUnaryFunction op) result
                                                                  where result = evalExpression function state x
evalExpression function state (Conditional exp true false) | toBool (fst result) = evalExpression function (snd result) true
                                                           | otherwise           = evalExpression function (snd result) false
                                                                  where result = evalExpression function state exp
evalExpression function state (FunctionCall name exp)         = (result, snd nScope)
                                                                  where result = fst (evalExpression function tScope (snd func))
                                                                        nScope = chainCall function state exp
                                                                        tScope = makeScope (snd nScope) (fst func) (fst nScope)
                                                                        func   = getFunDef function name
evalExpression function state (Block [])                      = (0, state)
evalExpression function state (Block [exp])                   = evalExpression function state exp
evalExpression function state (Block (exp:exps))              = evalExpression function (snd (evalExpression function state exp)) (Block exps)  

eval :: Program -> Integer
eval (def, exp) = fst (evalExpression def [] exp)
