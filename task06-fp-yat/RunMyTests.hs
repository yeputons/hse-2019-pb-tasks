{-# LANGUAGE ScopedTypeVariables #-}
import Yat
import Test.HUnit
import System.Exit

checkGE name got expected = TestLabel name $ TestCase $ assertEqual "" expected got
group name elems = TestLabel name $ TestList elems

(/+) = BinaryOperation Add
(/*) = BinaryOperation Mul
(/-) = BinaryOperation Sub
(|||) = BinaryOperation Or
(===) = BinaryOperation Eq
iff = Conditional
(=:=) = Assign
c = Number
r = Reference
call = FunctionCall

infixl 6 /+
infixl 6 /-
infixl 7 /*
infixr 2 |||
infix 4 ===
infixr 1 =:=

program1 = ([("foo", ["a", "b"], r "b")], Block ["a" =:= c 5, call "foo" [r "a" /+ c 10, r "a"]])

main = do
     exitWith $ if (eval program1) == 5 then ExitSuccess else ExitFailure 1