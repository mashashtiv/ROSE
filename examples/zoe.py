from none import *


def find_lane(cur_pos_x, cur_pos_y):
    min_x, max_x = 0, 2
    return min_x, max_x


def count(points, op):
    sum_points = 0
    for i in points[op]:
        sum_points += i

    return sum_points


def marge(op_1, op_2, op_3, points):

    if op_1 == 'no' and op_2 == 'no' and op_3 == 'no':
        return ['no']

    if op_1 == 'no' and op_2 == 'no' and op_3 != 'no':
        return [op_3]

    if op_1 == 'no' and op_2 != 'no' and op_3 == 'no':
        return [op_2]

    if op_1 != 'no' and op_2 == 'no' and op_3 == 'no':
        return [op_1]

    if count(points, op_1) >= count(points, op_2):
        if count(points, op_1) >= count(points, op_3):
            return [op_1]
        else:
            return [op_3]
    elif count(points, op_2) >= count(points, op_3):
        return [op_2]
    else:
        return [op_3]







def priorities(lane, step, points, bord, cur_pos_x , cur_pos_y):
    min_x, max_x = find_lane(cur_pos_x, cur_pos_y)
    if lane > max_x or lane < min_x:
        return ['no']
    if step <= 0:
        return ["finish"]

    points[lane].append(bord[cur_pos_x][cur_pos_y])

    R = [lane + 1] + priorities(lane+1, step-1, points, bord, cur_pos_x +1, cur_pos_y +1)
    M = [lane] + priorities(lane, step - 1, points, bord, cur_pos_x, cur_pos_y +1)
    L = [lane - 1] + priorities(lane -1, step - 1, points, bord, cur_pos_x -1, cur_pos_y +1)

    return marge(R, M, L, points)



points = [[],[],[]]
bord = [[[-10], [+5], [+10]], [[+10], [0], [-10]]]
lane = 1
step = 1
cur_pos_x = 1
cur_pos_y = 0

print(priorities(lane, step, points, bord, cur_pos_x, cur_pos_y))

