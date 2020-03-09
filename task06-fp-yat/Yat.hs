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

makeFormat :: String -> String
makeFormat = intercalate "\n" . map ("\t"++) . lines

-- Верните текстовое представление программы (см. условие).
showExpression :: Expression -> String
showExpression (Number n)               = show n 
showExpression (Reference name)         = name
showExpression (Assign name expr)       = "let " ++ name ++ " = " ++ showExpression expr ++ " tel"
showExpression (BinaryOperation op l r) = "(" ++ showExpression l ++ " " ++ showBinop op ++ " " ++ showExpression r ++ ")"
showExpression (UnaryOperation op expr) = showUnop op ++ showExpression expr
showExpression (FunctionCall name expr) = name ++ "(" ++ intercalate ", " (map showExpression expr) ++ ")"
showExpression (Conditional expr t f)   = "if " ++ showExpression expr ++ " then " ++ showExpression t ++ " else " ++ showExpression f ++ " fi"
showExpression (Block [])               = "{\n}"
showExpression (Block expr)             = "{\n" ++ intercalate ";\n" (map (makeFormat . showExpression) expr) ++ "\n}"


showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (funcName, varNames, e) = "func " ++ funcName ++ "(" ++ intercalate ", " varNames ++ ") = " ++ showExpression e

showProgram :: Program -> String
showProgram ([], e) = showExpression e
showProgram (funcDef, e) = intercalate "\n" (map showFunctionDefinition funcDef) ++ "\n" ++ showExpression e 

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

getFunctionName :: FunctionDefinition -> Name
getFunctionName (funcName, _, _) = funcName

getFunctionBody :: FunctionDefinition -> ([Name], Expression)
getFunctionBody (_, [], expr)    = ([], expr)
getFunctionBody (_, names, expr) = (names, expr)

getValue :: State -> Name -> Integer
getValue scope name = head [snd s | s <- scope, fst s == name]

makeFunctionScope :: State -> [Name] -> [Integer] -> State
makeFunctionScope scope params values = zip params values ++ scope

getFunctionDefinition :: Name -> [FunctionDefinition] -> ([Name], Expression)
getFunctionDefinition name funcs = getFunctionBody  (head [f | f <- funcs, name == getFunctionName f])

evalManyExpression :: [FunctionDefinition] -> State -> [Expression] -> (State, [Integer])
evalManyExpression funcDefs scope []       = (scope, [])
evalManyExpression funcDefs scope (e:expr) = (fst manyExpression, (:) (snd oneExpression) (snd manyExpression))
                                             where oneExpression  = evalExpression funcDefs scope e 
                                                   manyExpression = evalManyExpression funcDefs (fst oneExpression) expr

evalExpression :: [FunctionDefinition] -> State -> Expression -> (State, Integer)
evalExpression funcDefs scope (Number n)               = (scope, n)
evalExpression funcDefs scope (Reference name)         = (scope, getValue scope name)
evalExpression funcDefs scope (Assign name expr)       = ((:) (name, snd value) (fst value), snd value)
                                                         where value = evalExpression funcDefs scope expr

evalExpression funcDefs scope (BinaryOperation op l r) = (fst rvalue, toBinaryFunction op (snd lvalue) (snd rvalue))
                                                         where lvalue = evalExpression funcDefs scope l
                                                               rvalue = evalExpression funcDefs (fst lvalue) r

evalExpression funcDefs scope (UnaryOperation op expr) = (fst value, toUnaryFunction op (snd value))
                                                         where value = evalExpression funcDefs scope expr

evalExpression funcDefs scope (FunctionCall name expr) = (fst manyFuncResult, snd funcResult)
                                                         where manyFuncResult = evalManyExpression funcDefs scope expr
                                                               funcDef        = getFunctionDefinition name funcDefs
                                                               functionScope  = makeFunctionScope (fst manyFuncResult) (fst funcDef) (snd manyFuncResult)
                                                               funcResult     = evalExpression funcDefs functionScope (snd funcDef)

evalExpression funcDefs scope (Conditional expr t f)     | toBool (snd statement) = truePath
                                                         | otherwise              = falsePath
                                                         where statement = evalExpression funcDefs scope           expr 
                                                               truePath  = evalExpression funcDefs (fst statement) t
                                                               falsePath = evalExpression funcDefs (fst statement) f

evalExpression funcDefs scope (Block [])               = (scope, 0) 
evalExpression funcDefs scope (Block [e])              = evalExpression funcDefs scope e
evalExpression funcDefs scope (Block (e:expr))         = evalExpression funcDefs (fst (evalExpression funcDefs scope e)) (Block expr)

eval :: Program -> Integer
eval (funcDef, expr) = snd (evalExpression funcDef [] expr)

evalState :: Program -> State
evalState (funcDef, expr) = fst (evalExpression funcDef [] expr)
