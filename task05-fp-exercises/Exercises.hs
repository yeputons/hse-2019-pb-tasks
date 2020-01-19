module Exercises where -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.

import Control.Arrow
import Data.Char
import Data.Text (isInfixOf, pack)
import Prelude hiding (concat, foldr, map, sum)

{- HLINT ignore "Use foldr" -}
-- 1) Выделение функции высшего порядка.
-- Функция sum' считает сумму чисел в списке при помощи функции sum''.
-- Функция sum'' x xs считает сумму чисел в списке xs плюс x.
-- Реализуйте функцию sum'' рекурсивно, не используя функции, кроме (+).
--
-- >>> sum'' 10 [2, 3]
-- 15
sum' :: [Int] -> Int
sum' = sum'' 0

sum'' :: Int -> [Int] -> Int
sum'' ini [] = ini
sum'' ini (x:xs) = (+) ini $ sum'' x xs

-- Функция concat' принимает на вход список списков и возвращает конкатенацию
-- этих списков. Она использует функцию concat'', которая дополнительно
-- принимает начальное значение, которое дописывается в конец.
-- Реализуйте функцию concat'' рекурсивно, не используя функции, кроме (++).
--
-- >>> concat'' "c" ["a", "b"]
-- "abc"
concat' :: [[a]] -> [a]
concat' = concat'' []

concat'' :: [a] -> [[a]] -> [a]
concat'' ini [] = ini
concat'' ini (x:xs) = (++) x $ concat'' ini xs

-- Функция hash' принимает на вход строку s и считает полиномиальный
-- хэш от строки по формуле hash' s_0...s_{n - 1} =
--  s_0 + p * s_1 + ... + p^{n - 1} * s_{n - 1}, где p - константа
-- (в данном случае, 17).
-- Функция hash' использует функцию hash'', которая принимает на вход
-- начальное значение хэша и строку. Реализуйте функцию hash'' рекурсивно,
-- не используя функции, кроме (+), (*) и (^).
--
-- >>> hash'' 10 "AB"
-- 4077
-- >>> (ord 'A') + (ord 'B') * p + 10 * p ^ 2
-- 4077
p :: Int
p = 17

hash' :: String -> Int
hash' = hash'' 0

hash'' :: Int -> String -> Int
hash'' ini [] = ini
hash'' ini (x:xs) = (+) (ord x) $ (*) p $ hash'' ini xs

-- Выделите общую логику предыдущих функций и реализуйте функцию высшего порядка foldr',
-- не используя никаких стандартных функций.
foldr' :: (a -> b -> b) -> b -> [a] -> b
foldr' _ ini [] = ini
foldr' f ini (x:xs) = f x $ foldr' f ini xs

-- Реализуйте функцию map' (которая делает то же самое, что обычный map)
-- через функцию foldr', не используя стандартных функций.
map' :: (a -> b) -> [a] -> [b]
-- map' f = foldr' (\x y -> f x : y) []
map' f = foldr' ((:) <<< f) [] -- just for import Control.Arrow warning

-- 2) Maybe
-- Maybe a - это специальный тип данных, который может принимать либо
-- значение Nothing, либо значение Just x, где x --- значение типа a.
-- Его удобно использовать для сообщения об ошибке.
-- Даны функции tryHead и tryTail, реализованные следующим образом
-- >>> tryHead []
-- Nothing
-- >>> tryHead ["hello"]
-- Just "hello"
-- >>> tryHead [1, 2, 3]
-- Just 1
tryHead :: [a] -> Maybe a
tryHead (x:_) = Just x
tryHead _ = Nothing

--
-- >>> tryTail []
-- Nothing
-- >>> tryTail ["hello"]
-- Just []
-- >>> :t tryTail ["hello"]
-- tryTail ["hello"] :: [[Char]]
-- >>> tryTail [1, 2, 3]
-- Just [2,3]
tryTail :: [a] -> Maybe [a]
tryTail (_:xs) = Just xs
tryTail _ = Nothing

-- Также предоставлен пример функции, которая возвращает второй элемент
-- списка или Nothing, если второго элемента в списке нет.
--
-- >>> secondElement []
-- Nothing
-- >>> secondElement "a"
-- Nothing
-- >>> secondElement "ab"
-- Just 'b'
secondElement :: [a] -> Maybe a
secondElement xs =
      case tryTail xs of
        Just a -> tryHead a
        _      -> Nothing

-- Используя функции tryHead и tryTail, а также case и сопоставление с
-- образцом (pattern matching) только для Maybe (но не для списков) реализуйте
-- без использования стандартных функций (при этом разрешается заводить свои
-- дополнительные функции, используя where):
-- Функцию thirdElementOfSecondList, которая принимает на вход список
-- списков, и возвращает третий элемент второго списка или Nothing, если
-- второго списка или третьего элемента в нём не существует.
--
-- >>> thirdElementOfSecondList []
-- Nothing
-- >>> thirdElementOfSecondList ["abcd"]
-- Nothing
-- >>> thirdElementOfSecondList [[], [1, 2], [3, 4]]
-- Nothing
-- >>> thirdElementOfSecondList [["a"], ["b", "c", "d"]]
-- Just "d"
thirdElementOfSecondList :: [[a]] -> Maybe a
thirdElementOfSecondList xs =
      maybeTryHead $ maybeTryTail $ maybeTryTail $ maybeTryHead $ maybeTryTail $ Just xs
    maybeTryHead xs =
          case xs of
            Just xs -> tryHead xs
            _       -> Nothing
    maybeTryTail xs =
          case xs of
            Just xs -> tryTail xs
            _       -> Nothing

-- Функцию fifthElement, которая возвращает пятый элемент списка или Nothing,
-- если пятого элемента в списке нет.
-- >>> fifthElement []
-- Nothing
-- >>> fifthElement "abcd"
-- Nothing
-- >>> fifthElement [1, 2, 3, 4, 5]
-- Just 5
fifthElement :: [a] -> Maybe a
fifthElement xs = maybeTryHead $ maybeNthTail 4 xs
  where
    maybeTryHead xs =
          case xs of
            Just xs -> tryHead xs
            _       -> Nothing
    maybeTryTail xs =
          case xs of
            Just xs -> tryTail xs
            _       -> Nothing
    maybeNthTail n xs =
          case n of
            0 -> Just xs
            _ -> maybeTryTail $ maybeNthTail (n - 1) xs

-- Выделите общую логику в оператор ~~>.
(~~>) :: Maybe a -> (a -> Maybe b) -> Maybe b
(~~>) ma f =
      case ma of
        Just ma -> f ma
        _       -> Nothing

-- Перепишите функцию thirdElementOfSecondList в thirdElementOfSecondList' используя
-- только tryHead, tryTail, применение функций и оператор ~~>, но не используя
-- сопоставление с образом (pattern matching) ни в каком виде, case, if, guards.
thirdElementOfSecondList' :: [[a]] -> Maybe a
thirdElementOfSecondList' xs = Just xs ~~> tryTail ~~> tryHead ~~> tryTail ~~> tryTail ~~> tryHead

-- 3) Несколько упражнений
-- Реализуйте функцию nubBy', которая принимает на вход функцию для сравнения
-- элементов на эквивалентность и список элементов и возвращает список из тех же
-- элементов без повторений. Гарантируется, что функция задаёт отношение
-- эквивалентности. Важно сохранить порядок, в котором элементы встречались впервые.
-- Запрещено использовать стандартные функции, которые решают эту задачу.
--
-- >>> nubBy' (==) []
-- []
-- >>> nubBy' (==) "abaacbad"
-- "abcd"
-- nubBy' (\x y -> x == y || x + y == 10) [2, 3, 5, 7, 8, 2]
-- [2,3,5]
nubBy' :: (a -> a -> Bool) -> [a] -> [a]
nubBy' _ [] = []
nubBy' eq (x:xs) = (:) x $ filter' (not . eq x) $ nubBy' eq xs

filter' _ [] = []
filter' f (x:xs) =
      if f x
         then x : filter' f xs
         else filter' f xs

-- hlint recommend to use if, my own version was
-- filter' f (x:xs) =
--       case f x of
--             True -> x : filter' f xs
--             False -> filter' f xs
-- Реализуйте функцию quickSort, которая принимает на вход список, и
-- возвращает список, в котором элементы отсортированы при помощи алгоритма
-- быстрой сортировки.
-- Рандом или быстрый partition использовать не нужно, выберите максимально
-- простую реализацию.
--
-- Требование Ord a => означает, что для типа a можно использовать знаки
-- сравнения (>, <, == и т.д.).
--
-- >>> [x + 1 | x <- [1..10], x > 5]
-- [7,8,9,10,11]
-- >>> quickSort' []
-- []
-- >>> quickSort' [2, 3, 1, 2]
-- [1,2,2,3]
-- >>> quickSort' "babca"
-- "aabbc"
quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = left ++ [x] ++ right
  where
    left  = quickSort' $ filter' (<= x) xs
    right = quickSort' $ filter' (> x) xs

-- Найдите суммарную длину списков, в которых чётное количество элементов
-- имеют квадрат больше 100. Реализация должна быть без использования
-- list comprehension, лямбда-функций, вспомогательных функций или явного
-- упоминания параметра weird': только композиция, частичное применение
-- функций и операторов.
--
-- >>> weird' []
-- 0
-- >>> weird' [[1, 2, 3], [4, 5], [1, 2, 11]]
-- 5
-- >>> weird' [[1, 11, 12], [9, 10, 20]]
-- 3
weird' :: [[Int]] -> Int
weird' = (.) (foldr' ((+) . length) 0) $ filter $ (.) even $ (.) length $ filter $ (> 100) . (^ 2)

-- or either
-- weird' = (.) (sum' . (map' length)) $ filter $ (.) even $ (.) length $ filter $ (> 100) . (^ 2)
-- 4) grep
-- Нужно реализовать несколько вариаций grep'а.
-- Вместо файлов на вход будет подаваться список из структур File,
-- содержащих в себе имя файла и его содержимое (список строк).
-- (Можно считать, что File -- это typedef для кортежа из строки и списка строк).
type File = (String, [String])

-- Функция grep' принимает на вход:
-- * Функцию match :: String -> Bool, которая возвращает True,
--   если параметр-строчка файла является искомым
--   (например, содержит подстроку для поиска).
-- * Функцию format :: String -> [String] -> [String], которая
--   по имени файла и списку найденных искомых строк в нём
--   возвращает список строк для вывода на экран.
-- * Список файлов files :: [File].
-- Функция grep' должна вернуть список строк для вывода на экран
-- после поиска искомых строк во всех файлах.
--
-- >>> grep' (\_ s -> s) ((== 'a') . head) [("a.txt", ["ab", "b"]), ("b.txt", ["b", "ac"])]
-- ["ab", "ac"]
--
-- Здесь (\_ s -> s) --- это лямбда-функция, которая игнорирует первый
-- параметр и возвращает второй.
grep' :: (String -> [String] -> [String]) -> (String -> Bool) -> [File] -> [String]
grep' _ _ [] = []
grep' format match ((name, strings):files) =
      format name (filter' match strings) ++ grep' format match files

-- Также вам предоставлена функция для проверки вхождения подстроки в строку.
-- >>> isSubstringOf "a" "bac"
-- True
-- >>> isSubstringOf "ac" "bac"
-- True
-- >>> isSubstringOf "ab" "bac"
-- False
isSubstringOf :: String -> String -> Bool
isSubstringOf n s = pack n `isInfixOf` pack s

-- При помощи функций выше реализуйте несколько вариантов grep.
--
-- Вариант, когда ищется подстрока и нужно просто вернуть список подходящих
-- строк.
-- >>> grepSubstringNoFilename "b" [("a.txt", ["a", "b"])]
-- ["b"]
-- >>> grepSubstringNoFilename "c" [("a.txt", ["a", "a"]), ("b.txt", ["b", "bab", "c"]), ("c.txt", ["c", "ccccc"])]
-- ["c", "c", "ccccc"]
grepSubstringNoFilename :: String -> [File] -> [String]
grepSubstringNoFilename needle = grep' (curry snd) $ isSubstringOf needle

-- Вариант, когда ищется точное совпадение и нужно ко всем подходящим строкам
-- дописать имя файла через ":".
--
-- >>> grepExactMatchWithFilename "b" [("a.txt", ["a", "b"])]
-- ["a.txt:b"]
-- >>> grepExactMatchWithFilename "c" [("a.txt", ["a", "a"]), ("b.txt", ["b", "bab", "c"]), ("c.txt", ["c", "ccccc"])]
-- ["b.txt:c", "c.txt:c"]
grepExactMatchWithFilename :: String -> [File] -> [String]
grepExactMatchWithFilename needle = grep' (\x -> map' ((x ++ ":") ++)) (== needle)