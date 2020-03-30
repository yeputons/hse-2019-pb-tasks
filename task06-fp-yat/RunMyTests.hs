{-# LANGUAGE ScopedTypeVariables #-}
import Yat
import Test.HUnit
import System.Exit

checkGE name got expected = TestLabel name $ TestCase $ assertEqual "" expected got
group name elems = TestLabel name $ TestList elems

(/+) = BinaryOperation Add
(=:=) = Assign
c = Number
r = Reference
call = FunctionCall

infixl 2 /+
infixr 1 =:=

programTestVariableAndArgumentTheSameName1 = (
    [
        ("foo", ["a", "b"], 
            r "b"
        )
    ], 
    Block [
        "a" =:= c 5, 
        call "foo" [r "a" /+ c 10, r "a"]
    ]
  )

programTestVariableAndArgumentTheSameName2 = (
    [
        ("foo", ["a", "b", "c"], 
            r "b"
        )
    ], 
    Block [
        "a" =:= c 5, 
        call "foo" [r "a" /+ c 10, r "a", r "a" /+ c 8]
    ]
  )

testAll = TestList [
    group "variable and argument has the same name" [
      checkGE "result" (eval programTestVariableAndArgumentTheSameName1) $ 5,
      checkGE "result" (eval programTestVariableAndArgumentTheSameName2) $ 5
    ]
  ]

main = do
  results <- runTestTT testAll
  exitWith $ if errors results + failures results == 0 then ExitSuccess else ExitFailure 1
