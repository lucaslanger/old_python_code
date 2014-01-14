def are_isomorphic(n1,n2):
	if n1 == None and n2 == None:
		return True
	if n1 == None or n2 == None:
		return False

	if n1.key == n2.key:
		
		if n1.leftChild == n2.leftChild:
			return (are_isomorphic(n1.leftChild, n2.leftChild) and are_isomorphic(n1.rightChild, n2.rightChild) )
		else
			return (are_isomorphic(n1.rightChild, n2.leftChild) and are_isomorphic(n1.leftChild, n2.rightChild) )
	else:
		return False