'''
Created on 09.01.2021

MIT License

Copyright (c) 2021 Maxim Gansert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@autor: Maxim Gansert, Mindscan
'''

import unittest
from . import tokenizer



class Test(unittest.TestCase):

    def testTokenize_Empty_expectEmptyGenerator(self):
        tokens = tokenizer.tokenize('')
        self.assertEqual(next(tokens, None), None)
        
    def testTokenize_SeparatorSemicolon_expectSeperatorSemicolon(self):
        tokens = tokenizer.tokenize(";")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Separator ";"'])
        
    def testTokenize_SeparatorDot_expectSeperatorDot(self):
        tokens = tokenizer.tokenize(".")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Separator "."'])
        
    def testTokenize_SeparatorComma_expectSeperatorComma(self):
        tokens = tokenizer.tokenize(",")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Separator ","'])

    def testTokenize_SeparatorOpenParentheses_expectSeperatorOpen(self):
        tokens = tokenizer.tokenize("(")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Separator "("'])
        
    def testTokenize_SeparatorCloseParentheses_expectSeperatorClose(self):
        tokens = tokenizer.tokenize(")")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Separator ")"'])
        
    def testTokenize_SeparatorOpenCurlyBraces_expectSeperatorOpen(self):
        tokens = tokenizer.tokenize("{")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Separator "{"'])
        
    def testTokenize_SeparatorCloseCurlyBraces_expectSeperatorClose(self):
        tokens = tokenizer.tokenize("}")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Separator "}"'])
        
        
    def testTokenize_IntegerZero_expectIntegerZero(self):
        tokens = tokenizer.tokenize("0")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "0"'])

    def testTokenize_IntegerOne_expectIntegerOne(self):
        tokens = tokenizer.tokenize("1")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "1"'])

    def testTokenize_IntegerTwo_expectIntegerTwo(self):
        tokens = tokenizer.tokenize("2")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "2"'])
        
    def testTokenize_IntegerThree_expectIntegerThree(self):
        tokens = tokenizer.tokenize("3")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "3"'])
        
    def testTokenize_IntegerFour_expectIntegerFour(self):
        tokens = tokenizer.tokenize("4")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "4"'])

    def testTokenize_IntegerFive_expectIntegerFive(self):
        tokens = tokenizer.tokenize("5")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "5"'])

    def testTokenize_IntegerSix_expectIntegerSix(self):
        tokens = tokenizer.tokenize("6")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "6"'])

    def testTokenize_IntegerSeven_expectIntegerSeven(self):
        tokens = tokenizer.tokenize("7")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "7"'])

    def testTokenize_IntegerEight_expectIntegerEight(self):
        tokens = tokenizer.tokenize("8")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "8"'])

    def testTokenize_IntegerNine_expectIntegerNine(self):
        tokens = tokenizer.tokenize("9")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "9"'])

    def testTokenize_OperatorAssign_expectOperatorAssign(self):
        tokens = tokenizer.tokenize("=")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Operator "="'])

    def testTokenize_IdentifierA_expectIdentifierA(self):
        tokens = tokenizer.tokenize("a")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "a"'])

    def testTokenize_IdentifierE_expectIdentifierE(self):
        tokens = tokenizer.tokenize("e")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "e"'])
        
    def testTokenize_IdentifierI_expectIdentifierI(self):
        tokens = tokenizer.tokenize("i")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "i"'])
        
    def testTokenize_WhiteSpace_expectEmptyGenerator(self):
        tokens = tokenizer.tokenize(" ")
        self.assertEqual(next(tokens, None), None)
        
    def testTokenize_TabWhiteSpace_expectEmptyGenerator(self):
        tokens = tokenizer.tokenize("\t")
        self.assertEqual(next(tokens, None), None)

    def testTokenize_NewlineWhiteSpace_expectEmptyGenerator(self):
        tokens = tokenizer.tokenize("\n")
        self.assertEqual(next(tokens, None), None)
        
    def testTokenize_MultipleWhitespace1_expectEmptyGenerator(self):
        tokens = tokenizer.tokenize("\n\t\t     \n\n\t\t\n")
        self.assertEqual(next(tokens, None), None)
        
    def testTokenize_MultipleWhitespace2_expectEmptyGenerator(self):
        tokens = tokenizer.tokenize("     \n\t\t  \n \n\t   \t\n")
        self.assertEqual(next(tokens, None), None)

    def testTokenize_NopMethodCall_expectOneIdentifierAndTwoSeparators(self):
        tokens = tokenizer.tokenize("nop()")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "nop"', 'Separator "("', 'Separator ")"'])
        
    def testTokenize_AlwaysMethodCall_expectOneIdentifierAndTwoSeparators(self):
        tokens = tokenizer.tokenize("always()")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "always"', 'Separator "("', 'Separator ")"'])
        
    def testTokenize_AlwaysMethodCallPreceededBySpace_expectOneIdentifierAndTwoSeparators(self):
        tokens = tokenizer.tokenize(" always()")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "always"', 'Separator "("', 'Separator ")"'])

    def testTokenize_AlwaysMethodCallPreceededByWhiteSpaces_expectOneIdentifierAndTwoSeparators(self):
        tokens = tokenizer.tokenize("\t always()")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "always"', 'Separator "("', 'Separator ")"'])

    def testTokenize_AlwaysMethodCallFollowedByWhiteSpace_expectOneIdentifierAndTwoSeparators(self):
        tokens = tokenizer.tokenize("always ()")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "always"', 'Separator "("', 'Separator ")"'])
        
    def testTokenize_AlwaysMethodCallFollowedByEmptyDataBody_expectOneIdentifierAndFourSeparators(self):
        tokens = tokenizer.tokenize("always (){ }")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "always"', 'Separator "("', 'Separator ")"', 'Separator "{"', 'Separator "}"' ])
        
        
    def testTokenize_FourtyFour_expectOneInteger(self):
        tokens = tokenizer.tokenize("44")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "44"'])

    def testTokenize_FiftyFive_expectOneInteger(self):
        tokens = tokenizer.tokenize("55")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Integer "55"'])
        
    def testTokenize_True_expectBooleanTrue(self):
        tokens  = tokenizer.tokenize('True')
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Boolean "True"'])
    
    def testTokenize_False_expectBooleanFalse(self):
        tokens  = tokenizer.tokenize('False')
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Boolean "False"'])

    def testTokenize_None_expectNONE(self):
        tokens  = tokenizer.tokenize('None')
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['NONE "None"'])
    
    def testTokenize_IdentifierContainingANumber_expectOneIdentifier(self):
        tokens  = tokenizer.tokenize('test3')
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['Identifier "test3"'])

    def testTokenize_StringInSingleQuote_expectString(self):
        tokens  = tokenizer.tokenize("'test3'")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['String "\'test3\'"'])
        
    def testTokenize_StringInSingleQuoteContainingSpace_expectString(self):
        tokens  = tokenizer.tokenize("'test 3'")
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['String "\'test 3\'"'])
        
    def testTokenize_StringInDoubleQuote_expectString(self):
        tokens  = tokenizer.tokenize('"test3"')
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['String ""test3""'])

    def testTokenize_StringInDoubleQuoteContainingSpace_expectString(self):
        tokens  = tokenizer.tokenize('"test 3"')
        stokens = [str(token) for token in tokens]
        self.assertEqual(stokens,['String ""test 3""'])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()