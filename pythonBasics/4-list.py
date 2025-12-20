""" List """
# Ordered, Mutable , Allow Duplicates

l = [1,2,3]

""" 
Indexing
Range of Elements => Slicing
Change Values

Adding and Removing values
"""

print(l[0:2])
print(l[0:5])

l[0]=100
l.insert(1,99)

print(l)

# Add-remove

l.append(555)
print(l)

# l.pop()
# l.remove(99)
l.pop(1)
print(l)

l.reverse()
print(l)

l.clear()
print(l)


""" List Comphrension """

b=[1,2,3]
c=[]

for x in b:
    c.append(x*2)
print(c)


d = [x*2 for x in b]
print(d)


d = [x for x in b if x<3]
print(d)

# Formatting String

n="Raja"
txt="My name is {fname}".format(fname=n)
print(txt)

txt1="My name is {0}".format(n)
print(txt1)

txt2="My name is {}".format(n)
print(txt2)

txt3=f"My name is {n}"
print(txt3)