''' 
Russell Kosovsky 

    An attempt to rewrite the cherished bot, "sel" from C to Python.

        Continuing off a modified version of Jim's bot: "jimsel". *cough cough* dogwater
            - jimsel claims to be a rewrite of some unknown suspiciopus bot named "morton"
            - it seems to me like it was halfway done and then abandoned (unless morton 
            is supposed to be bad)
            - but after reading sel's C code and jimsel's python code, it seemes that 
            jimsel is actually a past attempt to rewrite of sel
            - requardless, jimsel is a good starting point to rewrite sel in python

        it seems like open_wall() is the only rewritten C function from sel

        what we have so far from jimsel (other than open_wall) seemes to be everthing 
        that could easily be rewritten in python without needing any of the other
        "missing function" from sel that we need to rewrite.

        next step: 
            - start at beginning of the first logic chunk and identify what 
            functions (from sel) need to be rewritten

'''

import math 
import libpyAI as ai

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
    
    print()
    print("--------------------------- START of frame ----------------------------")
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeedDeg(20)

    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    
    wf_1 = ai.wallFeeler(500, tracking + 15)
    wf_2 = ai.wallFeeler(500, tracking - 15)

    enemy = ai.closestShipId()

    # ai.closestRadarX(): closest ships x coord (0-256) -1 if no ships on radar
    renemy_x = ai.closestRadarX()
    # ai.closestRadarY(): closest ships y coord (0-256) -1 if no ships on radar
    renemy_y = ai.closestRadarY()

    # ???angle between enemy and self???
    radar_angle = int(math.degrees(math.atan(abs(renemy_y)/abs(renemy_x + 0.00000001))))

    heading_to_enemy = heading - ai.aimdir(0)
    heading_to_dodge = heading - ai.shotVelDir(0)

    # Other Wall Feelers
    wf_t = ai.wallFeeler(500, tracking)
    wf_p30 = ai.wallFeeler(500, tracking + 30)
    wf_n30 = ai.wallFeeler(500, tracking - 30)
    wf_p45 = ai.wallFeeler(500, tracking + 45)
    wf_n45 = ai.wallFeeler(500, tracking - 45)
    wf_p60 = ai.wallFeeler(500, tracking + 60)
    wf_n60 = ai.wallFeeler(500, tracking - 60)
    wf_p75 = ai.wallFeeler(500, tracking + 75)
    wf_n75 = ai.wallFeeler(500, tracking - 75)
    wf_p90 = ai.wallFeeler(500, tracking + 90)
    wf_n90 = ai.wallFeeler(500, tracking - 90)
    
    # ai.selfRadarX(): Returns agents X radar coordinate. If the ship is hidden from the radar returns -1.
    renemy_x = renemy_x - ai.selfRadarX() # diff between enemy x cord and self x cord

    # ai.selfRadarX(): Returns agents Y radar coordinate. If the ship is hidden from the radar returns -1.
    renemy_y = renemy_y - ai.selfRadarY() # diff between enemy y cord and self y cord

    # if x coord diff is negative and y coord diff is positive
    if renemy_x < 0 and renemy_y > 0:
        radar_angle = 180 - radar_angle

    # if x coord diff is negative and y coord diff is negative
    elif renemy_x < 0 and renemy_y < 0:
        radar_angle = 180 + radar_angle

    # if x coord diff is positive and y coord diff is negative
    elif renemy_x > 0 and renemy_y < 0:
        radar_angle = 360 - radar_angle

    print("frame initialized")

####################################################################################

    print("-----------------------------------------------------------------------")
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
    print("-----------------------------------------------------------------------")

####################################################################################

    print("-----------------------------------------------------------------------")
    print("first logic chunk")
    
    if(ai.shotAlert(0) > -1 and ai.shotAlert(0) < 80):
        
        print("Dodging")
        ai.turn(heading_to_dodge)
        ai.thrust(1)
    
    elif(ai.closestShipId() > -1 and abs(heading_to_enemy < 400)):
        
        print("Shooting")
        if(heading_to_enemy > 0):
            ai.turnRight(1)
        else:
            ai.turnLeft(1)
        ai.fireShot()

    elif(ai.closestRadarX() > -1 and abs(radar_angle < 600)):
        
        print("Aiming")
        ai.turnToDeg(radar_angle)
        if (ai.selfSpeed() < 10):
            ai.thrust(1)
    
    else:
        print("outcome: nothing")

    print("-----------------------------------------------------------------------")

####################################################################################
    
    print("-----------------------------------------------------------------------")
    print("second logic chunk")
    if((wf_1 == wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        
        print("Turning 1: ",heading - (180 + tracking))
        ai.turnToDeg(heading - (180 + tracking))
        #if(ai.selfSpeed() < 10):
        ai.thrust(1)
    
    
    elif((wf_1 < wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        
        print("Turning 2: ",heading - (180 - 15 +tracking))
        ai.turnToDeg(heading - (180 - 15 + tracking))
        ai.turn(15)
        #if(ai.selfSpeed() < 10):
        ai.thrust(1)
    
    
    elif((wf_1 > wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        
        print("Turning 3: ",heading - (180 + 15 + tracking))
        ai.turnToDeg(heading - (180 + 15 + tracking))
        ai.turn(-15)
        #if(ai.selfSpeed() < 10):
        ai.thrust(1)
    
    else:
        print("outcome: nothing")

    print("-----------------------------------------------------------------------")

####################################################################################

    print("---------------------------- END of frame -----------------------------")


ai.start(AI_loop,["-name","SelPy","-join","localhost"])

