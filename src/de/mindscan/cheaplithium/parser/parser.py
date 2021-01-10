'''
Created on 08.01.2021

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

from . import tokenizer
from . import ast
 


# TODO: then we need some DecisionLanguageParser - Call it "LithiumParser"?
# TODO: takes the tokens and parses them into an AST
# TODO: the AST then can be executed, and interpreted in different ways, such 
#       that the same "code" has different meanings, eg. as e.g as 
#       INPUT-specification, initialization, guard, etc, it is so much more flexible...
# TODO: but someone must write it...  


def parse(tokens):
    parser = LithiumParser()
    return parser.parse(tokens)

class LithiumParser(object):
    def __init__(self):
        pass
    
    def parse(self, tokens):
        pass
