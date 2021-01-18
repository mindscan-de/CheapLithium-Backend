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

class Node(object):
    nodeAttrs = []
    
    def __init__(self,**kwargs):
        
        namedArguments = kwargs.copy()
        
        # TODO: collect nodeAttrs from base classes and add them here too 
        for nodeAttributeName in self.nodeAttrs:
            # pop the named values from the argument list
            value = namedArguments.pop(nodeAttributeName, None)
            # make it an attribute of this class instance
            setattr(self, nodeAttributeName, value)
        
        # check if some parameters were extra    
        if namedArguments:
            print ("found extra argumens: {} for class {} ".format(namedArguments, type(self).__name__))
            
        pass
    
    def __repr__(self):
        node_attributes_values = []
        
        # TODO: collect nodeAttrs from base classes and add them here too
        for nodeAttributeName in self.nodeAttrs:
            node_attributes_values.append("{}:{}".format(nodeAttributeName, getattr(self, nodeAttributeName)))
        
        return '{}({})'.format( type(self).__name__ , ', '.join(node_attributes_values))
    
    pass

class Declaration(Node):
    pass


class MethodDeclaration(Declaration):
    nodeAttrs=['name','parameters']
    # parameters
    # body


class LithiumCompileUnit(Declaration):
    nodeAttrs = ['guard', 'body']
    

class Apply(Node):
    nodeAttrs=['name', 'arguments']
    
class Apply2(Node):
    nodeAttrs=['name', 'arguments']
    
    
class Primary(Node):
    nodeAttrs=['selector']

class Env(Primary):
    nodeAttrs=['selector']    
    
class Literal(Primary):
    nodeAttrs=['value', 'selector']
    
class DictSelector(Node):
    nodeAttrs=['index']

class Expression(Node):
    pass

class Assignment(Expression):
    # leftexpression
    # value
    pass



class VMModule(Node):
        nodeAttrs=['name']
