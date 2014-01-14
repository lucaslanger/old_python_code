import urllib2

count = 0

def merge_sort(li):

    if len(li) < 2: return li 
    m = len(li) / 2 
    return merge(merge_sort(li[:m]), merge_sort(li[m:])) 

def merge(l, r):
    global count
    result = [] 
    i = j = 0 
    while i < len(l) and j < len(r): 
        if l[i] < r[j]: 
            result.append(l[i])
            i += 1 
        else: 
            result.append(r[j])
            count = count + (len(l) - i) # if a i in left array is greater than j in right array all values to the right of i are also greater -- so they are all inversions
            j += 1
    result.extend(l[i:]) #if we have reached the end because either l or r is empty, fill the result with the remaining values
    result.extend(r[j:]) 
    return result

html = urllib2.urlopen('http://spark-public.s3.amazonaws.com/algo1/programming_prob/IntegerArray.txt').read().splitlines()
numArray = [num for num in html]

unsorted = [10,2,3,22,33,7,4,1,2,3]
print merge_sort(numArray)
print count
