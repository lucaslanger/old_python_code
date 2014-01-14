import urllib2
import sys

comparisons = 0

def countComparisons(nums):
    
    global comparisons
    j = 1 # value to swap with
    if ( (len(nums) == 1) or (len(nums) == 0) ):
        return nums 
    else:
        comparisons += len(nums) - 1

        for i in range(1,len(nums)):
            if nums[i] < nums[0]:           
                nums[i], nums[j] = nums[j], nums[i]
                j += 1
        rArray = [c for c in countComparisons(nums[1:j])]
        rArray.append(nums[0])
        rArray.extend(countComparisons(nums[j:]))
    return rArray

a = urllib2.urlopen("http://spark-public.s3.amazonaws.com/algo1/programming_prob/QuickSort.txt").readlines()
b = open("100.txt","r").readlines()
#array = [int(b) for b in a]
#array = [3,9,8,4,6,10,2,5,7,1]
array = [int(x) for x in b]
sys.setrecursionlimit(11000)                             
ans = countComparisons(array)
print comparisons









