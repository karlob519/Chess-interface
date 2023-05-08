from itertools import groupby

chars_list = ['X', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'Y']
nums_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

knight_chars = ['X', 'X', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'X', 'X']
knight_nums = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 0]

def out(pos):
    char, num = pos[0], int(pos[1])
    if char == 'X' or num == 0 or char == 'Y' or num == 9:
        return True
    else:
        return False

positions = [char + str(num) for char in chars_list[1:9] for num in nums_list[1:9]]

def rook_paths(pos):
    av_sqrs = []
    char_ind = chars_list.index(pos[0])
    num = int(pos[1])
    # left
    count = 1
    next_pos = chars_list[char_ind - count] + str(nums_list[num])
    
    while out(next_pos) is False:
        next_pos = chars_list[char_ind - count] + str(nums_list[num])
        av_sqrs.append(next_pos)
        count += 1

    # right
    count = 1
    next_pos = chars_list[char_ind + count] + str(nums_list[num])
    while out(next_pos) is False:
        next_pos = chars_list[char_ind + count] + str(nums_list[num])
        av_sqrs.append(next_pos)
        count += 1

    # up 
    count = 1
    next_pos = chars_list[char_ind] + str(nums_list[num + count])
    while out(next_pos) is False:
        next_pos = chars_list[char_ind] + str(nums_list[num + count])
        av_sqrs.append(next_pos)
        count += 1
    # down
    count = 1
    next_pos = chars_list[char_ind] + str(nums_list[num - count])
    while out(next_pos) is False:
        next_pos = chars_list[char_ind] + str(nums_list[num - count])
        av_sqrs.append(next_pos)
        count += 1
    
    return av_sqrs

def bishop_paths(pos):
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

def king_paths(pos):
    av_sqrs = []
    char_ind = chars_list.index(pos[0])
    num = int(pos[1])
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                None
            else:
                next_pos = chars_list[char_ind + i] + str(nums_list[num + j])
                if out(next_pos) is False:
                    av_sqrs.append(next_pos)
    return av_sqrs

def knight_paths(pos):
    av_sqrs = []
    char_ind = knight_chars.index(pos[0])
    num = knight_nums.index(int(pos[1]))
    for i in [-2, -1, 1, 2]:
        for j in [-2, -1, 1, 2]:
            if abs(i) + abs(j) != 3:
                None
            else:
                next_pos = knight_chars[char_ind + i] + str(knight_nums[num + j])
                if out(next_pos) is False:
                    av_sqrs.append(next_pos)
    return av_sqrs


def rook():
    dic = {pos : rook_paths(pos) for pos in positions}
    return dic

def bishop():
    dic = {pos : bishop_paths(pos) for pos in positions}
    return dic

def queen():
    dic = {pos : rook_paths(pos) + bishop_paths(pos) for pos in positions}
    return dic

def king():
    dic = {pos : king_paths(pos) for pos in positions}
    return dic

def knight():
    dic = {pos : knight_paths(pos) for pos in positions}
    return dic


