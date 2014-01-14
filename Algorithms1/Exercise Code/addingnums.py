n1 = 8833646723
n2 = 42655337

a = [int(x) for x in str(n1)]

b = [int(x) for x in str(n2)]

def addnums(num1, num2): 
    num1.reverse()
    num2.reverse()
    
    retarray = []
	
    longnum = max(num1, num2, key = len)
    shortnum = num1 if longnum == num2 else num2 
    carry = 0 
	
    for i in range(0, len(longnum)):
    	sum = (longnum[i] + shortnum[i] + carry) if i < len(shortnum)  else longnum[i] + carry
    	carry = 1 if sum >= 10 else 0
    	value = sum - (10 * carry)
        retarray.append(value)

    if carry == 1:
    	retarray.append(1)
    
    retarray.reverse()
    return retarray
    
    
print addnums(a,b)
print n1 + n2