from numpy import *
import math
import random

def PopMatSetinit(arr_a,arr_b,PopSize,m,n):
	PopSet=[]

	for repeatId in xrange(0,PopSize):
		x=mat(zeros((m,n)))
		list1=range(1,m*n+1)
		random.shuffle(list1)
		a=list(arr_a)
		b=list(arr_b)

		try:
			k=1
			while k:
				k=list1.pop()
				i=int(math.floor((k-1)/n+1,))
				j=(k-1)%n+1
				x[i-1,j-1]=min(a[i-1],b[j-1])
				a[i-1]=a[i-1]-x[i-1,j-1]
				b[j-1]=b[j-1]-x[i-1,j-1]

			pass
		except Exception as e:
			pass
		PopSet.append(x)
	return PopSet


def PopCross(x1,x2):
	D=floor((x1+x2)/2)
	R=(x1+x2)%2
	return D,R



if __name__ == '__main__':
	a=array([8,19,17])
	b=array([11,3,14,16])

	pset=PopMatSetinit(a,b,100,3,4)
	print pset[0]
	print pset[1]
	(d,r)=PopCross(pset[0],pset[1])
	print d
	print r
