# word1 = "Apple"
# word2 = "Apple"
list1 = [1, 2, 3]
print(list1 * 2)
data = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
print(data[1][0][0])
nums = set([1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4])
print(nums)


# list2 = [1, 2, 3]
# list1.insert(3, 5)
# print(list1)
# print('abcdrfghij'.split('cd', 0))
# print(word1 is word2)
# print(list1 is list2)
def writer():
    title = 'Sir'
    name = (lambda x: title + ' ' + x)
    return name


a = {4, 5, 6}
b = {2, 8, 6}
print(a-b)

who = writer()
print(who('Arthur'))

print("".__add__("ad"))