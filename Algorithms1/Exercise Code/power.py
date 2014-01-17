numberofmultiplications = 0
def power(num, exp):
    global numberofmultiplications
    if exp == 1:
        return num
    else:
        if exp % 2 == 1:
            numberofmultiplications += 2
            return power(num, exp/2)**2 * num
            
        else:
            numberofmultiplications += 1
            return power(num, exp/2)**2
        
def sumofcpower(x,i):
    if i == 0:
        return 1
    else:
        return power(x,i) + sumofcpower(x, i-1)
    
print sumofcpower(3,5)        
