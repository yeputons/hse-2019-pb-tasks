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

showExpr :: Expression -> String
showExpr (Number num)                      = show num
showExpr (Reference name)                  = name
showExpr (Assign name ex)                  = "let " ++ name ++ " = " ++ showExpr ex ++ " tel"
showExpr (BinaryOperation oper fir sec)    = "(" ++ showExpr fir ++ " " ++ showBinop oper ++ " " ++ showExpr sec ++ ")"
showExpr (UnaryOperation oper ex)          = showUnop oper ++ showExpr ex
showExpr (FunctionCall name [])            = name ++ "()"
showExpr (FunctionCall name ex)            = name ++ "(" ++ intercalate ", " (map showExpr ex) ++ ")"
showExpr (Conditional ex t f)              = "if " ++ showExpr ex ++ " then " ++ showExpr t ++ " else " ++ showExpr f ++ " fi"
showExpr (Block [])                        = "{\n}"
showExpr (Block ex)                        = "{\n" ++ intercalate ";\n" (map (intercalate "\n" . map ("\t"++) . lines . showExpr) ex) ++ "\n}"

showFunc :: FunctionDefinition -> String
showFunc (name, args, ex) = "func " ++ name ++ "(" ++ intercalate ", " args ++ ") = " ++ showExpr ex

-- Верните текстовое представление программы (см. условие).

showProgram :: Program -> String
showProgram (funcs, ex) = concatMap ((++ "\n") . showFunc) funcs ++ showExpr ex

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

getName:: FunctionDefinition -> Name
getName (name, _, _) = name

getArgs :: FunctionDefinition -> [Name]
getArgs (_, args, _) = args

getBody :: FunctionDefinition -> Expression
getBody (_, _, expr) = expr

getValue :: State -> String -> Integer
getValue scope var = case lookup var scope of
                                Just a -> a
                                _       -> 0

evalExpression :: State -> [FunctionDefinition] -> Expression -> (State, Integer)
evalExpression scope _ (Number num)                     = (scope, num)

evalExpression scope _ (Reference ref)                  = (scope, getValue scope ref)

evalExpression scope funcs (Assign name ex)             = (filter (\ var -> fst var /= name) (fst tmp_expr `union` scope) ++ [(name, snd tmp_expr)], snd tmp_expr)
                                                            where tmp_expr = evalExpression scope funcs ex

evalExpression scope funcs (BinaryOperation op fir sec) = (fst tmp_r, toBinaryFunction op (snd tmp_l) (snd tmp_r))
                                                            where tmp_l = evalExpression scope funcs fir
                                                                  tmp_r = evalExpression (union scope $ fst tmp_l) funcs sec

evalExpression scope funcs (UnaryOperation uop op)      = second (toUnaryFunction uop) calc
                                                            where calc = evalExpression scope funcs op

evalExpression scope funcs (FunctionCall name args)     = (new_scope, snd $ evalExpression new_scope funcs (getBody func))
                                                            where new_scope = zip (getArgs func) (map (snd . evalExpression scope funcs) args) ++ fst (evalExpression scope funcs (Block args))
                                                                  func = case find ((== name) . getName) funcs of
                                                                                   Just func' -> func'

evalExpression scope funcs (Conditional cond fir sec)   | toBool(snd condition) = evalExpression (fst condition) funcs fir
                                                        | otherwise             = evalExpression (fst condition) funcs sec
                                                            where condition = evalExpression scope funcs cond

evalExpression scope funcs (Block [])                   = (scope, 0)
evalExpression scope funcs (Block [x])                  = evalExpression scope funcs x
evalExpression scope funcs (Block (x:xs))               = evalExpression  (fst $ evalExpression scope funcs x) funcs  (Block xs)

eval :: Program -> Integer
eval (funcs, expr) = snd $ evalExpression [] funcs expr
