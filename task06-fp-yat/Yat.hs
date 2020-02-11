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

addTabs :: String -> String
addTabs = intercalate "\n" . map ("\t" ++) . lines

showExpression :: Expression -> String
showExpression (Number num)                        = show num
showExpression (Reference name)                    = name
showExpression (Assign name e)                     = "let " ++ name ++ " = " ++ showExpression e ++ " tel"
showExpression (BinaryOperation op l r)            = "(" ++ showExpression l ++ " " ++ showBinop op ++ " " ++ showExpression r ++ ")"
showExpression (UnaryOperation op e)               = showUnop op ++ showExpression e
showExpression (FunctionCall name args)            = name ++ "(" ++ intercalate ", " (map showExpression args) ++ ")"
showExpression (Conditional e t f)                 = "if " ++ showExpression e ++ " then " ++ showExpression t ++ " else " ++ showExpression f ++ " fi"
showExpression (Block [])                          = "{\n}"
showExpression (Block exprs)                       = "{\n" ++ intercalate ";\n" (map (addTabs . showExpression) exprs) ++ "\n}"

showFunction :: FunctionDefinition -> String
showFunction (name, args, e) = "func " ++ name ++ "(" ++ intercalate ", " args ++ ") = " ++ showExpression e


showProgram :: Program -> String
showProgram (functions, exprs) = intercalate "\n" (map showFunction functions ++ [showExpression exprs])

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


getVar :: Name -> State -> Integer
getVar _ []                                              = 0
getVar name ((varName, varValue):scope)| name == varName = varValue
                                       | otherwise      = getVar name scope

getFuncDef :: Name -> [FunctionDefinition] -> ([Name], Expression)
getFuncDef name funcs = f (head (filter (eq name) funcs)) 
                      where eq name (n, names, e) = name == n
                            f (n, name, e) = (name, e)

createFuncScope :: State -> [Name] -> [Integer] -> State
createFuncScope scope names values = zip names values ++ scope

chainExpr :: [FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
chainExpr func scope []     = ([], scope)
chainExpr func scope (e:es) = (fst exResult:fst esResult, snd esResult)
                            where exResult  = evalExpr func scope e
                                  esResult  = chainExpr func (snd exResult) es

evalExpr :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpr funcs scope (Number n)               = (n, scope)
evalExpr funcs scope (Reference name)         = (getVar name scope, scope)
evalExpr funcs scope (Assign name e)          = (fst result, var:snd result)
                                              where result = evalExpr funcs scope e
                                                    var    = (name, fst result)
evalExpr funcs scope (FunctionCall name args) = (fst (evalExpr funcs (createFuncScope (snd result) (fst func) (fst result)) (snd func)), snd result) 
                                              where func   = getFuncDef name funcs
                                                    result = chainExpr funcs scope args
evalExpr funcs scope (UnaryOperation op e)    = (toUnaryFunction op (fst result), snd result)
                                              where result = evalExpr funcs scope e
evalExpr funcs scope (BinaryOperation op l r) = (toBinaryFunction op (fst lres) (fst rres), snd rres)
                                              where lres = evalExpr funcs scope l
                                                    rres = evalExpr funcs (snd lres) r
evalExpr funcs scope (Conditional e t f)      | toBool (fst res) = evalExpr funcs (snd res) t
                                              | otherwise        = evalExpr funcs (snd res) f
                                              where res = evalExpr funcs scope e
evalExpr funcs scope (Block [x])              = evalExpr funcs scope x
evalExpr funcs scope (Block [])               = (0, scope)                                         
evalExpr funcs scope (Block (e:es))           = evalExpr funcs (snd (evalExpr funcs scope e)) (Block es)

eval :: Program -> Integer
eval program = fst (evalExpr (fst program) [] (snd program))