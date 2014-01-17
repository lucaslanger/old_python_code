
from linkedlist import *

class NaturalNumber:
    def __init__(self, base, coefficients):
        self.coefficientlist = DoublyLinkedList()
        for c in coefficients:
            nodec = Node(c)
            self.coefficientlist.addFront(nodec)  # this reverses the order. lowest exponent at front
        self.base = base
      
    def sum(self, secondnum):
        result = [ ]
        h1 = self.coefficientlist.head
        h2 = secondnum.coefficientlist.head
        carry = 0
        while True:
            rem = (h1.value + h2.value + carry) % self.base
            carry = (h1.value + h2.value + carry - rem) / self.base
            result.append(rem)
        
            h1prev = True if h1.prev else False
            h2prev = True if h2.prev else False
        
            if h1prev == False and h2prev == False:
                print 'Both h1 and h2 are empty!'
                if carry != 0:
                    result.append(carry)
                break
          
            elif h1prev == False:
                print "h1 is empty!"
                if h2.prev:
                    while h2.prev:
                        mod = (h2.prev.value + carry) % self.base
                        carry = (h2.prev.value + carry - mod) / self.base
                        result.append(mod)
                        h2 = h2.prev
                        
                if carry != 0:
                    result.append(carry)
                break
          
            elif h2prev == False:
                print "h2 is empty!"
                if h1.prev:
                    while h1.prev:
                        mod = (h1.prev.value + carry) % self.base
                        carry = (h1.prev.value + carry - mod) / self.base
                        result.append(mod)
                        h1 = h1.prev

                if carry != 0:
                    result.append(carry)
                break
            
            h1 = h1.prev
            h2 = h2.prev
            
        return NaturalNumber(self.base, clipBackZeroes(result))
      
    
    def subtract(self, secondnum):
        result = []
        h1 = self.coefficientlist.head
        h2 = secondnum.coefficientlist.head
        borrow = 0
        r = 0
        while True:
            if h1.value - h2.value - borrow >= 0:
                r = h1.value - h2.value - borrow
                borrow = 0 # since we didn't need to borrow this time we set borrow to 0
            else:
                if h1.prev:
                    r = self.base + h1.value - h2.value - borrow# borrow 10 from h1.prev
                    borrow = 1
                else: #if we need to borrow but h1 doesn't have a previous value then we get a negative number
                    print "Well, the number is going to be negative... do we need to address this?"
                    break
                    
            result.append(r)
            
            if h1.prev == None or h2.prev == None: #if we didnt need to borrow we need to check if h1 is empty
                if h1.prev == None and h2.prev == None:
                    break #can't have borrowed and not had h1.prev to get here MUST DEAL WITH CASE WHERE LAST VALUE BECOMES 0
                    
                elif h2.prev == None: # dump the rest of h1 onto
                    while h1.prev:
                        if (h1.prev.value - borrow != 0 or h1.prev.prev != None):
                            if h1.prev.value - borrow < 0:
                                #print "Debug: need to borrow because of borrow: " + str(h1.prev.value - borrow)
                                result.append(self.base + h1.prev.value - borrow)
                                h1 = h1.prev
                                borrow = 1
                            else:
                                #print "Debug: Appending Value of h1: " + str(h1.prev.value - borrow)
                                result.append(h1.prev.value - borrow)
                                h1 = h1.prev
                                borrow = 0
                        else:
                            break
                            
                else:
                    print "Well, the number is going to be negative... do we need to address this?"
                    break
                
                break# breaks from main loop
            h1 = h1.prev
            h2 = h2.prev
        return NaturalNumber(self.base, clipBackZeroes(result)[::-1]) #added reverse property for division
                    
                
            
    def multiply(self, num2):
        h1 = self.coefficientlist.head
        numstoadd = []
        numberofzeroes = 0
        while True:
            carry = 0
            h2 = num2.coefficientlist.head
            num = []
            while True:
                r = (h1.value * h2.value + carry) % self.base
                carry = (h1.value * h2.value + carry - r )/ self.base
                num.append(r)
                
                if h2.prev == None:
                    if carry != 0:
                        num.append(carry) 
                    break
                else:
                    h2 = h2.prev
                 
            for i in range(numberofzeroes):
                num.insert(0,0)

            numstoadd.append(num[::-1]) # need to put numbers in proper order for addition calls
            numberofzeroes += 1
            if h1.prev == None:
                break
            else:
                h1 = h1.prev
        
        t = numstoadd[0]
        counter = 1
        while True:
            try:
                fnum = NaturalNumber(self.base, t)
                snum = NaturalNumber(self.base, numstoadd[counter] )
                t = [int(i) for i in fnum.sum(snum).coefficientlist.toString().split(',')]
                counter += 1
            except:
                break
            
        return NaturalNumber(self.base, t[::-1])
        
        
    def divide(self, secondnum):
        debugc = 0
        
        result = []
        
        sec = secondnum.coefficientlist.head
        denom = [sec.value]
        while sec.prev:
            denom.insert(0, sec.prev.value)
            sec = sec.prev
        denom_num = NaturalNumber(self.base, denom)
        
        front = [self.coefficientlist.tail.value]
        natfront = NaturalNumber(self.base, [a for a in front])
        self.coefficientlist.removeLast()

        
        while True:
            
            if greaterThanOrEqual(natfront, denom_num) == False:
                if self.coefficientlist.tail:
                    front.append(self.coefficientlist.tail.value)
                    self.coefficientlist.removeLast()# removeLast?
                    natfront = NaturalNumber(self.base, [a for a in front])
                else:
                    return NaturalNumber(self.base, clipBackZeroes(result[::-1])) #so that when you grab it with toString it gets reversed again.. resulting in proper answer format
                
                result.append(0)
                         
            else:
                while True:                   
                    if greaterThanOrEqual(natfront, denom_num):
                        print "Time to increment last value of result!", debugc
                        debugc +=1
                        result[-1] += 1 #increment last value of result
                        natfront = natfront.subtract(denom_num)
                        #print [a for a in natfront.coefficientlist.toString().split(',')][::-1]
                        front = [int(a) for a in natfront.coefficientlist.getNodesHtoT()[::-1]]
                        #print front
                    else:
                        break
                
def greaterThanOrEqual(natnum1, natnum2):
    size1, size2 = natnum1.coefficientlist.size, natnum2.coefficientlist.size
    if size1 > size2:
        return True
    elif size1 == size2:
        tail1 = natnum1.coefficientlist.tail
        tail2 =  natnum2.coefficientlist.tail
        while True:
            if tail1.value > tail2.value:
                return True
            elif tail2.value > tail1.value:
                return False
            else:
                if tail1.nexT: #if there are still more digits to come
                    tail1 = tail1.nexT
                    tail2 = tail2.nexT
                else: # if there are not more digits to come and they have been equal up to now, then they are the same number
                    return True

    else:
        return False
                    
  
def clipBackZeroes(li):
    try:
        if li[-1] != 0:
            return li
        else:
            return clipBackZeroes(li[:-1])
    except:
        return [0]
#print clipBackZeroes([1,1,0,0,0,0])

def testsum():
    num1 = [4,6,7,3,6,7]
    num2 = [7,3,7,9,4,8,6,8]
    n1 = NaturalNumber(10, num1)
    n2 = NaturalNumber(10, num2)
    print n1.sum(n2).coefficientlist.toString()
    print int(''.join(str(a) for a in num1)) + int(''.join(str(a) for a in num2)) # only for base 10

def testsub():
    num1 = [1,0,0,0,0,0,0,0]
    num2 = [0,0,0,0,0,1]
    n1 = NaturalNumber(10,num1)
    n2 = NaturalNumber(10,num2)
    print n1.subtract(n2).coefficientlist.toString().split(',')[::-1]
    print int(''.join(str(a) for a in num1)) - int(''.join(str(a) for a in num2)) # only for base 10
    
def testprod():
    num1 = [1,1,1]
    num2 = [1,0,1,0]
    n1 = NaturalNumber(2, num1)
    n2 = NaturalNumber(2, num2)
    print n1.multiply(n2).coefficientlist.toString()  
    print int(''.join(str(a) for a in num1)) * int(''.join(str(a) for a in num2))  

def testdivide():
    num1 = [3,2,1,0,0]
    num2 = [1,0,2]
    n1 = NaturalNumber(4, num1)
    n2 = NaturalNumber(4, num2)
    print n1.divide(n2).coefficientlist.toString()
    #print greaterThanOrEqual(NaturalNumber(10,[6,0,0]), NaturalNumber(10, [2,1,1]))
testdivide()
    