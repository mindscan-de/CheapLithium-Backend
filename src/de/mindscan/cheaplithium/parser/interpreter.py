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

from de.mindscan.cheaplithium.parser.ast import Literal, Env, DictSelector, This 
from de.mindscan.cheaplithium.parser.ast import VMModule, VMPrimary, VMApply, VMLithiumCompileUnit, VMBody, VMAssignment
from de.mindscan.cheaplithium.parser.SpecialEngine import SpecialEngine



def eval_transition(compileunit, environment:dict ):
    # use special Engine as part of the environment, where we decide what's a module
    special_engine = SpecialEngine()
    if isinstance(compileunit, VMLithiumCompileUnit):
        guard_result = eval_ll(compileunit.guard, environment, special_engine);
        if guard_result is False or guard_result is None:
            return False, {}
        
        eval_ll(compileunit.body, environment, special_engine)
        return guard_result, special_engine.getThis()
          
    else:
        raise Exception("eval_transition can't evaluate {}: (NYI) please implement this type!".format(type(compileunit)))


# TODO: the return of the environment and the data is the most important thing after the parsing, because this will 
#       make the lithium runtime engine update the runtime data / threadenvironment  

# TODO: return the environment after executing the HIT Node    
def eval_hit_node(compileunit, environment:dict, inputdata:dict):

    if isinstance(compileunit, VMLithiumCompileUnit):
        userinterface = eval_hit_render_input_interface(compileunit, environment)
        allowed_input_labels = [ x['label'] for x in userinterface ]
        
        ## filter input data, whether it is allowed dur to user interface         
        filtered_input_data = {}
        for input_label in allowed_input_labels:
            filtered_input_data[input_label] = inputdata[input_label]

        # inject the filtered form data into the thread
        special_engine = SpecialEngine()
        special_engine.setUserLabeledInput(filtered_input_data)
        
        # TODO: evaluate the compileunit guard?
        # eval_ll(compileunit.guard, environment, special_engine)
        
        # inject the filtered form inputdata data into the thread, by using the special engine
        eval_ll(compileunit.body, environment, special_engine)
    else:
        raise Exception("eval_hit_node can't evaluate {}: (NYI) please implement this type!".format(type(compileunit)))


# TODO: prevent the environment to change because we use (execute) this method as a  help to identify 
#       thevalues which are input data and which nit, because all other statements are exevuted too and
#       manipulate the environment. Therefore the environment may has to be firewalled...
#       make a deep copy of the environment first. 
def eval_hit_render_input_interface(compileunit, environment:dict):
    
    if isinstance(compileunit, VMLithiumCompileUnit):
        # enable the recording mode, for the user interface
        special_engine = SpecialEngine()
        special_engine.setInterfaceRenderMode(True)
        
        # TODO: should the guard be calcuated at all?
        # eval_ll(compileunit.guard, environment, special_engine)
        
        # record the user input interface into special engine, while execution
        eval_ll(compileunit.body, environment, special_engine)
        # replay user input interface after evaluation
        return special_engine.getInputInterface()
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
        if (special_engine != None) and (special_engine.isModuleName(ast.value)):
            # in case it is a module - wrap it with a vmmodule node
            return eval_ll( VMModule(name=ast.value), environment, special_engine )
             
        return ast.value
    
    elif isinstance(ast, DictSelector):
        index = eval_ll(ast.index,environment, special_engine)
        return lambda theDict: theDict[index] if ( isinstance(theDict, dict) or isinstance(theDict, list) ) else getattr(theDict, index)
    
    elif isinstance(ast, Env):
        if(ast.selector==None):
            return environment
        
        selector = eval_ll(ast.selector, environment, special_engine)
        return selector(environment)
    
    elif isinstance(ast,This):
        if(ast.selector == None):
            return special_engine.getThis()
    
    elif isinstance(ast, list):
        evaluatedList = []
        for element in ast:
            result = eval_ll(element, environment, special_engine)
            evaluatedList.append( result )
        return evaluatedList
    
    elif isinstance(ast, VMBody):
        for element in ast.statements:
            result = eval_ll(element, environment, special_engine)
        return None
    
    elif isinstance(ast,VMModule):
        module_name = ast.name
        themodule = importlib.import_module('.'+module_name, package='de.mindscan.cheaplithium.vm')

        if special_engine:
            try:
                themodule._inject_engine(special_engine)
            except:
                pass
        
        return themodule
    
    elif isinstance(ast,VMAssignment):
        _right = eval_ll(ast.right, environment, special_engine)
        
        if isinstance(ast.left, VMPrimary):
            _leftValue = eval_ll_ref(ast.left.value, environment, special_engine)
            _leftSelector = eval_ll(ast.left.selector, environment, special_engine)
            # Do the assignment. Does this work?
            _leftValue[0][_leftSelector] = _right
            return None
             
        # this thing may not exist... and even may not work...
        _left = eval_ll(ast.left, environment, special_engine)
        return None
    
    elif isinstance(ast,VMPrimary):
        value = eval_ll(ast.value,environment, special_engine)
        if ast.selector is None:
            return value
        # ATTN: fix the mising Dict Selection on the fly. 
        if not isinstance(ast.selector, DictSelector):
            ast.selector = DictSelector(index = ast.selector)

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


# eval as reference; for the assignment problem ...
def eval_ll_ref( ast, environment, special_engine=None):
    if isinstance(ast, Env):
        return [environment]
    elif isinstance(ast, This):
        return special_engine.getThisByRef()
    else:
        raise Exception("eval_ll_ref can't evaluate {}: (NYI) please implement this type!".format(type(ast)))        

    