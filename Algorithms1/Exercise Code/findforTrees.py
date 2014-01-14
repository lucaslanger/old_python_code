def find(node, root):
	while root.value != node.value:
		if root == None:
			return None
		else:
			if root.value > node.value:
				root = root.leftChild
			else:
				root = root.rightChild
		
	return node
	
def findMin(root):
	while root.leftChild:
		root = root.leftChild
	return root
	
def findMax(root):
	while root.rightChild:
		root = root.rightChild
	return root