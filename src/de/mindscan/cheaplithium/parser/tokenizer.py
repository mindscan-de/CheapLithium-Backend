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

import re

## TODO: DecisionLanguageLexxer will output tokens for an input string lexxer is based on regexes...
## TODO: DecisionLanguageTokenzer will use the Lexxer to provide tokens

## TODO: don't make it too fancy... for now i use regexes, but they aren't 
##       sufficient enough, because i want to extract some information from 
##       the AST, like input descriptions from the node, and transitiion 
##       signatures....
## TODO: also want to provide the users with help, and code completion later on.


# This are the token types for the lithium language
# A token has a value and has a tokentype, the tokentype

# ####################################
# Lithium Language Tokentypes
# ####################################

class LithiumToken(object):
    def __init__(self, tokenValue):
        self.token_value = tokenValue
    
    def __repr__(self):
        return '{} "{}"'.format(self.__class__.__name__, self.token_value)
    
    def __str__(self):
        return self.__repr__()


class EndOfInput(LithiumToken):
    pass

class Literal(LithiumToken):
    pass

# for nonfractional numbers    
class Integer(Literal):
    pass

# for Strings
class String(Literal):
    pass

class Boolean(Literal):
    SETOF = set(['True', 'False'])

# for None / Null
class NONE(Literal):
    pass

class Operator(LithiumToken):
    SETOF = set(['='])

class Separator(LithiumToken):
    SETOF = set([';', '.', ',', '(', ')'])

# Names of variables, methods, environments
class Identifier(LithiumToken):
    pass

# ########################################
# Lithium Language Tokenizer
# ########################################

def tokenize(code: str):
    tokenizer = LithiumTokenizer(code)
    return tokenizer.tokenize()

class LithiumTokenizer(object):
    def __init__(self, code):
        self.code = code
        self.codeLength = len(self.code)
        
    # tokenstart is the character position, where we will start with a new token
    # tokenend is the current character position, we are going to read and analyze,
    # the real token is between these positions, but excluding the end position  
    def reset(self):
        self.tokenstart = 0
        self.tokenend = 0
    
    def tokenize(self):
        self.reset()
        
        while self.tokenstart < self.codeLength:
            # be optimistic and start with a tokenlength of one
            self.tokenend = self.tokenstart+1
            
            currentChar = self.code[self.tokenstart]
            
            # whitespace
            if(self.isStartOfWhitespace(currentChar)):
                self.consumeWhitespaces()
                continue
                
            
            # TODO: comments?        
            
            currentTokenType = None
            if(currentChar in Separator.SETOF):
                currentTokenType = Separator
            elif(currentChar in '0123456789'):
                currentTokenType = Integer
            elif(currentChar in Operator.SETOF):
                currentTokenType = Operator
            elif(self.isStartOfIdentifier(currentChar)):
                currentTokenType = Identifier

            # if we can not identify that particular token
            if(currentTokenType is None):
                # skip that sh$t and yield nothing
                self.tokenstart = self.tokenend
                continue
            
            currentGeneratedToken = currentTokenType(self.code[self.tokenstart:self.tokenend])
            yield currentGeneratedToken
        
            # the start of the new token is the end of the current token
            self.tokenstart = self.tokenend
            
        return None

    def isStartOfIdentifier(self, char):
        return re.match(r'^\w+$', char)
    
    def isStartOfWhitespace(self, char):
        return re.match(r'^\s+$', char)
    
    def consumeWhitespaces(self):
        
        
        # skip until nonwhitespace found.
        self.tokenstart = self.tokenend
        return 