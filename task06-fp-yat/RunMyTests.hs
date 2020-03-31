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

infixl 6 /+
infixr 1 =:=

program1 = (
    [
        ("f", ["param"],
            Block [
                "param" =:= r "param" /+ c 1,
                 r "param"
            ]
        )
    ],
    Block [
        "param" =:= c 2,
        "res" =:= call "f" [c 0],
        r "param"
    ]
 )
testAll = TestList [
    group "program1" [
      checkGE "result" (eval program1) $  2
    ]
  ]

main = do
  results <- runTestTT testAll
  exitWith $ if errors results + failures results == 0 then ExitSuccess else ExitFailure 1