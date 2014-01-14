class Node: 
  def __init__(self, value = None , nexT = None, prev = None): 
    self.nexT = nexT 
    self.prev = prev
    self.value = value

  def toString(self): 
    return str("value: " + str(self.value) + "next: " + str(self.nexT))
  
class DoublyLinkedList:
  def __init__(self, size, head = None, tail = None):
    self.head = head
    self.tail = tail
    self.size = size
          
  def addLast(self, newnode):
    if self.size > 0:
      newnode.prev = self.tail
      self.tail.nexT = newnode
    else:
      self.head = newnode # assume newnode has prev and next as None already
      self.tail = newnode
      self.size += 1
          
  def removeLast(self):
    if self.size == 0:
      return None
    
    elif self.head == self.tail:
      self.head = None
      self.tail = None
    else:
      self.tail = self.tail.prev
      self.tail.nexT = None
      self.size += -1
  
  def addFront(self, newnode):
    if self.head:
      tmp = self.head
      self.head.prev = newnode 
      self.head = newnode
      newnode.nexT = tmp
    else:
      self.head = newnode  
    newnode.prev = None
    self.size += 1
  
  def removeFront(self):
    if self.head == self.tail:
            self.head = None
            self.tail = None
    else:	
            self.head = self.head.nexT
            self.head.prev = None
    size -= 1

  def getNodes(self):
    currentnode = self.head
    print currentnode.nexT
    rli = []
    while(currentnode != None):
      rli.append(str(currentnode.value))
      currentnode = currentnode.nexT
    return rli

  def toString(self):
    return str(','.join(self.getNodes()))

def createStack(mylist):
  myDLL = DoublyLinkedList(0)
  for n in mylist:
    newnode = Node(n)
    myDLL.addFront(newnode)
  return myDLL

print createStack([6,3,7,8,4,8,9,4,8,3,7,9,4,6,8,9,4,7]).toString()

