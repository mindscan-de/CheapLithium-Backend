'''
Created on 14.01.2021

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
SRC_BASE_DIR  = '../../../../../src'

import sys
sys.path.insert(0,SRC_BASE_DIR)

import importlib

from de.mindscan.cheaplithium.parser.ast import Apply, Literal, Env, DictSelector, MethodDeclaration

# interpreterrun = (tree, 'de.mindscan.cheaplithium.vm', 'transitions', {} )

def eval_transition(ast, package, module, environment:dict ):
    dynamic_module = importlib.import_module('.'+module, package=package)
    
    if isinstance(ast, MethodDeclaration):
        func = getattr(dynamic_module, ast.name)
        arguments = eval_ll( ast.parameters, environment )
        
        # TODO check, whether this is really needed...
        if arguments is None:
            arguments=[]
            
        return func(*arguments)
    ## restart implementation for AST
    elif isinstance(ast, Apply):
        print(str(ast))
        function_name = eval_ll(ast.name, environment)
        arguments = eval_ll(ast.arguments, environment)
        
        func = getattr(dynamic_module, function_name)
        
        return func(*arguments)
    
    else:
        raise Exception("eval_transition can't evaluate {}: (NYI) please implement this type!".format(type(ast)))

# eval lithium language
def eval_ll( ast, environment):
    if ast is None:
        return None
    
    elif isinstance(ast,Literal):
        return ast.value
    
    elif isinstance(ast, DictSelector):
        index = eval_ll(ast.index,environment)
        return lambda theDict:theDict[index]
    
    elif isinstance(ast, Env):
        if(ast.selector==None):
            return environment
        
        selector = eval_ll(ast.selector, environment)
        return selector(environment)
    
    elif isinstance(ast, list):
        evaluatedList = []
        for element in ast:
            result = eval_ll(element, environment)
            evaluatedList.append( result )
        return evaluatedList 
    
    
    raise Exception("eval_ll can't evaluate {}: (NYI) please implement this type!".format(type(ast)))
    