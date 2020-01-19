module Exercises where  -- Вспомогательная строчка, чтобы можно было использовать функции в других файлах.
import Control.Arrow
import Data.Char
import Data.Text(isInfixOf, pack)
import Prelude hiding (sum, concat, foldr, map)
{- HLINT ignore "Use foldr" -}


sum' :: [Int] -> Int
sum' = sum'' 0

sum'' :: Int -> [Int] -> Int
sum'' ini [] = ini
sum'' ini (x:xs) = ini + x + (sum'' 0 xs)


concat' :: [[a]] -> [a]
concat' = concat'' []

concat'' :: [a] -> [[a]] -> [a]
concat'' ini (x:[]) = (x ++ ini)
concat'' ini (x:y:xs) = concat'' ini ((x ++ y):xs)


p :: Int
p = 17

hash' :: String -> Int
hash' = hash'' 0

hash'' :: Int -> String -> Int
hash'' ini [] = ini
hash'' ini (x:xs) = (ord x) + p * (hash'' ini xs)


foldr' :: (a -> b -> b) -> b -> [a] -> b
foldr' f ini (x:[]) = f x ini
foldr' f ini (x:xs) = f x (foldr' f ini xs)


map' :: (a -> b) -> [a] -> [b]
map' f [] = []
map' f (x:xs) = (f x):(map' f xs)


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
thirdElementOfSecondList xs = case tryTail xs of 
	                                 Just xss -> thirdElementOfFirstList xss 
	                                 Nothing  -> Nothing
	                          where thirdElementOfFirstList xss = case tryHead xss of
	                             	                                   Just x  -> thirdElement x
	                             	                                   Nothing -> Nothing
                                	thirdElement xs = case tryTail xs of
                                                         Just a  -> secondElement a
                                                         Nothing -> Nothing


fifthElement :: [a] -> Maybe a
fifthElement xs = element 4 xs
               where 
               	element 0 xs = tryHead xs
               	element num xs = case tryTail xs of
               		                  Just xs -> element (num - 1) xs
               		                  Nothing -> Nothing


(~~>) :: Maybe a -> (a -> Maybe b) -> Maybe b
(~~>) ma f = case ma of 
	              Just ma -> f ma
	              Nothing -> Nothing


thirdElementOfSecondList' :: [[a]] -> Maybe a
thirdElementOfSecondList' xs = (element 1 xs) ~~> (element 2)
              where
               	element 0 xs = tryHead xs
               	element num xs = case tryTail xs of
               		                  Just xs -> element (num - 1) xs
               		                  Nothing -> Nothing


nubBy' :: (a -> a -> Bool) -> [a] -> [a]
nubBy' eq [] = []
nubBy' eq (x:xs) = (x:nubBy' eq (filter' (eq x) xs))
           where 
           	filter' f [] = []
           	filter' f (x:xs) | f x = filter' f xs
           	                 | otherwise = (x:filter' f xs)


quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' (x:xs) = (quickSort' (filter (<= x) xs)) ++ [x] ++ (quickSort' (filter (>x) xs))


weird':: [[Int]] -> Int
weird' [] = 0
weird' xs = foldr' ((+) . snd) (0) (filter (even . length . fst) (zip (map' (filter ((> 10) . abs)) xs) (map' length xs)))


type File = (String, [String])


grep' :: (String -> [String] -> [String]) -> (String -> Bool) -> [File] -> [String]
grep' format match (file:[]) = (format (fst file) (filter match (snd file)))
grep' format match (file:files) = (format (fst file) (filter match (snd file))) ++ (grep' format match files)


isSubstringOf :: String -> String -> Bool
isSubstringOf n s = pack n `isInfixOf` pack s


grepSubstringNoFilename :: String -> [File] -> [String]
grepSubstringNoFilename needle files = grep' (\ _ s -> s) (isSubstringOf needle) files
 

grepExactMatchWithFilename :: String -> [File] -> [String]
grepExactMatchWithFilename needle files = grep' (\ fn s -> map' ((fn ++ [':']) ++ ) s) (needle == ) files
