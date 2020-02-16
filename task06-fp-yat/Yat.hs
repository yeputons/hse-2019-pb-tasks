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

putTabs :: String -> String
putTabs = intercalate "\n" . map ("\t" ++) . lines

showExpression :: Expression -> String
showExpression (Number          n)                = show n
showExpression (Reference       name)             = name
showExpression (Assign          name e)           = concat ["let ", name, " = ", showExpression e, " tel"]
showExpression (BinaryOperation op l r)           = concat ["(", showExpression l, " ", showBinop op, " ", showExpression r, ")"]
showExpression (UnaryOperation  op e)             = showUnop op ++ showExpression e
showExpression (FunctionCall    name exprs)       = concat [name, "(", intercalate ", " (map showExpression exprs), ")"]
showExpression (Conditional     e t f)            = concat ["if ", showExpression e, " then ", showExpression t, " else ", showExpression f, " fi"]
showExpression (Block           [])               = "{\n}"
showExpression (Block           exprs)            = concat ["{\n", intercalate ";\n" (map (putTabs . showExpression) exprs), "\n}"]

showFunction :: FunctionDefinition -> String
showFunction(name, param, e) = concat ["func ", name, "(", intercalate ", " param, ") = ", showExpression e]

showProgram :: Program -> String
showProgram(funcs, exprs) = concatMap ((++ "\n") . showFunction) funcs ++ showExpression exprs

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

getFunctionDef :: Name -> [FunctionDefinition] -> ([Name], Expression)
getFunctionDef name function = getFD(head (filter byName function))
                                where byName(fName, fNames, expr) = name == fName
                                      getFD (fName, name, expr)   = (name, expr)

addFuncToScope :: State -> [Name] -> [Integer] -> State
addFuncToScope scope names values = zip names values ++ scope

chainOfFunctions :: [FunctionDefinition] -> State -> [Expression] -> ([Integer], State)
chainOfFunctions func scope []     = ([], scope)
chainOfFunctions func scope (e:es) = (fst eresult:fst esresult, snd esresult)
                               where
                                 eresult  = evalExpression func scope e
                                 esresult = chainOfFunctions func (snd eresult) es

getVariable :: State -> Name -> Integer
getVariable []                                  _                        = 0
getVariable ((varName, varValue) : tailOfScope) vName | vName == varName = varValue
                                                      | otherwise        = getVariable tailOfScope vName

evalExpression :: [FunctionDefinition] -> State -> Expression -> (Integer, State)
evalExpression function scope (Number          n)                = (n, scope)
evalExpression function scope (Reference       name)             = (getVariable scope name, scope)
evalExpression function scope (Assign          name e)           = (fst val, var : snd val)
                                                                  where val = evalExpression function scope e
                                                                        var = (name, fst val)
evalExpression function scope (BinaryOperation op l r)           = (toBinaryFunction op (fst lres) (fst rres), snd rres)
                                                                  where lres  = evalExpression function scope l
                                                                        rres  = evalExpression function (snd lres) r
evalExpression function scope (UnaryOperation  op e)             = (toUnaryFunction op (fst res), snd res)
                                                                  where res = evalExpression function scope e
evalExpression function scope (FunctionCall    name exprs)       = (fst res, snd resChainOfFunctions)
                                                                  where resChainOfFunctions = chainOfFunctions function scope exprs
                                                                        resGetFunctionDef   = getFunctionDef name function
                                                                        resAddFuncToScope   = addFuncToScope (snd resChainOfFunctions) (fst resGetFunctionDef) (fst resChainOfFunctions)
                                                                        res                 = evalExpression function resAddFuncToScope (snd resGetFunctionDef) 
evalExpression function scope (Conditional     e t f)            | toBool (fst condRes) = fExprRes
                                                                 | otherwise            = sExprRes
                                                                  where condRes  = evalExpression function scope e  
                                                                        fExprRes = evalExpression function (snd condRes) t
                                                                        sExprRes = evalExpression function (snd condRes) f
evalExpression function scope (Block [])                         = (0, scope)
evalExpression function scope (Block [e])                        = evalExpression function scope e 
evalExpression function scope (Block (e:es))                     = evalExpression function (snd result) (Block es) 
                                                                  where result = evalExpression function scope e

-- Реализуйте eval: запускает программу и возвращает её значение.
eval :: Program -> Integer
eval prog = fst (evalExpression (fst prog) [] (snd prog))
