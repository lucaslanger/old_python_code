import re
from Workinglinkedlist import *

class StringStack:
    def __init__(self):
        self.dll = DoublyLinkedList()
    
    def isEmpty(self):
        return (self.dll.size == 0)
    
    def push(self, s):
        self.dll.addFront(Node(s))
        
    def pop(self):
        tmp = self.dll.head
        if tmp:
            self.dll.removeFront()
            return tmp
        else:
            return None
        
    def get_stack(self):
        rli = []
        tmp = self.dll.head
        while tmp:
            rli.insert(0,tmp.value)
            tmp = tmp.prev
        return rli
        
    def peek(self):
        tmp = self.dll.head
        try:
            return tmp.value
        except: 
            return None

class StringSplitter:
    def __init__(self, s):
        self.cur = 0
        self.tokens = s.split(' ')#('\\s')
        
    def count_tokens(self):
        return len(self.tokens) - self.cur
    
    def has_more_tokens(self):
        return (len(self.tokens) > self.cur)
    
    def get_next_token(self):
        tmp = (self.tokens[self.cur] if self.has_more_tokens() else None)
        self.cur += 1
        return tmp

class language_parser():
    
    
    def __init__(self):
        self.s_stack = StringStack()
        
    def is_boolean(self, blah):
        if blah == 'true' or blah == 'false':
            return True
        else:
            return False
    
    def is_assignment(self, blah):
        if re.search('[a-zA-Z]+=[0-9]+', blah):
            return True
        else:
            return False
        
    def is_then(self, blah):
        return (blah == 'then')
    
    def is_if(self, blah):
        return (blah == 'if')
    
    def is_else(self,blah):
        return (blah == 'else')
    
    def is_end(self,blah):
        return (blah == 'end')
    
    def test_token(self,blah):
        return [('boolean',self.is_boolean(blah)),('assignment',self.is_assignment(blah)),('then',self.is_then(blah)),('end',self.is_end(blah)),('if',self.is_if(blah)),('else',self.is_else(blah))]
    
    def parse(self, i):
        
        s_splitter = StringSplitter(i)
        
        while s_splitter.has_more_tokens():
            nt = s_splitter.get_next_token()
            
            if nt != None:
                test = self.test_token(nt)
                if not(True in [a[1] for a in test]):
                    return False
                else:
                    index = [a[1] for a in test].index(True)
                    peekedval = self.s_stack.peek()
                    tokenval = test[index][0]
                    print self.s_stack.get_stack(), tokenval

                    if peekedval == 'if' and tokenval == 'boolean': # clears if, adds bool
                        self.s_stack.pop()
                        self.s_stack.push('boolean')
                        
                    elif peekedval == 'boolean' and tokenval == 'then': # clears bool, adds then
                        self.s_stack.pop()
                        self.s_stack.push('then')
                        
                    elif peekedval == 'then' and tokenval == 'assignment':
                        self.s_stack.pop()
                        self.s_stack.push('if_completed')
                        
                    elif peekedval == 'then' and tokenval == 'if':
                        self.s_stack.push('if')
                        
                    elif peekedval == 'if_completed' and tokenval == 'else':
                        self.s_stack.pop()
                        self.s_stack.push('else')
                        
                    elif peekedval == 'else' and tokenval == 'assignment':
                        self.s_stack.pop()
                        self.s_stack.push('else_completed')
                        
                    elif peekedval == 'else' and tokenval == 'if':
                        self.s_stack.push('if')
                        
                    elif peekedval == 'else_completed' and tokenval == 'end':
                        self.s_stack.pop()
                        if self.s_stack.peek() == 'then':
                            self.s_stack.pop()
                            self.s_stack.push('if_completed') 
                        elif self.s_stack.peek() == 'else':
                            self.s_stack.pop()
                            self.s_stack.push('else_completed')
                        
                    elif peekedval == None and tokenval == 'assignment':
                        pass
                    elif peekedval == None and tokenval == 'if':
                        self.s_stack.push('if')
                    else:
                        return False
                        
        if self.s_stack.isEmpty():
            return True
        
        else:
            print 'Here'
            while self.s_stack.isEmpty() == False:
                self.s_stack.pop()
        
            return False
    
testinputs = ['a=2 a=2','foo = 123', 'if true then a=2 else b=3 end', 'a=2 a=2 if true then a=2 else a=2 end a=2 if true then a=2 else a=2 end if true then a=2 else a=2 end a=2 if true then a=2 else a=2 end',
              'if true then a=2 else a=3 end then a=2 else a=3 end', 'a=2 a=2 if true then a=2 else a=2 end', 'if true then if false then a=2 else a=2 end else if false then a=2 else if false then b=2 else b=3 end end end']

answers = []    

def main():
    lp = language_parser()
    for i in testinputs:
        answers.append(lp.parse(i))
    return answers

print main()
    
