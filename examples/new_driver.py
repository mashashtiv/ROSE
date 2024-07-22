from rose.common import obstacles, actions
driver_name = "Zoe and Masha"
running = True
def drive(world):
        cur_pos_x = world.car.x
        cur_pos_y = world.car.y
        obs = world.get((cur_pos_x, cur_pos_y - 1))
        match obs:
            case obstacles.NONE:
                return actions.NONE
            case obstacles.PENGUIN:
                return actions.PICKUP
            case obstacles.WATER:
                return actions.BRAKE
            case obstacles.CRACK:
                return actions.JUMP
            case obstacles.TRASH:
                return actions.NONE
            case obstacles.BIKE:
                return actions.NONE
            case obstacles.BARRIER:
                return actions.NONE


# #"""
# This driver does not do any action.
# """
# from rose.common import obstacles, actions  # NOQA
#
# driver_name = "No Driver"
#
#
# def drive(world):
#     return actions.NONE


from rose.common import obstacles, actions
driver_name = "Zoe and Masha"
running = True
min_x = 0
max_x = 5
def run(cur_pos_x, cur_pos_y, obs, world):
    if cur_pos_x == min_x:
        return actions.RIGHT
    elif cur_pos_x == max_x:
        return actions.LEFT
    if min_x < cur_pos_x < max_x:
        if obs != obstacles.PENGUIN and obs != obstacles.NONE:
            obs = world.get((cur_pos_x - 1, cur_pos_y - 1))
            if obs == obstacles.PENGUIN or obs == obstacles.NONE:
                return actions.LEFT
            obs = world.get((cur_pos_x +1, cur_pos_y - 1))
            if obs == obstacles.PENGUIN or obs == obstacles.NONE:
                return actions.RIGHT

    #elif min_x <= cur_pos_x <=max_x:
        #go_to_p(cur_pos_x, cur_pos_y, obs, world)
# #def go_to_p(cur_pos_x, cur_pos_y, obs, world):
#
#     if (min_x, cur_pos_y - 1) == obstacles.PENGUIN:
#         return actions.LEFT,actions.PICKUP
#
#     elif (max_x, cur_pos_y - 1) == obstacles.PENGUIN:
#         return actions.RIGHT, actions.PICKUP
#

def drive(world):
        cur_pos_x = world.car.x
        cur_pos_y = world.car.y
        obs = world.get((cur_pos_x, cur_pos_y - 1))
        match obs:
            case obstacles.NONE:
                return actions.NONE
            case obstacles.PENGUIN:
                return actions.PICKUP
            case obstacles.WATER:
                return actions.BRAKE
            case obstacles.CRACK:
                return actions.JUMP
            case obstacles.TRASH:
                run(cur_pos_x,cur_pos_y,obs,world)


            case obstacles.BIKE:
                run(cur_pos_x,cur_pos_y,obs,world)


            case obstacles.BARRIER:
                run(cur_pos_x,cur_pos_y,obs,world)

            case _:
                return actions.NONE











from rose.common import obstacles, actions

driver_name = "Zoe and Masha"
running = True

min_x = 0
max_x = 5
def run(cur_pos_x, cur_pos_y, obs, world):
    if cur_pos_x == min_x:
        return actions.RIGHT
    elif cur_pos_x == max_x:
        return actions.LEFT
    else:
        if min_x < cur_pos_x < max_x:
            if obs != obstacles.PENGUIN and obs != obstacles.NONE:
                next_obs = world.get((cur_pos_x - 1, cur_pos_y - 1))
                if next_obs == obstacles.PENGUIN or next_obs == obstacles.NONE:
                    return actions.LEFT
                else:
                    return actions.NONE
            else:
                next_obs = world.get((cur_pos_x +1, cur_pos_y - 1))
                if next_obs == obstacles.PENGUIN or next_obs == obstacles.NONE:
                    return actions.RIGHT
                else:
                    return actions.NONE
        else:
            return actions.NONE
    #elif min_x <= cur_pos_x <=max_x:
        #go_to_p(cur_pos_x, cur_pos_y, obs, world)
# #def go_to_p(cur_pos_x, cur_pos_y, obs, world):
#
#     if (min_x, cur_pos_y - 1) == obstacles.PENGUIN:
#         return actions.LEFT,actions.PICKUP
#
#     elif (max_x, cur_pos_y - 1) == obstacles.PENGUIN:
#         return actions.RIGHT, actions.PICKUP
#

def drive(world):
        cur_pos_x = world.car.x
        cur_pos_y = world.car.y
        obs = world.get((cur_pos_x, cur_pos_y - 1))
        match obs:
            case obstacles.NONE:
                return actions.NONE
            case obstacles.PENGUIN:
                return actions.PICKUP
            case obstacles.WATER:
                return actions.BRAKE
            case obstacles.CRACK:
                return actions.JUMP
            case obstacles.TRASH:
                return run(cur_pos_x,cur_pos_y,obs,world)


            case obstacles.BIKE:
                return run(cur_pos_x,cur_pos_y,obs,world)


            case obstacles.BARRIER:
                return run(cur_pos_x,cur_pos_y,obs,world)

            case _:
                return actions.NONE