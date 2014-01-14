def convertbase10(initialbase, numberarr):
    
    ans = 0
    numberarr.reverse()
    for i in range(len(numberarr)):
        ans += int(numberarr[i]) * initialbase**(i)
    return ans
       
print convertbase10(3,[a for a in str(222)])