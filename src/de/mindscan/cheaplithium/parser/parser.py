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

from de.mindscan.cheaplithium.parser.ast import VMLithiumCompileUnit,  VMApply, VMBody, VMPrimary, VMAssignment
from de.mindscan.cheaplithium.parser.ast import Env, This, Literal 

from de.mindscan.cheaplithium.parser import tokenizer
from de.mindscan.cheaplithium.parser.tokenizer import EndOfInput, Boolean, Integer, NONE, Identifier,\
    KeyWordIdentifier, String

# ##############################
# Simple Interface to the parser
# ##############################

def parseToAst(code):
    return _parserHelper(code).parse()

def _parserHelper(code):
    tokens = tokenizer.tokenize(code)
    return LithiumParser(tokens)


'''
=================================
First basic idea for this grammar
=================================

We don't need something perfect, but we need something, which is good enough.

(Currently testing alternate grammars with xtext)

Even though the grammar allows more by syntax, the parser (validation) will take care of it, or not...
Maybe i will rewrite this whole parser, if i need to support Expressions with oerations and parentheses...
This version is good enough for now...

-------------------------------------------------------------------------
First layout of this parser. I might rewrite this parser in the future... 
-------------------------------------------------------------------------

Model:
    {Model} model = (VMLithiumCompileUnit)?
;


VMLithiumCompileUnit:
    {VMLithiumCompileUnit} guard = LLMethodInvocation ( body = VMBody )?
;


VMBody:
    {VMBody} '{' statements+=LLStatement* '}'
;

    
LLStatement:
    LLExpressionStatement ';'
;


LLExpressionStatement:
    LLAssignment |
    LLExpression
;


LLAssignment:
    PrimaryAndSelection
    (
        {LLAssignment.left=current} '=' right=LLExpression 
    )
;


LLExpression returns Expression:
    LLMethodInvocation
;


LLMethodInvocation returns Expression:
    PrimaryAndSelection
    (
        {LLMethodInvocation.func=current} '(' (args+=LLExpression (',' args+=LLExpression)* )? ')'
    )?
;


PrimaryAndSelection returns Expression:
    LLMemberSelection    
;


LLMemberSelection returns Expression:
    LLLiteral
    (
        {LLMemberSelection.value=current} '.' (selector+=ID ('.' selector+=ID)*)
    )?
;


LLLiteral returns Expression:
    {LLStringLiteral} value = STRING |
    {LLIntegerLiteral} value = INT |
    {LLBooleanLiteral} value = ('True' | 'False') |
    {LLNoneLiteral} value = 'None' |
    {LLEnv} 'env' |
    {LLThis} 'this' |
    {LLRef} value=ID
;


This can parse the following:

*  (empty) 
*  always()
*  always() {}
*  transitions.always() {}
*  transitions.isTrue(True) {}
*  transitions.isFalse(False) {}
*  transitions.isLessThan(10,20) {}
*  transitions.isLessThan(env.result,20) {}
*  transitions.isLessThan(env.result, env.x.y) {}
*  transitions.isLessThan(env.result.y, env.x.y, env) {}
*  transitions.foo.isLessThan(env.y, env.x.y, env) {}
*  transitions.isEqualTo(env.result, "myvalue") {}
*  transitions.isEqualTo(env.result, 'myvalue') {}
*  transitions.isLessThan(env.result.y, commons.a()) {}
*  commons.foo() {
                    inputui.user_textfield("myLabel","myDescription") ;
                }
*  commons.foo() {
                    inputui.user_textfield("myLabelTF","myTFDescription ") ;
                    inputui.user_textarea("myLabelTA","myTADescription") ;
                    inputui.user_yesnoselection("myLabelYN","myYNDescription") ;
                }
*  commons.foo() {
                    env.x = env.y;
                }
*  commons.foo() {
                    env.x = env.y();
                }
*  commons.foo() {
                    env.x = inputui.user_yesnoselection("myLabelYN","myYNDescription");
                }

** THIS will fail (as expected) :
*  commons.foo() {
                    env.x() = env.y;
                }

Can not parse right now...:

*  expressions with operators <-- (ato de)

'''

# --------------------------------------------------------------
# Some additional Infrastructure code to handle the token stream
# --------------------------------------------------------------

class LATokenIterator(object):
    
    def __init__(self, iterable):
        self.list = list(iterable)
        self.current_position = 0
        self.default_token = None
        self.value = None
        self.marked_position = None
    
    def __iter__(self):
        return self
    
    def set_default(self, default_token ):
        self.default_token = default_token
        
    def last(self):
        return self.value

    def next(self):
        return self.__next__()
    
    def __next__(self):
        try:
            self.value = self.list[self.current_position]
            self.current_position += 1
        except IndexError:
            raise StopIteration()
        
        return self.value
    
    def lookahead(self, skip_count=0):
        try:
            self.value = self.list[self.current_position + skip_count]
        except IndexError:
            return self.default_token
        
        return self.value
    
    def pushmarker(self):
        self.marked_position = self.current_position
    
    def popmarker(self):
        if not self.marked_position is None:
            self.current_position = self.marked_position
        else:
            raise Exception("Popmaker with invalid state.")
    
    def discardmarker(self):
        self.marked_position = None

class LithiumParser(object):
    
    def __init__(self, tokens):
        self.tokens = LATokenIterator(tokens)
        self.tokens.set_default(EndOfInput(None))
    
    '''
    Model:
        {Model} model = (VMLithiumCompileUnit)?
    ;
    '''
    def parse(self):
        return self.parseVMLithiumCompileUnit()


# ----------------------------------------------------------------------------
# Parser Rules implementation
# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
    
    '''
    VMLithiumCompileUnit:
        {VMLithiumCompileUnit} guard = LLMethodInvocation ( body = VMBody )?
    ;
    '''
    def parseVMLithiumCompileUnit(self):
        guard = None
        body = None
        
        # if end of input - return empty VMLithumCompileUnit
        if self.tryType(EndOfInput):
            return VMLithiumCompileUnit( guard = guard, body = body)

        guard = self.parseLLMethodInvocation( )
        
        if self.tryAsString('{'):
            body = self.parseVMBody()
            
        return VMLithiumCompileUnit( guard = guard, body = body)

    '''
    VMBody:
        {VMBody} '{' statements+=LLStatement* '}'
    ;
    '''
    def parseVMBody(self):
        statements = []
        
        if self.tryAndConsumeAsString('{'):
            while True:
                if self.tryAndConsumeAsString('}'):
                    break
                
                # This must not consume the EndOfInput..
                if self.tryType(EndOfInput):
                    raise Exception("premature end of input. expected '}'")
                
                # TODO: Support multiple levels of '{'
                #if self.tryAsString('{'):
                #    statement = self.parseVMBody()
                #    statements.append(statement)
                
                # curent token is something different than stop set
                # parse as it were/is a statement
                try:
                    statement = self.parseLLStatement()
                    if not statement is None:
                        statements.append(statement)
                except:
                    raise Exception("ParserError..")
        
        return VMBody(statements = statements)


    '''
    LLStatement:
        LLExpressionStatement ';'
    ;
    '''
    def parseLLStatement(self):
        expressionStatement = self.parseLLExpressionStatement()
        
        if self.tryAndConsumeAsString(';'):
            return expressionStatement;
        else:
            raise Exception("Missing ';'")
        

    '''
    LLExpressionStatement:
        LLAssignment |
        LLExpression
    ;
    '''
    def parseLLExpressionStatement(self):
        if False:
            raise Exception ("We did not expect that token for a Expression Statement")

        # store the current position in the tokenstream
        self.tokens.pushmarker()        
        try:
            assignment = self.parseLLAssignment()
            # remove the marked position because we were successfull
            self.tokens.discardmarker()
            return assignment
        except:
            pass
        
        # restore the parser position from before the assignment
        self.tokens.popmarker()
        
        try:
            expression = self.parseLLExpression()
            return expression
        except:
            pass
        
        raise Exception ("This should eithe be an assigment or an Expression.")
    

    '''
    LLAssignment:
        PrimaryAndSelection
        (
            {LLAssignment.left=current} '=' right=LLExpression 
        )
    ;
    '''
    def parseLLAssignment(self):
        current = self.parsePrimaryAndSelection()
        
        if self.tryAndConsumeAsString('='):

            left = current
            right = self.parseLLExpression()
            
            return VMAssignment(left=left, right=right)
        else:
            raise Exception("an '=' was expected, but we might give it a second try in a different rule")
        
    '''
    LLExpression returns Expression:
        LLMethodInvocation
    ;
    '''
    def parseLLExpression(self):
        result = self.parseLLMethodInvocation()
        return result


    '''
    LLMethodInvocation returns Expression:
        PrimaryAndSelection
        (
            {LLMethodInvocation.func=current} '(' (args+=LLExpression (',' args+=LLExpression)* )? ')'
        )?
    ;
    '''
    def parseLLMethodInvocation(self):
        current = self.parsePrimaryAndSelection()
        
        if self.tryAndConsumeAsString('('):
            func = current
            arguments = []
            
            # ATTN must not consume token
            if not self.tryAsString(')'):
                argument = self.parseLLExpression()
                arguments.append(argument)
                
                # (args+=LLExpression (',' args+=LLExpression)* )
                while self.tryAndConsumeAsString(','):
                    argument = self.parseLLExpression()
                    arguments.append(argument)
                
            # Shall Consume token
            if self.tryAndConsumeAsString(')'):
                return VMApply(func = func, arguments = arguments)
            else:
                # something else than a ',' or ')'
                raise("We got something unexpected in pareLLMethodInvocation.")
            
        return current
    
    
    '''
    PrimaryAndSelection returns Expression:
        LLMemberSelection    
    ;
    '''
    def parsePrimaryAndSelection(self):
        return self.parseLLMemberSelection()
    
    
    '''
    LLMemberSelection returns Expression:
        LLLiteral
        (
            {LLMemberSelection.value=current} '.' (selector+=ID ('.' selector+=ID)*)
        )?
    ;    
    '''
    def parseLLMemberSelection(self):
        current = self.parseLLLiteral()
        
        if self.tryAndConsumeAsString('.'):
            selector = self.parseLLLiteral()
            
            while self.tryAndConsumeAsString('.'):
                # TODO Do we have an error here and shouldn't we have that 
                #      wrapped in a DictSelector? We will see in runtime later.  
                current = VMPrimary(value = current, selector = selector)
                selector = self.parseLLLiteral()
            
            return VMPrimary(value = current, selector = selector)
        
        return current
    
    '''
    LLLiteral returns Expression:
        {LLStringLiteral} value = STRING |
        {LLIntegerLiteral} value = INT |
        {LLBooleanLiteral} value = ('True' | 'False') |
        {LLNoneLiteral} value = 'None' |
        {LLEnv} 'env' |
        {LLThis} 'this' |
        {LLRef} value=ID
    ;
    '''
    def parseLLLiteral(self):
        if self.tryAndAcceptType( String ):
            string = self.tokens.last()
            return Literal( value = self.unescapeString(string.token_value))
        if self.tryAndAcceptType( Boolean ):
            boolean = self.tokens.last()
            return Literal(value = (boolean.token_value == 'True'))
        if self.tryAndAcceptType( Integer ):
            integer = self.tokens.last()
            return Literal(value = int(integer.token_value))
        if self.tryAndAcceptType( NONE ):
            return Literal(value = None)
        if self.tryType( KeyWordIdentifier ):
            if self.tryAndConsumeAsString('env'):
                return Env()
            elif self.tryAndConsumeAsString('this'):
                return This()
            #TODO: raise exception, that we don't know that keyword identifier
            kw_identifier=next(self.tokens)
            return Literal(value = kw_identifier.token_value)
        if self.tryAndAcceptType( Identifier ):
            identifier = self.tokens.last()
            return Literal(value = identifier.token_value)
        else:
            raise Exception("can not parse the current token.")
    
    
    # ##########################
    # Parser Intrastructure code
    # ##########################
    
    def tryAndAccept(self, acceptableToken):
        la = self.tokens.lookahead()
        
        if not (la.token_value == acceptableToken ):
            return False
        
        next(self.tokens)
        return True
    
    def tryAndConsumeAsString(self, acceptableToken):
        la = self.tokens.lookahead()
        
        if not (la.token_value == acceptableToken ):
            return False
        
        next(self.tokens)
        return True
    

    def tryAndAcceptType(self, acceptableType):
        la = self.tokens.lookahead()
        
        if not isinstance(la,acceptableType):
            return False
        
        next(self.tokens)
        return True
    
    def tryType(self, acceptableType):
        la = self.tokens.lookahead()
        
        if not isinstance(la,acceptableType):
            return False
            
        return True
    
    def tryAsString(self, acceptableToken):
        la = self.tokens.lookahead()
        
        if not (la.token_value == acceptableToken ):
            return False
        
        return True
        
            
    # TODO: handle escape sequences and such.
    # good enough until we need more.
    def unescapeString(self, string):
        return string[1:-1] 
    
