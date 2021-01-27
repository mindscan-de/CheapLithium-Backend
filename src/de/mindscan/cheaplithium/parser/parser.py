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

from de.mindscan.cheaplithium.parser.ast import VMLithiumCompileUnit,  DictSelector, Literal, VMApply, VMBody, VMPrimary
from de.mindscan.cheaplithium.parser.tokenizer import EndOfInput, Separator, Boolean

# ##############################
# Simple Interface to the parser
# ##############################

def parse(tokens):
    parser = LithiumParser(tokens)
    return parser.parse()

 

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

# TODO: then we need some DecisionLanguageParser - Call it "LithiumParser"?
# TODO: takes the tokens and parses them into an AST
# TODO: the AST then can be executed, and interpreted in different ways, such 
#       that the same "code" has different meanings, eg. as e.g as 
#       INPUT-specification, initialization, guard, etc, it is so much more flexible...
# TODO: but someone must write it...  


class LATokenIterator(object):
    
    def __init__(self, iterable):
        self.list = list(iterable)
        self.current_position = 0
        self.default_token = None
        self.value = None
    
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
            raise StopIteration
        
        return self.value
    
    def lookahead(self, skip_count=0):
        try:
            self.value = self.list[self.current_position + skip_count]
        except IndexError:
            return self.default_token
        
        return self.value
    

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
        
        # if tokens are empty, we don't need to invoke the parser any more... Just saying. 
        if False:
            return None;
        
        return self.parseVMLithiumCompileUnit()

#
#
#
#

    
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
        
        # TODO: if next token in first-Menge then
        if True: 
            guard = self.parseLLMethodInvocation( )
        
        # TODO: if next token is in FirstMenge '{'
        if True:
            if self.try_accept(Separator('{')):
                body = self.parseVMBody()
                self.accept(Separator('}'))
            
        return VMLithiumCompileUnit( guard = guard, body = body)

    '''
    VMBody:
        {VMBody} '{' statements+=LLStatement* '}'
    ;
    '''
    def parseVMBody(self):
        statements = []
        
        while(True):
            # peek
            
            # TODO: if next token is followmenge of VMMody ( '}' )
            if False:
                break
            
            # TODO: if next token is end of input -> raise exception
            if False:
                pass
            
            statement = self.parseLLStatement()
            if not statement is None:
                statements.append(statement)
        
        return VMBody(statements = statements)


    '''
    LLStatement:
        LLExpressionStatement ';'
    ;
    '''
    def parseLLStatement(self):
        expressionStatement = self.parseLLExpressionStatement
        
        # if next token is FOLLOW MENGE of parseLLStatement (';')
        if True:
            # TODO: consume ';'
            return expressionStatement;
        else:
            # raise exception, that we were expecting the follow 
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

        # we may have to store a marker so we can return, if we parsed it the wrong way.        
        try:
            assignment = self.parseLLAssignment()
            return assignment
        except:
            pass
        
        # we may have to restore the position now, so we can return the expression.
        try:
            expression = self.parseLLExpression()
            return expression
        except:
            pass
        
        raise Exception ("This should eithe be an assigment or an Expression.")
    

    '''
    TODO: implement the rule
    LLAssignment:
        PrimaryAndSelection
        (
            {LLAssignment.left=current} '=' right=LLExpression 
        )
    ;
    '''
    def parseLLAssignment(self):
        current = self.parsePrimaryAndSelection()
        
        # TODO if next token is '='
        if True:
            # TODO consume '='
            
            _sleft = current
            right = self.parseLLExpression()
            
            # TODO: create an assignment node, otherwise we will return the right 
            #       value instead...
            return right
        
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
        
        # TODO: if next is '('
        if True:
            # TODO consume '('
            
            func = current
            arguments = []
            
            #TODO
            # (args+=LLExpression (',' args+=LLExpression)* )
            
            # TODO CHECK if ')'
            if True:
                return VMApply(func = func, arguments = arguments)
                
            return VMApply(func = func, arguments = arguments)
        
        return current
    
    
    '''
    PrimaryAndSelection returns Expression:
        LLMemberSelection    
    ;
    '''
    def parsePrimaryAndSelection(self):
        return self.parseLLMemberSelection
    
    
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
        
        # TODO: tryconsume '.'
        if True:
            selectors=[]
            
            # TODO parse the selector and create a DictSelectorNode
            
            return VMPrimary(value = current, selector = selectors)
        pass
    
    
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
        if self.tryAndAcceptType( Boolean ):
            boolean = next(self.tokens)
            return Literal(value = (boolean.token_value == 'True'))
        else:
            raise Exception("can not parse the current token.")
    
    def tryAndAccept(self, acceptableToken):
        la = self.tokens.lookahead()
        
        if not (la.token_value == acceptableToken ):
            return False
        
        next(self.tokens)
        return True

    def tryAndAcceptType(self, acceptableType):
        la = self.tokens.lookahead()
        
        if isinstance(la,acceptableType):
            return True
            
        return False
            
    
    # #######################
    # OBSOLETE ?
    # #######################

    def parse_guard(self):
        
        selector = DictSelector(index=Literal(value='always'))
        name = Literal(value='transitions', selector=selector )
        return VMApply(func=name, arguments=None)


    
    def try_accept(self, *accepted_tokens):
        return False




    # Doesnt't work
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