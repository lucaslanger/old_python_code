'''
Created on Feb 8, 2014

@author: Lucas
'''

#Mergesort

import random

def createFile():
    
    f = open("datafile.txt", "w");
    for i in range(100000):
        f.write( str(random.randrange(1,100000000000)) + "\n" );
        
    f.close();
    

def merge_sort(li):

    if (len(li) == 1):
        return li
    
    else:
        li_length = len(li)
        return merge( merge_sort(li[:li_length/2]), merge_sort(li[li_length/2:]) )
    
    
def merge(list1, list2):
    
    result = []
    len_list1, len_list2 = len(list1), len(list2)
    list1_counter, list2_counter = 0,0
    
    run = True
    while (run):
        if (list1_counter == len_list1):
            result.extend(list2[list2_counter:])
            run = False
        
        elif(list2_counter == len_list2):
            result.extend(list1[list1_counter:])
            run = False
        
        else:
            list1_current = list1[list1_counter]
            list2_current = list2[list2_counter]
            
            if (list1_current > list2_current):
                result.append( list1_current )
                list1_counter += 1
            
            else:
                result.append( list2_current )
                list2_counter += 1
            
    return result

createFile()
myNums = [int(num) for num in open("datafile.txt", "r").readlines()];

sorted_nums = merge_sort(myNums)
print len(sorted_nums), [str(n) + " " for n in sorted_nums[:100]]
