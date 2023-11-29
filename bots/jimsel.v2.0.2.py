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


def init_feeler_dirs():
    global FEELER_DIRS
    FEELER_DIRS = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75, 90, -90]


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


def change_heading(dir, heading):
	ai.turn(ai.ai.angleDiff(heading, dir))

def change_tracking(dir, tracking, heading):
	change_heading(ai.ai.angleAdd(tracking, ai.ai.angleDiff(dir, tracking)), heading);


def AI_loop():
    
    print()
    print("--------------------------- START of frame ----------------------------")
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    
    ## matches sel
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeedDeg(20)

    ## matches sel
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    
    ## matches sel
    wf_1 = ai.wallFeeler(500, tracking + 15)
    wf_2 = ai.wallFeeler(500, tracking - 15)

    enemy = ai.closestShipId()

    # ai.closestRadarX(): closest ships x coord (0-256) -1 if no ships on radar
    enemy_x = ai.closestRadarX()
    # ai.closestRadarY(): closest ships y coord (0-256) -1 if no ships on radar
    enemy_y = ai.closestRadarY()

    # angle between enemy and self???
    radar_angle = int(math.degrees(math.atan(abs(enemy_y)/abs(enemy_x + 0.00000001))))

    heading_to_enemy = heading - ai.aimdir(0)
    heading_to_dodge = heading - ai.shotVelDir(0)

    renemy_x = enemy_x - ai.selfRadarX() # diff between enemy x cord and self x cord
    renemy_y = enemy_y - ai.selfRadarY() # diff between enemy y cord and self y cord

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



    print("-----------------------------------------------------------------------")
    print("first logic chunk")
    
    if(ai.shotAlert(0) != -1 and ai.shotAlert(0) < 80):
        
        print("Dodging")
        ai.turn(heading_to_dodge)
        #ai.turn(ai.angleDiff(heading, ai.angleAdd(ai.shotVelDir(0), 180)))
        ai.thrust(1)
    

    elif ai.wallBetween(ai.selfX(), ai.selfY(), enemy_x, enemy_y) != -1:

        change_heading(open_wall(ai.enemyTrackingDeg(0), ai.enemyDistance(0)), heading)
        if(ai.selfSpeed() < 6):
            ai.thrust(1)


    elif ((ai.enemyTrackingDeg(0) > -1) and (abs(ai.ai.angleDiff(heading, ai.enemyHeadingDeg(0))) < 5)):

        change_heading(ai.enemyHeadingDeg(0), heading)
        ai.fireShot(1)
    
    
    elif ((ai.enemyTrackingDeg(0) > -1) and (abs(ai.ai.angleDiff(heading, ai.enemyHeadingDeg(0))) > 5)):

        change_heading(ai.enemyHeadingDeg(0), heading)
    
    
    elif (abs(ai.ai.angleDiff(ai.enemyHeadingDeg(0), heading)) < 5):

        change_tracking(ai.enemyHeadingDeg(0), tracking, heading)
        ai.fireShot(1)
        
        if not (((abs(ai.ai.angleDiff(tracking, ai.enemyHeadingDeg(0))) < 15) and (ai.selfSpeed() < 7))):
            ai.thrust(1)
    
    
    elif not ((ai.closestRadarX() <= 0)):

        ai.turn(ai.ai.angleDiff(heading, ai.enemyHeadingDeg(0)))

    
    print("-----------------------------------------------------------------------")
    print("second logic chunk")


    if ((wf_1 == wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turn(ai.angleDiff(heading, ai.angleAdd(tracking, 180)))
	

    elif ((wf_1 < wf_2) and (wf_1 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        ai.turn(ai.angleDiff(heading, ai.angleAdd(180, ai.angleAdd(-15, tracking))))
        if (ai.angleDiff(heading, ai.angleAdd(180, ai.angleadd(-15, tracking))) < 30):
            ai.thrust(1)
		

    elif ((wf_1 > wf_2) and (wf_2 < (20 * ai.selfSpeed())) and (ai.selfSpeed() > 1)):
        
        ai.turn(ai.angleDiff(heading, ai.angleAdd(180, ai.angleadd(15, tracking))))

        if (ai.angleDiff(heading, ai.angleAdd(180, ai.angleadd(15, tracking))) < 30):
            ai.thrust(1)


    print("-----------------------------------------------------------------------")
    print("---------------------------- END of frame -----------------------------")


ai.start(AI_loop,["-name","SelPy","-join","localhost"])