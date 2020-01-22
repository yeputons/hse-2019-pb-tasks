module Exercises where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Control.Arrow
import Data.Char
import Data.Text(isInfixOf, pack)
import Prelude hiding (sum, concat, foldr, map)


sum' :: [Int] -> Int
sum' = sum'' 0

sum'' :: Int -> [Int] -> Int
sum'' ini [] = ini
sum'' ini (x:xs) = ini + sum'' x xs


concat' :: [[a]] -> [a]
concat' = concat'' []

concat'' :: [a] -> [[a]] -> [a]
concat'' ini [] = ini
concat'' ini (x:xs) = x ++ concat'' ini xs

p :: Int
p = 17

hash' :: String -> Int
hash' = hash'' 0

hash'' :: Int -> String -> Int
hash'' ini [] = ini
hash'' ini (x:xs) = ord x + p * hash'' ini xs

foldr' :: (a -> b -> b) -> b -> [a] -> b
foldr' f ini [] = ini
foldr' f ini (x:xs) = f x $ foldr' f ini xs


map' :: (a -> b) -> [a] -> [b]
map' f = foldr' (\x ys -> (f x):ys) []


tryHead :: [a] -> Maybe a
tryHead (x:_) = Just x
tryHead _     = Nothing


tryTail :: [a] -> Maybe [a]
tryTail (_:xs) = Just xs
tryTail _      = Nothing


secondElement :: [a] -> Maybe a
secondElement xs = case tryTail xs of
                     Just a  -> tryHead a
                     _       -> Nothing


thirdElementOfSecondList xs = case secondElement xs of 
                                Just ys -> thirdElement ys  
                                _       -> Nothing 
                                where thirdElement xs = case tryTail xs of
                                                        Just ys -> secondElement ys
                                                        _       -> Nothing 

fifthElement :: [a] -> Maybe a
fifthElement = nthElement 5
                where nthElement 1 (x:xs) = Just x
                      nthElement a (x:xs) = nthElement (a - 1) xs
                      nthElement a [] = Nothing


(~~>) :: Maybe a -> (a -> Maybe b) -> Maybe b
(~~>) (Just ma) f = f ma 
(~~>) _ f = Nothing

thirdElementOfSecondList' :: [[a]] -> Maybe a
thirdElementOfSecondList' xs = secondElement xs ~~> tryTail ~~> tryTail ~~> tryHead


nubBy' :: (a -> a -> Bool) -> [a] -> [a]
nubBy' eq [] = []
nubBy' eq (x:xs) = x:nubBy' eq (unique' eq x xs)
           where unique' f a [] = []
                 unique' f a (x:xs) | f a x     = unique' f a xs
                                    | otherwise = x:unique' f a xs

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = quickSort' [ y | y <- xs, y <= x ] ++ [x] ++ quickSort' [ y | y <- xs, y > x] 


weird':: [[Int]] -> Int
weird' = sum'.map' length.filter ((== 0).(`mod` 2).length.filter (> 10))

type File = (String, [String])


grep' :: (String -> [String] -> [String]) -> (String -> Bool) -> [File] -> [String]
grep' format match [] = []
grep' format match (a:b) = uncurry format ((fst a), filter (match) (snd a)) ++ grep' format match b


isSubstringOf :: String -> String -> Bool
isSubstringOf n s = pack n `isInfixOf` pack s


grepSubstringNoFilename :: String -> [File] -> [String]
grepSubstringNoFilename needle = grep' (\_ s -> s) (isSubstringOf needle)
 

grepExactMatchWithFilename :: String -> [File] -> [String]
grepExactMatchWithFilename needle = grep' (\filename str -> map' ((filename ++ ":") ++) str) (== needle) 