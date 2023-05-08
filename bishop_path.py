class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class B(A):
    def __init__(self, a, name):
        
        self.a = a
        self.name = name


chars_list = ['X', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'X']
nums_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 0]

def out(pos):
    char, num = pos[0], int(pos[1])
    if char == 'X' or num == 0:
        return True
    else:
        return False

def is_black(pos):
    x = chars_list.index(pos[0])
    y = int(pos[1])
    #print(x, y)
    return (x+y) % 2 == 0

a = A(20, 30)
b = B(a, 'bishop')
positions = [char + str(num) for char in chars_list[1:9] for num in nums_list[1:9]]

def poss_movs(pos):
    av_sqrs = []
    char_ind = chars_list.index(pos[0])
    num = int(pos[1])
    count = 1
    next_pos = chars_list[char_ind - count] + str(nums_list[num + count])
    # up left
    while out(next_pos) is False:
        next_pos = chars_list[char_ind - count] + str(nums_list[num + count])
        av_sqrs.append(next_pos)
        count += 1

    # down left
    count = 1
    next_pos = chars_list[char_ind - count] + str(nums_list[num - count])
    while out(next_pos) is False:
        next_pos = chars_list[char_ind - count] + str(nums_list[num - count])
        av_sqrs.append(next_pos)
        count += 1

    # up right
    count = 1
    next_pos = chars_list[char_ind + count] + str(nums_list[num + count])
    while out(next_pos) is False:
        next_pos = chars_list[char_ind + count] + str(nums_list[num + count])
        av_sqrs.append(next_pos)
        count += 1
    # down right
    count = 1
    next_pos = chars_list[char_ind + count] + str(nums_list[num - count])
    while out(next_pos) is False:
        next_pos = chars_list[char_ind + count] + str(nums_list[num - count])
        av_sqrs.append(next_pos)
        count += 1
    
    return av_sqrs

def paths():
    dic = {pos : poss_movs(pos) for pos in positions}
    return dic

