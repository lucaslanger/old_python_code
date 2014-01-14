def insertion_sort(myArray):
    sortedarr = []
    for i in range(len(myArray)):
        inserted = False
        for j in range(len(sortedarr)):
            if sortedarr[j] > myArray[i]:
                sortedarr.insert(j,myArray[i])
                inserted = True
                break
        if inserted == False:
            sortedarr.append(myArray[i])
        #print sortedarr
    return sortedarr
    
print insertion_sort([3,4,6,7,5,5,8,9,3,3,7,8,4,7,78,5,5,78,5,4,6,7,67,45,46])
