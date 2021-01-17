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
from de.mindscan.cheaplithium.parser.tokenizer import EndOfInput, Separator

 

'''
=================================
First basic idea for this grammar
=================================

Even though the grammar allows more by syntax, the parser (validation) will take care of it, or not...
Maybe i will rewrite this whole parser, if i need to support Expressions with oerations and parentheses...
This version is good enough for now...

-------------------------------------------------------------------------
First layout of this parser. I might rewrite this parser in the future... 
-------------------------------------------------------------------------

Model:
    guard=LLGuard ( body=LLMethodBody )?  
;

LLGuard:
    expr = LLExpression
;

LLMethodBody:
    {LLMethodBody} '{'    statements+=LLStatement* '}'
;

LLStatement:
    LLExpression ';'
;

LLExpression: LLAssignment;

LLAssignment returns LLExpression:
    LLSelectionExpression 
    ( 
        {LLAssignment.left = current} '=' right=LLExpression
    )?
;

LLSelectionExpression returns LLExpression:
    LLTerminalExpression 
    (
        {LLMemberSelection.receiver=current} '.' member=ID
        (
            methodinvocation?='(' 
                    (args+=LLExpression (',' args+=LLExpression)* )?
                ')'
        )?
    )*
;

LLTerminalExpression returns LLExpression:
    {LLStringLiteralConstant} value=STRING |
    {LLIntConstant} value=INT |
    {LLBooleanConstant} value= ('True' | 'False') |
    {LLThis} 'this' |
    {LLEnv} 'env' |
    {LLNone} 'None' |
    {LLRef} symbol=ID 
;

'''

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
        # create a lookAheadBuffer for the tokens, 
        #   and a nonexisting token is a EndOfInput-LithiumToken 
        
        # parse data_processing_function
        # {optional] parse data_transfer_body
        
        pass


    def parse_data_transfer_body(self):
        # TODO: use an AST element
        # a data_transferbody contains a list of assignments
        data_transfer_body = None
        
        currentToken = EndOfInput("")
        if isinstance( currentToken, EndOfInput ):
            return data_transfer_body
        
        
        # check if next is Separateor."{" -- otherwise is parser error
        # consume Separator."{" -- this can actually check
        parser_error=None
        if not isinstance( currentToken, Separator) or not currentToken.token_value.equals("{"):
            return parser_error;
        
        
        # while tokens avail (!=EndOfInput)
        #  if token is Separator."}" - consume - return data transfer_body
        #  assignment = parseDataAssignment()
        #  
        
        currentToken = EndOfInput("")
        if not isinstance(currentToken, EndOfInput):
            # unexpected tokens after body close
            # everything else should be ignored?
            return data_transfer_body
        
        
        return data_transfer_body