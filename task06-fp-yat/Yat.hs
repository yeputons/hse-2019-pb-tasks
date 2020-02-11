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

putTabs::String -> [String]
putTabs xs = map ("\t" ++) (foldr putTabs' [] xs) 

putTabs':: Char -> [String] -> [String]
putTabs' '\n' xs       = [] : xs
putTabs' x []          = [[x]]
putTabs' x (xs : xss)  = (x : xs) : xss

showExpression :: Expression -> String
showExpression (Number n)               = show n
showExpression (Reference name)         = name
showExpression (Assign name e)          = "let " ++ name ++ " = " ++ showExpression e ++ " tel"
showExpression (BinaryOperation op l r) = "(" ++ showExpression l ++ " " ++ showBinop op ++ " " ++ showExpression r ++ ")"
showExpression (UnaryOperation op e)    = showUnop op ++ showExpression e
showExpression (Conditional e t f)      = "if " ++ showExpression e ++ " then " ++ showExpression t ++ " else " ++ showExpression f ++ " fi"
showExpression (FunctionCall name exp)  = name ++ "(" ++ intercalate ", " (map showExpression exp) ++ ")"
showExpression (Block [])               = "{\n}"
showExpression (Block exp)              = "{\n" ++ (intercalate "\n" . putTabs . intercalate ";\n" . map showExpression) exp ++ "\n}"

showFunction::FunctionDefinition -> String
showFunction (name, param, body) = "func " ++ name ++ "(" ++ intercalate ", " param ++ ") = " ++ showExpression body 

showProgram :: Program -> String
showProgram (funcs, ex) = concatMap ((++ "\n") . showFunction) funcs ++ showExpression ex

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
getName (name, _, _)  = name

getFun::FunctionDefinition -> ([Name],Expression)
getFun (_, arg, body) = (arg, body)

getFunDef::[FunctionDefinition] -> Name -> ([Name], Expression)
getFunDef func name   = fun (head (filter (equal name) func))
                          where equal name func = name == getName func
                                fun             = getFun 

makeScope::State -> [Name] -> [Integer] -> State
makeScope scope names values = zip names values ++ scope

chainCall::[FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
chainCall func scope []      = ([], scope)
chainCall func scope (e:es)  = (fst x:fst xs, snd xs)
                                 where x  = evalExpression func scope e
                                       xs = chainCall func (snd x) es




evalExpression::[FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpression func state (Number n)               = (n, state)
evalExpression func state (Reference name)         = case lookup name state of
                                                          Just a            -> (a, state)
                                                          Nothing           -> (0,state)
evalExpression func state (Assign name e)          = second ((:) (name, fst result)) result
                                                          where result      = evalExpression func state e
evalExpression func state (BinaryOperation op l r) = first (toBinaryFunction op (fst lr)) rr
                                                          where lr          = evalExpression func state l
                                                                rr          = evalExpression func (snd lr) r
evalExpression func state (UnaryOperation op e)    = first (toUnaryFunction op) res
                                                           where res        = evalExpression func state e
evalExpression func state (FunctionCall name exp)  = (res, snd newScope)
                                                           where res        = fst (evalExpression func tempScope (snd fun))
                                                                 fun        = getFunDef func name
                                                                 newScope   = chainCall func state exp
                                                                 tempScope  = makeScope (snd newScope) (fst fun) (fst newScope)
evalExpression func state (Conditional e t f)      | toBool (fst res)       = evalExpression func (snd res) t
                                                   | otherwise              = evalExpression func (snd res) f
                                                            where res       = evalExpression func state e
evalExpression func state (Block [])               = (0, state)
evalExpression func state (Block [e])              = evalExpression func state e
evalExpression func state (Block (e:es))           = evalExpression func (snd (evalExpression func state e)) (Block es)                       

eval :: Program -> Integer
eval (def, exp) = fst (evalExpression def [] exp)
