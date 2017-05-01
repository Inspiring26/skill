 # -*- coding: utf-8 -*- 
num=1
for x in xrange(2,11):
	num=2*(num+1)
	
print '天','	','吃前的数量'
for x in xrange(1,11):
	print x,'	',num
	num=(num/2)-1

	