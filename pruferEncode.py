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

def pruferNumEncoder(TranMat):
	SrcNum=TranMat.shape[0]
	DecNum=TranMat.shape[1]
	LeafSet,NodeSet,SrcNonZerolist,DecNonZerolist=splitNodeTo2Set(TranMat,SrcNum,DecNum)
	# print LeafSet,NodeSet
	PT_set=[]
	flag=1 # index for minLeafNum in srcSet or desSet
	while(len(SrcNonZerolist)>1):
		MinLeafNum=min(LeafSet)
		if (MinLeafNum<SrcNum+1) :# row /source node
			EdgeIdxInNonZerolist=SrcNonZerolist.index(MinLeafNum-1)
			RelatedNode=DecNonZerolist[EdgeIdxInNonZerolist]+1+SrcNum
			flag=1
		else: # col / destination node
			EdgeIdxInNonZerolist=DecNonZerolist.index(MinLeafNum-SrcNum-1)
			RelatedNode=SrcNonZerolist[EdgeIdxInNonZerolist]+1
			flag=0
		# print MinLeafNum,RelatedNode
		del SrcNonZerolist[EdgeIdxInNonZerolist],DecNonZerolist[EdgeIdxInNonZerolist]
		PT_set.append(RelatedNode)
		# print SrcNonZerolist,DecNonZerolist
		#update leafnode set
		LeafSet.remove(MinLeafNum)
		if flag:
			if(DecNonZerolist.count(RelatedNode-SrcNum-1)>1):
				pass
			elif (DecNonZerolist.count(RelatedNode-SrcNum-1)==0) : #NOT CONNTECTED GRAGH
				LeafSet.remove(RelatedNode)
			else:
				LeafSet.append(RelatedNode)
				NodeSet.remove(RelatedNode)
		else:
			if(SrcNonZerolist.count(RelatedNode-1)>1):
				pass
			elif (SrcNonZerolist.count(RelatedNode-1)==0):
				LeafSet.remove(RelatedNode)
			else:
				LeafSet.append(RelatedNode)
				NodeSet.remove(RelatedNode)
		# print LeafSet,NodeSet
	return PT_set




def splitNodeTo2Set(TranMat,SrcNum,DecNum):
	TempMat=TranMat.nonzero()
	LeafSet=[]
	NodeSet=[]
	SrcNonZerolist=TempMat[0].tolist()
	DecNonZerolist=TempMat[1].tolist()
	# print SrcNonZerolist,DecNonZerolist

	for i in range(0,SrcNum+DecNum):
		if i < SrcNum:
			if SrcNonZerolist.count(i)>1:
				NodeSet.append(i+1)
			else:
				LeafSet.append(i+1)
		else:
			if DecNonZerolist.count(i-SrcNum)>1:
				NodeSet.append(i+1)
			else:
				LeafSet.append(i+1)
	return LeafSet,NodeSet,SrcNonZerolist,DecNonZerolist


def pruferNumDecoder(PT,SrcNum,DecNum,arr_a,arr_b):
	PT_norepeat=set(PT)
	UniversalSet=set(range(1,SrcNum+DecNum+1))
	P_ba=list((UniversalSet-PT_norepeat))
	TranMat=mat(zeros((SrcNum,DecNum)))
	a=list(arr_a)
	b=list(arr_b)
	print P_ba, PT
	Edge=[]
	while(PT):
		# print 'caonima'
		i=min(P_ba)
		index=0
		j=PT[index]
		while (i-(SrcNum+0.5))*(j-(SrcNum+0.5))>0:# make sure i,j in different Set(Src or Des)
			index=index+1
			j=PT[index]
		if(index!=0):
			PT[0],PT[index]=PT[index],PT[0]
		Edge.append([i,j])
		updateTranportValue(TranMat,i,j,a,b,SrcNum)
		P_ba.remove(i)
		del PT[0]
		if PT.count(j)==0:
			P_ba.append(j)
		# print Edge
	if len(P_ba)==2:
		print "we run into this part"
		Edge.append([P_ba[0],P_ba[1]])
		updateTranportValue(TranMat,P_ba[0],P_ba[1],a,b,SrcNum)
		# print "last step a,b is"
		# print a,b

	# print "edge set is:"
	# print Edge
	# print TranMat
	while sum(a)+sum(b)>0 :
		r=a.index(max(a))+1
		s=b.index(max(b))+1+SrcNum
		Edge.append([r,s])
		updateTranportValue(TranMat,r,s,a,b,SrcNum)
	# print Edge
	# print TranMat
	return TranMat


def updateTranportValue(mat,i,j,a,b,SrcNum):
	if i>j:
		i,j=j,i
	x=min([a[i-1],b[j-SrcNum-1]])
	a[i-1]=a[i-1]-x
	b[j-SrcNum-1]=b[j-SrcNum-1]-x
	mat[i-1,j-1-SrcNum]=x
	# print "a,b=|||"
	# print a,b


def vefifyChromosome():

	pass

def Cross():
	pass

def select():
	pass

def variation():
	pass

if __name__ == '__main__':
	a=array([8,19,17])
	b=array([11,3,14,16])

	pset=PopMatSetinit(a,b,1,3,4)
	print pset[0]
	PT=pruferNumEncoder(pset[0])
	recMat=pruferNumDecoder(PT,3,4,a,b)
	print recMat
	print ((pset[0]==recMat).all())
	# pruferNumDecoder([4,2,2,7,3],3,4,a,b)
	# pruferNumDecoder([4,2,1,7,2],3,4,a,b)
#	pruferNumDecoder([3,7,2,7,3],3,4,a,b)
	
