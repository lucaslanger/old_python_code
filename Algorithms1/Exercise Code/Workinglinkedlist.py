class Node: 
    def __init__(self, value = None): 
        self.nexT = None 
        self.prev = None
        self.value = value

    def toString(self):
        val = str(self.value) if self.value else "None"
        ne = str(self.nexT) if self.nexT else "None"
        pre = str(self.prev) if self.prev else "None"
        return "value: %s next: %s prev: %s" %(val, ne ,pre)
  
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
          
    def addLast(self, newnode):
        if self.size > 0:
            self.tail.prev = newnode
            tmp = self.tail
            self.tail = newnode
            self.tail.nexT = tmp
        else:
            self.head = newnode 
        self.tail = newnode
        self.size += 1
          
    def removeLast(self):
        if self.tail == None:
            pass
        elif self.head == self.tail:
            self.head = None
            self.tail = None
            self.size += -1
        else:
            self.tail = self.tail.nexT
            self.tail.prev = None
            self.size += -1
  
    def addFront(self, newnode):
        if self.head:
            self.head.nexT = newnode
            tmp = self.head
            self.head = newnode 
            self.head.prev = tmp
        else:
            self.head = newnode
            self.tail = newnode
        self.size += 1
  
    def removeFront(self):
        if self.head == None:
            self.head = None
            self.tail = None
        elif self.head == self.tail:
            self.head = None
            self.tail = None
            self.size = 0
        else:	
            self.head = self.head.prev
            self.head.nexT = None
            self.size -= 1

    def getNodesHtoT(self):
        currentnode = self.head
        rli = []
        while(currentnode != None):
            rli.append(str(currentnode.value))
            currentnode = currentnode.prev
        return rli

    def toString(self):
        return str(','.join(self.getNodesHtoT()))

def testcreateList(mylist):
    myDLL = DoublyLinkedList()
    for n in mylist:
        newnode = Node(n)
        myDLL.addLast(newnode)
    return myDLL

def test():
    test = testcreateList([6,3,7,8,4,8,9,4,8,3,7,9,4,6,8,9,4,7])
    print test.toString()
    test.addLast(Node(11))
    print test.toString()

