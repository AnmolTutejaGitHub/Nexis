module Main where

import Data.List (sort, nub, group)
import Data.Maybe (fromMaybe, mapMaybe)
import qualified Data.Map.Strict as Map

data Tree a = Leaf | Node (Tree a) a (Tree a)
    deriving (Show, Eq)

newtype Stack a = Stack { unStack :: [a] }
    deriving (Show)

type Frequency = Map.Map Char Int

insert :: Ord a => a -> Tree a -> Tree a
insert x Leaf = Node Leaf x Leaf
insert x (Node l v r)
    | x < v     = Node (insert x l) v r
    | x > v     = Node l v (insert x r)
    | otherwise = Node l v r

flatten :: Tree a -> [a]
flatten Leaf         = []
flatten (Node l v r) = flatten l ++ [v] ++ flatten r

push :: a -> Stack a -> Stack a
push x (Stack xs) = Stack (x : xs)

pop :: Stack a -> Maybe (a, Stack a)
pop (Stack [])     = Nothing
pop (Stack (x:xs)) = Just (x, Stack xs)

charFrequency :: String -> Frequency
charFrequency = Map.fromListWith (+) . map (\c -> (c, 1))

main :: IO ()
main = do
    let tree = foldr insert Leaf [5, 3, 7, 1, 4 :: Int]
    print (flatten tree)
