'''
Created on 28.12.2020

MIT License

Copyright (c) 2020 Maxim Gansert

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

def always():
    '''
    This transition guard will always evaluate to True. That means that this transition 
    will be be taken every time, if this transition is the first to be successful in a 
    series of guard checks.
    
    You can always ise it as an if then else path, where the else part is always, if the
    first condition is not met. That means, the transitions must be executed in order of 
    definition, if this feature should be "standard".
    '''
    return True

def never():
    return False

def isTrue(value):
    return value==True or str(value).lower()=="true"

def isFalse(value):
    return value==False or str(value).lower()=="false"

def isYes(value):
    return value.lower()=="yes"

def isNo(value):
    return value.lower()=="no"

def isLessThan(a,b):
    return a<b

def isLessThanOrEqual(a,b):
    return a<=b

def isGreaterThan(a,b):
    return a>b

def isGreaterThanOrEqual(a,b):
    return a>=b

def isEqual(a,b):
    return a==b

def isNotEqual(a,b):
    return a!=b