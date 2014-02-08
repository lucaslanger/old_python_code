'''
Created on Feb 8, 2014

@author: Lucas
'''

import random

def createFile():
    
    f = open("datafile.txt", "w");
    for i in range(10000):
        f.write( str(random.randrange(1,100000000000)) + "\n" );
        
    f.close();
    
    
def swap_indices( myli, index1, index2 ):
    tmp = myli[index1]
    myli[index1] = myli[index2]
    myli[index2] = tmp
    
def selection_Sort(myList):
    for i in range(len(myList) ):
        biggest = i
        
        for j in range(i+1, len(myList) ):   
            
            if myList[j] > myList[biggest]:
                biggest = j
 
        swap_indices(myList, biggest, i)
        
    return myList
        
        
createFile()
myNums = [int(num) for num in open("datafile.txt", "r").readlines()];
sorted_nums = selection_Sort(myNums)
print len(sorted_nums), [str(n) + " " for n in sorted_nums[:100]]
 
 

        
    
