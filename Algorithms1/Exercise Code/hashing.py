dict = {}

def genHashCode(s):
    val = 0
    x = 10
    
    i=0
    for a in s:
        val += ord(a) * (x**i)
        i+= 1
    return val
        
def compressHash(v ,i):
    return v % i

datatohash = [('John', 68000), ('Julia',60500), ('Frank',50600),('Clide', 50030)]

for a in datatohash:
    h = compressHash(genHashCode(a[0]),4)
    if h in dict.keys():
        dict[h].append(a[1])
    else:    
        dict[h] = [a[1]]
    
print dict
    