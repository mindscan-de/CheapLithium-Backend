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

from de.mindscan.cheaplithium.parser.ast import Literal, Env, DictSelector, VMModule, VMPrimary, VMApply, VMLithiumCompileUnit

# interpreterrun = (tree, 'de.mindscan.cheaplithium.vm', 'transitions', {} )

def eval_transition(compileunit, environment:dict ):
    
    if isinstance(compileunit, VMLithiumCompileUnit):
        guard_result = eval_ll(compileunit.guard, environment);
        if guard_result is False:
            # TODO: add a second retur result
            return guard_result  #TODO: reenable this ",None"
        
        # TODO: This result should contain the data which is added to the transition data.
        __body_result = eval_ll(compileunit.body, environment)
        # TODO: return a pair of returnresult (one for the result of the Guard and one for the result of the body
        return guard_result
          
    else:
        raise Exception("eval_transition can't evaluate {}: (NYI) please implement this type!".format(type(compileunit)))

    
# TODO: implement the way HIT-NODES are evaluated, (after the input is provided)
def eval_hit_node(compileunit, environment:dict, inputdata:dict):
    # use special runtime mode/class to influence behavior of inputui, 
    # the injected special runtime provides input data to the thread via inputui
    pass


# TODO: mode to calculate the input field from the compile unit
def eval_hit_render_input_interface(compileunit, environment:dict, inputdata:dict):
    ui_input_interface = []
    # TODO: we want to evaluate the body of the compile unit.
    # we want to render the nodes, which refer to the input.
    if isinstance(compileunit, VMLithiumCompileUnit):
        # TODO: use a special runtime mode/class to influence behavior of inputui, this class collects also the input interface
        # then get the data from collector and then return the collected data.        
        return ui_input_interface
    else:
        raise Exception()


# TODO: code to calculate the MIT nodes.
def eval_mit_node(ast, environment:dict):
    pass




# eval lithium language
def eval_ll( ast, environment, special_engine=None):
    if ast is None:
        return None
    
    elif isinstance(ast,Literal):
        return ast.value
    
    elif isinstance(ast, DictSelector):
        index = eval_ll(ast.index,environment, special_engine)
        return lambda theDict: theDict[index] if ( isinstance(theDict, dict) or isinstance(theDict, list) ) else getattr(theDict, index)
    
    elif isinstance(ast, Env):
        if(ast.selector==None):
            return environment
        
        selector = eval_ll(ast.selector, environment, special_engine)
        return selector(environment)
    
    elif isinstance(ast, list):
        evaluatedList = []
        for element in ast:
            result = eval_ll(element, environment, special_engine)
            evaluatedList.append( result )
        return evaluatedList
    
    elif isinstance(ast,VMModule):
        module_name = eval_ll(ast.name, environment, special_engine)
        themodule = importlib.import_module('.'+module_name, package='de.mindscan.cheaplithium.vm')
        
        ## TODO: maybe so..., such that the special engine may get injected.
        if special_engine:
            try:
                themodule.__set_engine(special_engine)
            except:
                pass
        
        return themodule
    
    elif isinstance(ast,VMPrimary):
        value = eval_ll(ast.value,environment, special_engine)
        if ast.selector is None:
            return value
        
        selector = eval_ll(ast.selector, environment, special_engine)
        return selector(value)
    
    elif isinstance(ast,VMApply):
        theFunction = eval_ll(ast.func, environment, special_engine)
        arguments = eval_ll(ast.arguments, environment, special_engine)
        if arguments is None:
            return theFunction()
        else:
            return theFunction(*arguments)
        
    
    raise Exception("eval_ll can't evaluate {}: (NYI) please implement this type!".format(type(ast)))
    