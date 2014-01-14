def convert_dec_to_binary(b):
    ans = ''
    while b > 0:         
        modb = b % 2
        b = (b - modb)/2
        ans = str(modb) + ans # ordering?  
    return int(ans)
    
print convert_dec_to_binary(55)