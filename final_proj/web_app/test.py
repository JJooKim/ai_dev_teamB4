old, new={},{}

old['ad']=[1,2,3,4,5]
new['bb']=[6,7,8,9]

temp=zip(old['ad'], new['bb'])

for i in temp:
    print(i)