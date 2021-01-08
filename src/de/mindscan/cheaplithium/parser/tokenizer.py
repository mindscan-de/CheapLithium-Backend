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

## TODO: DecisionLanguageLexxer will output tokens for an input string lexxer is based on regexes...
## TODO: DecisionLanguageTokenzer will use the Lexxer to provide tokens

## TODO: don't make it too fancy... for now i use regexes, but they aren't 
##       sufficient enough, because i want to extract some information from 
##       the AST, like input descriptions from the node, and transitiion 
##       signatures....
## TODO: also want to provide the users with help, and code completion later on. 

class Literal(object):
    pass

# for nonfractional numbers    
class Integer(Literal):
    pass

# for Strings
class String(Literal):
    pass

# for true / false
class Boolean(Literal):
    pass

# for None / Null
class NONE(Literal):
    pass

# '=' 
class Operator(object):
    pass

# ';', '.', ',', '(', ')'
class Separator(object):
    pass

# Names of variables, methods, environments
class Identifier(object):
    pass


