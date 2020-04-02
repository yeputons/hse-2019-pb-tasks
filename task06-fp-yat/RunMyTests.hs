{-# LANGUAGE ScopedTypeVariables #-}
import Yat
import Test.HUnit
import System.Exit

check name a b = TestLabel name $ TestCase $ assertEqual "" a b
group name elems = TestLabel name $ TestList elems

(/+) = BinaryOperation Add
(/*) = BinaryOperation Mul
--(/-) = BinaryOperation Sub
--(|||) = BinaryOperation Or
--(===) = BinaryOperation Eq
--iff = Conditional
(=:=) = Assign
c = Number
r = Reference
call = FunctionCall

infixl 6 /+
--infixl 6 /-
infixl 7 /*
--infixr 2 |||
--infix 4 ===
infixr 1 =:=

program3 = (
    [
        ("f", ["param1", "param2"],
            Block [
            "a" =:= r "a" /+ c 1,
            "param1" =:= r "param1" /+ c 1,
            r "a" /* c 100 /+ r "b" /* c 10 /+ r "param1"
            ]
        )
    ],
    Block [
        "a" =:= c 2,
        "b" =:= c 7,
        "res" =:= call "f" [BinaryOperation Add (c 1) (UnaryOperation Not ("a" =:= c 7)), ("a" =:= c 3)],
        "b" =:= r "b" /+ c 1,
        r "res" /* c 100 /+ r "b" /* c 10 /+ r "a"
    ]
 )

testAll = TestList [
    group "program3" [
      check "output" (showProgram program3) $ concat [
        "func f(param1, param2) = {\n",
        "\tlet a = (a + 1) tel;\n",
        "\tlet param1 = (param1 + 1) tel;\n",
        "\t(((a * 100) + (b * 10)) + param1)\n",
        "}\n",
        "{\n",
        "\tlet a = 2 tel;\n",
        "\tlet b = 7 tel;\n",
        "\tlet res = f((1 + !let a = 7 tel), let a = 3 tel) tel;\n",
        "\tlet b = (b + 1) tel;\n",
        "\t(((res * 100) + (b * 10)) + a)\n",
        "}"
      ],
      check "result" (eval program3) $ 47283
    ]
  ]

main = do
  results <- runTestTT testAll
  exitWith $ if errors results + failures results == 0 then ExitSuccess else ExitFailure 1

