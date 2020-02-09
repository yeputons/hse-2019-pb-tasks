module Yat where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Data.List

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
addTabs []      = []
addTabs (s:str) | s == '\n' = s:'\t':addTabs str
                | otherwise = s:addTabs str

showExpression :: Expression -> String
showExpression (Number n)                      = show n
showExpression (Reference name)                = name
showExpression (Assign name expr)              = concat ["let ", name, " = ", showExpression expr, " tel"]
showExpression (BinaryOperation op left right) = concat ["(", showExpression left, " ", showBinop op, " ", showExpression right, ")"]
showExpression (UnaryOperation op expr)        = showUnop op ++ showExpression expr
showExpression (FunctionCall name args)        = concat [name, "(", intercalate ", " (map showExpression args), ")"]
showExpression (Conditional expr ifT ifF)      = concat ["if ", showExpression expr, " then ", showExpression ifT, " else ", showExpression ifF, " fi"]
showExpression (Block [])                      = "{\n}"
showExpression (Block exprs)                   = concat ["{\n\t", addTabs $ intercalate ";\n" $ map showExpression exprs, "\n}"]
                                          

showFunctionDefinition :: FunctionDefinition -> String
showFunctionDefinition (name, args, expr) = concat ["func ", name, "(", intercalate ", " args, ") = ", showExpression expr]

showProgram :: Program -> String
showProgram (funcs, body) = concatMap ((++ "\n") . showFunctionDefinition) funcs ++ showExpression body 

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

-- Некоторые функции мне понадобилсь для реализации
newtype Eval a = Eval ([FunctionDefinition] -> State -> (a, State))

runEval :: Eval a -> [FunctionDefinition] -> State -> (a, State)
runEval (Eval f) = f

evaluated :: a -> Eval a
evaluated a = Eval evaluated'
              where evaluated' _ st = (a, st)

addToState :: String -> Integer -> a -> Eval a
addToState name value a = Eval addToState'
                          where addToState' _   []                            = (a, [(name, value)])
                                addToState' fds ((ref, val):vs) | ref == name = (a, (name, value):vs)
                                                                | otherwise   = (a, (ref,val):snd (addToState' fds vs))

evalExpressionsL :: (a -> Integer -> a) -> a -> [Expression] -> Eval a
evalExpressionsL _ a []     = Eval evalExpressionsL' 
                              where evalExpressionsL' _ st = (a, st)
evalExpressionsL f a (e:es) = Eval evalExpressionsL'
                              where evalExpressionsL' fds st = runEval (evalExpressionsL f newA es) fds newSt
                                                               where newA          = f a valE
                                                                     (valE, newSt) = runEval (evalExpression e) fds st


-- Если хотите дополнительных баллов, реализуйте
-- вспомогательные функции ниже и реализуйте evaluate через них.
-- По минимуму используйте pattern matching для `Eval`, функции
-- `runEval`, `readState`, `readDefs` и избегайте явной передачи состояния.

{- -- Удалите эту строчку, если решаете бонусное задание.
newtype Eval a = Eval ([FunctionDefinition] -> State -> (a, State))  -- Как data, только эффективнее в случае одного конструктора.

runEval :: Eval a -> [FunctionDefinition] -> State -> (a, State)
runEval (Eval f) = f

evaluated :: a -> Eval a  -- Возвращает значение без изменения состояния.
evaluated a = Eval evaluated'
              where evaluated' _ st = (a, st)

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

evalExpression :: Expression -> Eval Integer
evalExpression (Number    n   )           = evaluated n
evalExpression (Reference name)           = Eval evalExpression'
                                            where evalExpression' _ st                           = (lookup st, st)
                                                  lookup          []                             = undefined
                                                  lookup          ((ref, val):vs) | ref == name  = val
                                                                                  | otherwise    = lookup vs

evalExpression (Assign    name expr)      = Eval evalExpression'
                                            where evalExpression' fds st = runEval (addToState name valE valE) fds newSt
                                                                           where (valE, newSt) = runEval (evalExpression expr) fds st

evalExpression (BinaryOperation op left right) = Eval evalExpression'
                                                 where evalExpression' fds st = (binF valLeft valRight, newString2)
                                                                                where binF                   = toBinaryFunction op
                                                                                      (valLeft, newString1)  = runEval          (evalExpression left) fds st
                                                                                      (valRight, newString2) = runEval          (evalExpression right) fds newString1

evalExpression (UnaryOperation op expr)   = Eval evalExpression'
                                            where evalExpression' fds st = (unF valE, newString)
                                                                           where unF  = toUnaryFunction op
                                                                                 (valE, newString) = runEval (evalExpression expr) fds st

evalExpression (FunctionCall name args)   = Eval evalExpression'
                                            where evalExpression' fds st = (fRet, newString)
                                                                           where fLookup []                                         = undefined
                                                                                 fLookup ((fName, fArgs, fBody):fs) | fName == name = (fArgs, fBody)
                                                                                                                    | otherwise     = fLookup fs
                                                                                 (fRet, _)                              = runEval (evalExpression fBody) fds fState
                                                                                 (fArgNames, fBody)                     = fLookup fds
                                                                                 (fState, newString)                    = extendState fArgNames args st
                                                                                 extendState [] []                   st = (st, st)
                                                                                 extendState [] _                    _  = undefined
                                                                                 extendState _  []                   _  = undefined
                                                                                 extendState (name:names) (arg:args) st = (snd $ runEval (addToState name valE 0) fds fState', newString')
                                                                                                                          where (valE, tmpString)     = runEval (evalExpression arg) fds st
                                                                                                                                (fState', newString') = extendState names args tmpString
evalExpression (Conditional c left right)      = Eval evalExpression'
                                                 where evalExpression' fds st = if toBool valC then valLeft else valRight
                                                                                where (valC, newString) = runEval (evalExpression c)  fds st
                                                                                      valLeft           = runEval (evalExpression left) fds newString
                                                                                      valRight          = runEval (evalExpression right) fds newString

evalExpression (Block es)                 = Eval evalExpression'
                                            where evalExpression' = runEval (evalExpressionsL (\_ a -> a) 0 es)


eval :: Program -> Integer
eval (fds, expr) = fst $ runEval (evalExpression expr) fds []
