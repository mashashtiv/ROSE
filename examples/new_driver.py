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


"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "No Driver"


def drive(world):
    return actions.NONE