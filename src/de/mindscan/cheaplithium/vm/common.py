'''
Created on 04.01.2021

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

def nop():
    '''
    This is one of the most interesting methods, since we need it for different reasons.
    
    But we might write back some infos or logs, so we need a way to do some callbacks...,
    as for now i leave it this way, but maybe we must change the signatures alongside.
    and hopefully we can log errors or info ans duch into the thread, maybe we need other 
    means of logging and we will just use a loging service and use the thread uuid to do 
    attribute logdata to the thread. 
    '''
    print("Invoked Node: nop()")
    return {'result':None}

def foo():
    print("Invoked Node: foo()")
    return {'result':'foo'}

def bar():
    print("Invoked Node: bar()")
    return {'result':'bar'}

def calculateNumberOfSamples(x):
    print("Invoked Node: calculateNumberOfSamples({})".format(x))
    return {'result':x * 11}