import libpyAI as ai 
import random
import math 


FEELER_DIRS = []
FEELER_DIRS.append(0)
FEELER_DIRS.append(15)
FEELER_DIRS.append(-15)
FEELER_DIRS.append(30)
FEELER_DIRS.append(-30)
FEELER_DIRS.append(45)
FEELER_DIRS.append(-45)
FEELER_DIRS.append(60)
FEELER_DIRS.append(-60)
FEELER_DIRS.append(75)
FEELER_DIRS.append(-75)
FEELER_DIRS.append(90)
FEELER_DIRS.append(-90)


def open_wall(xdir, dist):
    if(xdir == -1 or dist == -1):
        return ai.selfTrackingDeg() + 180
    else:
        max = -1
        for i in range(12):
            w = ai.wallFeeler(dist, xdir+FEELER_DIRS[i])
            if w == dist:
                return i
            elif w > max:
                max = i
        return i

def AI_loop():

    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeedDeg(20)

    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())

    enemy = ai.closestShipId()

    renemy_x = ai.closestRadarX()
    renemy_y = ai.closestRadarY()

    radar_angle = int(math.degrees(math.atan(abs(renemy_y)/abs(renemy_x + 0.00000001))))

    heading_to_enemy = heading - ai.aimdir(0)
    heading_to_dodge = heading - ai.shotVelDir(0)

    # Wall Feelers
    wf_0 = ai.wallFeeler(500, tracking)

    wf_1 = ai.wallFeeler(500, tracking + 15)
    wf_2 = ai.wallFeeler(500, tracking - 15)
    
    wf_3 = ai.wallFeeler(500, tracking + 30)
    wf_4 = ai.wallFeeler(500, tracking - 30)
    wf_5 = ai.wallFeeler(500, tracking + 45)
    wf_6 = ai.wallFeeler(500, tracking - 45)
    wf_7 = ai.wallFeeler(500, tracking + 60)
    wf_8 = ai.wallFeeler(500, tracking - 60)
    wf_9 = ai.wallFeeler(500, tracking + 75)
    wf_10 = ai.wallFeeler(500, tracking - 75)
    wf_11 = ai.wallFeeler(500, tracking + 90)
    wf_12 = ai.wallFeeler(500, tracking - 90)
    
    renemy_x = renemy_x - ai.selfRadarX()
    renemy_y = renemy_y - ai.selfRadarY()

    if renemy_x < 0 and renemy_y > 0:
        radar_angle = 180 - radar_angle
    elif renemy_x < 0 and renemy_y < 0:
        radar_angle = 180 + radar_angle
    elif renemy_x > 0 and renemy_y < 0:
        radar_angle = 360 - radar_angle

    print("open_wall: ",open_wall(tracking, 100))

    print("wf_1: ", wf_1)
    print("wf_2: ", wf_2)
    print("shot alert: ", ai.shotAlert(0))
    print("enemy id: ", enemy)
    print("aimdir: ", ai.aimdir(0))
    print("heading to enemy: ", heading_to_enemy)
    print("heading to dodge: ", heading_to_dodge)
    print("renemy_x: ", renemy_x)
    print("renemy_y: ", renemy_y)
    print("radar angle: ", radar_angle)
    print("-------")


    
    # Dodge shots
    if(ai.shotAlert(0) > -1 and ai.shotAlert(0) < 80):
        print("Dodging")
        ai.turn(heading_to_dodge)
        ai.thrust(1)
    
    # Shoot nearest enemy
    elif(ai.closestShipId() > -1 and abs(heading_to_enemy < 400)):
        print("Shooting")
        if(heading_to_enemy > 0):
            ai.turnRight(1)
        else:
            ai.turnLeft(1)
        ai.fireShot()

    # Point at closest enemy on radar and chase
    elif(ai.closestRadarX() > -1 and abs(radar_angle < 600)):
        ai.turnToDeg(radar_angle)
        if (ai.selfSpeed() < 10):
            ai.thrust(1)

    

    # Wall avoidance
    if((wf_1 == wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(heading - (180 + tracking))
        #if(ai.selfSpeed() < 10):
        ai.thrust(1)
        print("Turning 1: ",heading - (180 + tracking))
    elif((wf_1 < wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(heading - (180 - 15 + tracking))
        ai.turn(15)
        #if(ai.selfSpeed() < 10):
        ai.thrust(1)
        print("Turning 2: ",heading - (180 - 15 +tracking))
    elif((wf_1 > wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turnToDeg(heading - (180 + 15 + tracking))
        ai.turn(-15)
        #if(ai.selfSpeed() < 10):
        ai.thrust(1)
        print("Turning 3: ",heading - (180 + 15 + tracking))


ai.start(AI_loop,["-name","SelPy","-join","localhost"])



        
'''
def open_wall(xdir, dist):
    if xdir == -1 or dist == -1:
        return angle_add(ai.self_track(), 180)
    else:
        max_dist = -1
        max_i = -1
        for i in range(13):
            w = wf_(dist, angle_add(xdir, feeler_dirs[i]))
            if w == dist:
                return i
            elif w > max_dist:
                max_dist = w
                max_i = i
        return max_i


def wf_(range, degree):
    x = ai.self_x() + range * math.cos(math.radians(degree))
    y = ai.self_y() + range * math.sin(math.radians(degree))
    res = ai.wall_between(ai.self_x(), ai.self_y(), x, y)
    return range if res == -1 else res

def change_tracking(dir):
    change_heading(angle_add(ai.self_track(), angle_diff(dir, ai.self_track())))

def change_heading(dir):
    ai.self_turn(angle_diff(ai.self_heading(), dir))

def screen_enemy_num(n):
    if ai.ship_x(n) == -1:
        return -1
    elif ai.team_play() == 1 and ai.self_team() != ai.ship_team(n):
        return n
    else:
        return screen_enemy_num(n + 1)

def radar_enemy_num(n):
    if ai.radar_x(n) == -1:
        return -1
    elif ai.radar_enemy(n) == 1:
        return n
    else:
        return radar_enemy_num(n + 1)

def angle_diff(angle1, angle2):
    # Implement the angle difference calculation
    pass

def angle_add(angle1, angle2):
    # Implement the angle addition calculation
    pass

def init_feeler_dirs():
    global feeler_dirs
    feeler_dirs = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75, 90, -90]

'''
