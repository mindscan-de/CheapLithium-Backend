'''
Created on 10.01.2021

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

from de.mindscan.cheaplithium.parser import parser
from de.mindscan.cheaplithium.parser import tokenizer
from de.mindscan.cheaplithium.parser.parser import LithiumParser


class Test(unittest.TestCase):


    def testParse_TransitionsAlwaysNoArgsNoBody_expectLitiumCompileUnitWithGuard(self):
        # arrange
        tokens = tokenizer.tokenize("transitions.always()")
        
        #act
        parsed_ast = parser.parse(tokens)
        
        #assert
        self.assertEqual(str(parsed_ast), 'VMLithiumCompileUnit(guard:VMApply(func:Literal(value:transitions, selector:DictSelector(index:Literal(value:always, selector:None))), arguments:None), body:None)')


    def testParseBody_TransitionsAlwaysNoARgumentsNoBody_expectTransition(self):
        # arrange
        tokens = tokenizer.tokenize("transitions.always()")
        
        #act
        parsed_ast = LithiumParser(tokens).parse_guard()
        
        #assert
        self.assertEqual(str(parsed_ast), 'VMApply(func:Literal(value:transitions, selector:DictSelector(index:Literal(value:always, selector:None))), arguments:None)')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()