# a = "chow "
# b = str(2)
# c = a + b
# print(f"c: {c}")
# d = c.split()
# # print(f"d: {d}")
# print(f"d[0]: {d[0]}")
# n = int(d[1])
# if d[0] == "chow":
#     print("do chow")
#     if n == 2:
#         print("is a number")

# my_dict = {'a': 10, 'b': 5, 'c': 20, 'd': 15}

# # Find the key with the largest value
# max_key = max(my_dict, key=lambda k: my_dict[k])

# print(f"The key with the largest value is '{max_key}' with a value of {my_dict[max_key]}.")

# a = [0] * 8
# print(a)
# a[3] = int(True)
# if a[3]:
#     print(a)

# a = []
# for i in a:
#     print(i)
# a = "條2"
# print(a)

# num = 11
# a = "ting " + str(num)
# print(a)

# a = [0,1,2,4,5,6,7,8,9]
# for i in a:
#     b = a.copy()
#     b.remove(i)
#     print(b)
# a.append(3)
# a.sort()
# print(a)

# a = ""
# print(a)
# print("nothing")

# for i in range(10):
#     if i == 6:
#         continue
#     print(i)

# a = [0,1,2,3]
# print(len(a))
# for i in range(len(a)):
#     b = a.copy()
#     b.pop(i)
#     print(b)
# if 4 not in a:
#     print("not")
# else:
#     print("yes")

# a = [1,1,1,1,1]
# a.remove(1)
# print(a)

# chow_sets = [[1,2,3], [4,5,6], []]

# print(f"玩家1是否要吃牌: (1)否 ", end="")
# for i in range(len(chow_sets)): 
#     print("({0})".format(i+2), end="")
#     if chow_sets[i] != []:
#         for j in range(3):
#             print(chow_sets[i][j], end=" ")

# print(f"玩家1是否要吃牌: (1)否 ", end="")
# for i in range(len(chow_sets)): 
#     print(f"({i+2})", end="")
#     if chow_sets[i] != []:
#         for j in range(3):
#             print(chow_sets[i][j], end=" ")
# print(":", end="")

a = [1, 2, 3, 4, 5, 6]
b = a
b.remove(1)
print(a)