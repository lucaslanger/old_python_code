def karatsuba(num1, num2):
    product = 0  
    
    ma = max(num1,num2,key = len)   
    mi = num1 if ma == num2 else num2 #min(num1,num2,key = len) returns same val as max if len same
    multiples = (len(ma) - (len(ma) % len(mi)) )/len(mi) 
    #base case
    if len(num1) == 1 and len(num2) == 1: 
        return num1[0] * num2[0]
    #if length of first number is a multiple of second number
    elif multiples > 1:
        multiples += 1# extra is for remainder. Needs an extra recursive call for the remainder!       
        for i in range(multiples):
            if len(ma) > 0:
                last = []
                for c in range(len(mi)):                
                    last.append(ma.pop())     
                product += karatsuba(last,mi) * 10**(len(mi)*i)
        return product
    #recursing with karasuba's genius algorithm
    else:
        if len(ma) % 2 != 0:
            ma.insert(0,0)        
        
        for i in range(len(ma) - len(mi) ):
            mi.insert(0,0)    
 
        a = ma[:len(ma)/2]
        b = ma[len(ma)/2:]
        c = mi[:len(mi)/2]
        d = mi[len(mi)/2:]
        
        sum1 = int(''.join([str(u) for u in a])) + int(''.join([str(u) for u in b]))
        sum2 = int(''.join([str(u) for u in c])) + int(''.join([str(u) for u in d]))
        
        f = karatsuba(a,c)
        s = karatsuba(b,d)        
        t = karatsuba([int(h) for h in str(sum1)], [int(h) for h in str(sum2)] )
        
        return f*10**(len(ma)) + (t - f - s)*10**(len(ma)/2) + s

print karatsuba([3,0,5,3,6,8],[1,1,1,4,4,7])
print 305368*111447