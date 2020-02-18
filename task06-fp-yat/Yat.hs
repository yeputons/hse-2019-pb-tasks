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


addTab :: String -> String
addTab [] = []
addTab (fst:other) | fst == '\n' = fst : '\t' : addTab other
                   | otherwise   = fst : addTab other


showExpr :: Expression -> String
showExpr (Number num)                    = show num
showExpr (Reference name)                = name 
showExpr (Assign name expr)              = concat ["let ", name, " = ", showExpr expr, " tel"]
showExpr (BinaryOperation oper fst snd)  = concat ["(", showExpr fst, " ", showBinop oper, " ",  showExpr snd, ")"]
showExpr (UnaryOperation oper expr)      = showUnop oper ++ showExpr expr
showExpr (FunctionCall name [])          = name ++ "()"
showExpr (FunctionCall name (fst:other)) = concat [name, "(", showExpr fst, concatMap ((++) ", " . showExpr) other, ")"]
showExpr (Conditional expr true false)   = concat ["if ", showExpr expr, " then ", showExpr true, " else ", showExpr false, " fi"]
showExpr (Block [])                      = "{\n}"
showExpr (Block (fst:other))             = addTab (concat ["{\n", showExpr fst, concatMap ((++) ";\n" . showExpr) other]) ++ "\n}"



showFunc ::  FunctionDefinition -> String
showFunc (name, [], expr)          = concat ["func ", name, "() =", showExpr expr] 
showFunc (name, fst : other, expr) = concat ["func ", name, "(", fst, concatMap (", " ++) other, ") = ", showExpr expr]


showProgram :: Program -> String
showProgram (funcs, expr) = concatMap ((++ "\n") . showFunc) funcs ++ showExpr expr


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


findVar :: String -> State -> Integer
findVar _    []                 = 0
findVar name ((var, val):scope) | name == var = val
                                | otherwise   = findVar name scope 


parseArgs :: [FunctionDefinition] -> State -> FunctionDefinition -> [Expression] -> (State, State)
parseArgs _ _ (_,  _:_ , _) []                                          = ([], []) 
parseArgs funcs scope (_, [], _) _                                      = (scope, scope)
parseArgs funcs scope (funcName, nameArg:nameArgs, funcExpr) (arg:args) = (fst res, state ++ scope)
                                                                          where (int, state) = evalExpr funcs scope arg
                                                                                func         = (funcName, nameArgs, funcExpr) 
                                                                                newScope     = (nameArg, int) : state
                                                                                res          = parseArgs funcs newScope func args



evalExpr :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpr [] _ (FunctionCall _ _)                                                = (0, [])
evalExpr funcs scope (Number num)                                               = (num, scope)
evalExpr funcs scope (Reference name)                                           = (findVar name scope, scope)
evalExpr funcs scope (Assign name expr)                                         = (int, (name, int):state)
                                                                                                  where (int, state) = evalExpr funcs scope expr 

evalExpr funcs scope (BinaryOperation oper fst snd)                         = (toBinaryFunction oper int1 int2, state2)
                                                                                                  where (int1, state1) = evalExpr funcs scope fst
                                                                                                        (int2, state2) = evalExpr funcs state1 snd

evalExpr funcs scope (UnaryOperation oper expr)                                 = (toUnaryFunction oper int, state)
                                                                                                  where (int, state) = evalExpr funcs scope expr

evalExpr ((funcName, funcArgs, funcExpr):funcs) scope (FunctionCall name args)  | funcName /= name = evalExpr newFuncs scope (FunctionCall name args)
                                                                                | otherwise        = (fst eval, snd_state)
                                                                                                  where func                   = (funcName, funcArgs, funcExpr)
                                                                                                        newFuncs               = funcs ++ [func]
                                                                                                        (fst_state, snd_state) = parseArgs newFuncs scope func args
                                                                                                        eval                   = evalExpr newFuncs fst_state funcExpr

evalExpr funcs scope (Conditional expr true false)                              | toBool int = evalExpr funcs state true
                                                                                | otherwise  = evalExpr funcs state false
                                                                                                  where (int, state) = evalExpr funcs scope expr 

evalExpr funcs scope (Block [])                                                 = (0, scope)
evalExpr funcs scope (Block [x])                                                = evalExpr funcs scope x
evalExpr funcs scope (Block (x:xs))                                             = evalExpr funcs (snd (evalExpr funcs scope x)) (Block xs)


eval :: Program -> Integer
eval (functions, expr) = fst (evalExpr functions [] expr)
