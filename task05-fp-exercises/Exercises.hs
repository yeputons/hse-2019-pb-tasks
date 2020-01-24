module Exercises where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Control.Arrow
import Data.Char
import Data.Text(isInfixOf, pack)
import Prelude hiding (sum, concat, foldr, map)



sum' :: [Int] -> Int
sum' = sum'' 0

sum'' :: Int -> [Int] -> Int
sum'' ini [] = ini
sum'' ini (x:xs) = ini + x + sum'' 0 xs


concat' :: [[a]] -> [a]
concat' = concat'' []

concat'' :: [a] -> [[a]] -> [a]
concat'' ini [] = ini
concat'' ini [x] = x ++ ini
concat'' ini (x:y:xs) = concat'' ini $ (x ++ y):xs


p :: Int
p = 17

hash' :: String -> Int
hash' = hash'' 0

hash'' :: Int -> String -> Int
hash'' ini [] = ini
hash'' ini (x:xs) = ord x + p * hash'' ini xs


foldr' :: (a -> b -> b) -> b -> [a] -> b
foldr' _ ini [] = ini
foldr' f ini (x:xs) = f x $ foldr' f ini xs


map' :: (a -> b) -> [a] -> [b]
map' f = foldr' (\ x xs -> f x : xs) []

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


thirdElementOfSecondList :: [[a]] -> Maybe a
thirdElementOfSecondList xss = case tryTail xss of 
                                    Just xs -> case tryHead xs of
                                                Just x  -> case tryTail x of
                                                            Just a  -> secondElement a
                                                            Nothing -> Nothing
                                                Nothing -> Nothing
                                    Nothing  -> Nothing


fifthElement :: [a] -> Maybe a
fifthElement = element 4
            where 
                element 0 xs = tryHead xs
                element num xs = case tryTail xs of
                                        Just xs -> element (num - 1) xs
                                        Nothing -> Nothing


(~~>) :: Maybe a -> (a -> Maybe b) -> Maybe b
(~~>) (Just ma) f = f ma
(~~>) Nothing _ = Nothing


thirdElementOfSecondList' :: [[a]] -> Maybe a
thirdElementOfSecondList' xs = tryTail xs ~~> tryHead ~~> tryTail ~~> tryTail ~~> tryHead


nubBy' :: (a -> a -> Bool) -> [a] -> [a]
nubBy' _ [] = []
nubBy' eq (x:xs) = x : nubBy' eq (filter (not . eq x) xs)


quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = quickSort' (filter (<= x) xs) ++ [x] ++ quickSort' (filter (> x) xs)


weird':: [[Int]] -> Int
weird' xs = foldr' ((+) . snd) 0 $ filter (even . length . fst) $ zip (map' (filter ((> 10) . abs)) xs) $ map' length xs


type File = (String, [String])


grep' :: (String -> [String] -> [String]) -> (String -> Bool) -> [File] -> [String]
grep' format match files = concat' $ map' (\ file -> format (fst file) (filter match (snd file))) files


isSubstringOf :: String -> String -> Bool
isSubstringOf n s = pack n `isInfixOf` pack s


grepSubstringNoFilename :: String -> [File] -> [String]
grepSubstringNoFilename needle = grep' (\ _ s -> s) $ isSubstringOf needle
 

grepExactMatchWithFilename :: String -> [File] -> [String]
grepExactMatchWithFilename needle = grep' (\ fn -> map' ((fn ++ [':']) ++ )) (needle == )
