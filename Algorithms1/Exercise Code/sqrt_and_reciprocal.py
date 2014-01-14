def lucas_sqrt(x, guess):

	for i in range(100):
		guess = guess + x/(2*guess) - guess/2 
		
	return guess
	
def lucas_reciprocal(x, guess):
	
	for i in range(100):
		guess = 2*guess - x*(guess**2)
		
	return guess

def lucas_cubeRoot(x, guess):
	
	for i in range(100):
		guess = guess + x/(3 * guess**2) - guess/3
	
	return guess
	
a = lucas_sqrt(534.0,1.0)
print a 
print a **2

print 

b = lucas_reciprocal(3.0, 5.0)
print b
print 1.0/b

print 

c = lucas_cubeRoot(250.0, 5.0)
print c
print c**3