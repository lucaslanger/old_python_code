def findHighest(a, low, high): # we assume here that the array consists of increasing elements up until a certain point... and then decreasing
    if low == high:
        return low
    else:
        if high-low == 1:
            if a[high] > a[low]:
                return high
            else:
                return low
            
        else:
            mid = (high - low - (high-low)%2)/2
            if a[mid+1] > a[mid]:
                return findHighest(a, mid+1, high)
            else:
                return findHighest(a, low, mid)

a = [1,5,7,9,5,3,2,1]

print a[findHighest(a, 0, len(a) - 1)]            