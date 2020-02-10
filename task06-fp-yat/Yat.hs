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

showFuncCallArguments :: [Expression] -> String
showFuncCallArguments []      = ""
showFuncCallArguments [e]     = showExpression e ""
showFuncCallArguments (e:es)  = showExpression e "" ++ ", " ++ showFuncCallArguments es

showBlockArguments :: [Expression] -> String ->String
showBlockArguments [] _         = ""
showBlockArguments [e] tabs     = tabs ++ showExpression e tabs ++ "\n"
showBlockArguments (e:es) tabs  = tabs ++ showExpression e tabs ++ ";\n" ++ showBlockArguments es tabs


showExpression :: Expression -> String -> String
showExpression (Number n) tabs                       = show n
showExpression (Reference name) tabs                 = name
showExpression (Assign name e) tabs                  = "let " ++ name ++ " = " ++ showExpression e tabs ++ " tel"
showExpression (BinaryOperation op l r) tabs         = "(" ++ showExpression l tabs ++ " " ++ showBinop op ++ " " ++ showExpression r tabs ++ ")"
showExpression (UnaryOperation op e) tabs            = showUnop op ++ showExpression e tabs
showExpression (FunctionCall name expressions) tabs  = name ++ "(" ++ showFuncCallArguments expressions ++ ")"
showExpression (Conditional e t f) tabs              = "if " ++ showExpression e tabs ++ " then " ++ showExpression t tabs ++ " else " ++ showExpression f tabs ++ " fi"
showExpression (Block expressions) tabs              = "{\n" ++ showBlockArguments expressions (tabs ++ "\t") ++ tabs ++ "}"


showFunctionDefenition :: FunctionDefinition -> String
showFunctionDefenition (name, [], e) = "func " ++ name ++ "() = " ++ showExpression e "" ++ "\n"
showFunctionDefenition (name, n:names, e) = "func " ++ name ++ "(" ++ n ++ concatMap (", " ++) names ++ ") = " ++ showExpression e "" ++ "\n"

-- Верните текстовое представление программы (см. условие).
showProgram :: Program -> String
showProgram (definitions, e) = foldr ((++) . showFunctionDefenition) "" definitions ++ showExpression e ""

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
getVariable :: State -> Name -> Integer
getVariable [] _                             = 0
getVariable ((varName, varValue):scope) name | name == varName = varValue
                                             | otherwise       = getVariable scope name


getFunctionDefinition :: [FunctionDefinition] -> Name -> ([Name], Expression)
getFunctionDefinition func name = getter (head (filter (equal name) func))
                                  where
                                    equal name (n, names, e) = name == n
                                    getter (n, name, e)      = (name, e)

makeFunctionScope :: State -> [Name] -> [Integer] -> State
makeFunctionScope scope names values = zip names values ++ scope

chainFunction :: [FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
chainFunction func scope []     = ([], scope)
chainFunction func scope (e:es) = (fst eresult:fst esresult, snd esresult)
                              where
                                eresult  = evalExpression func scope e
                                esresult = chainFunction func (snd eresult) es




evalExpression :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpression func scope (Number n)                      = (n, scope)
evalExpression func scope (Reference name)                = (getVariable scope name, scope)
evalExpression func scope (Assign name e)                 = (fst result, (name, fst result):snd result)
                                                            where
                                                              result = evalExpression func scope e
evalExpression func scope (BinaryOperation op l r)        = (toBinaryFunction op (fst lresult) (fst rresult), snd rresult)
                                                            where
                                                              lresult = evalExpression func scope l
                                                              rresult = evalExpression func (snd lresult) r
evalExpression func scope (UnaryOperation op e)           = (toUnaryFunction op (fst result), snd result)
                                                            where
                                                              result = evalExpression func scope e
evalExpression func scope (FunctionCall name expressions) = (fst result, snd resChainFunc)
                                                            where
                                                              resChainFunc     = chainFunction func scope expressions
                                                              resGetFuncDef    = getFunctionDefinition func name
                                                              resMakeFuncScope = makeFunctionScope (snd resChainFunc) (fst resGetFuncDef) (fst resChainFunc)
                                                              result           = evalExpression func resMakeFuncScope (snd resGetFuncDef)
evalExpression func scope (Conditional e t f)             | toBool (fst result) = tresult
                                                          | otherwise           = fresult
                                                            where
                                                              result  = evalExpression func scope e
                                                              tresult = evalExpression func (snd result) t
                                                              fresult = evalExpression func (snd result) f
evalExpression func scope (Block [])                      = (0, scope)
evalExpression func scope (Block [e])                     = evalExpression func scope e
evalExpression func scope (Block (e:es))                  = evalExpression func (snd result) (Block es)
                                                            where
                                                              result = evalExpression func scope e

eval :: Program -> Integer
eval program = fst (evalExpression (fst program) [] (snd program))