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


FEELER_DIRS = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75, 90, -90]

    #wf_1 = ai.wallFeeler(500, tracking + 15)
    #wf_2 = ai.wallFeeler(500, tracking - 15)

#frontWall = ai.wallFeeler(1000,heading)
#frontWallL = ai.wallFeeler(1000,heading+10)
#frontWallR = ai.wallFeeler(1000,heading-10)

#leftWall = ai.wallFeeler(1000,heading+90)
#leftWallL = ai.wallFeeler(1000,heading+100)
#leftWallR = ai.wallFeeler(1000,heading+80)

#rightWall = ai.wallFeeler(1000,heading+270)
#rightWallL = ai.wallFeeler(1000,heading+280)
#rightWallR = ai.wallFeeler(1000,heading+260)

#backWall = ai.wallFeeler (1000,heading+180)
#backWallL = ai.wallFeeler(1000,heading+190)
#backWallR = ai.wallFeeler(1000,heading+170)

def turn_to_degree(heading, degree: float) -> None:
        '''turn_to_degree Turns the bot to the desired heading

        Args:
            degree (float): Heading to turn to
        '''
        delta = angleDiff(heading, degree)
        if abs(delta) > 20:
            if delta < 0:
                ai.turnRight(1)
            else:
                ai.turnLeft(1)
        #else:
        #    turn_to_degree(heading, int(degree))


def angleDiff(a1: float, a2: float) -> float:
    '''angle_diff Finds the difference between two angles

    Args:
        a1 (float): angle 1
        a2 (float): angle 2

    Returns:
        float: result of the difference between the two angles
    '''        
    diff = a2 - a1
    comp_diff = a2 + 360 - a1
    if abs(diff) < abs(comp_diff):
        return diff
    return comp_diff

def angleAdd(angle1, angle2):
    return (angle1 + angle2) % 360

def angleReduce(angle):
    angle = angle%360
    if (angle < 0):
        angle += 360
    print(angle)
    return angle

def open_wall(xdir, dist):
    if(xdir == -1 or dist == -1):
        print("open_wall: ", ai.selfTrackingDeg() + 180)
        return ai.selfTrackingDeg() + 180
    else:
        max = -1
        for i in range(12):
            #w = ai.wallFeeler(1000, angleReduce(xdir + FEELER_DIRS[i]))
            w = ai.wallFeeler(1000, xdir+FEELER_DIRS[i])
            #w = ai.wallFeeler(dist, xdir)
            if w == dist:
                print("open_wall: ", i)
                return i
            elif w > max:
                max = i
        print("open_wall: ", i)
        return i
        


def change_heading(direc, heading):
    #if (direc < 0):
    #    direc += 360

    #deg = angleDiff(heading, direc)
    #turn_to_degree(int(deg))
    turn_to_degree(heading, int(angleDiff(heading, direc)))

def change_tracking(direc, tracking, heading):
    change_heading(angleAdd(tracking, angleDiff(direc, tracking)), heading)


def AI_loop():
    
    print("--------------------------- START of frame ----------------------------")
    
    ## matches sel
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(20)
    ai.setPower(20)

    ## matches sel
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    
    print(heading)
    print(tracking)
    
    ## matches sel
    wf_1 = ai.wallFeeler(1000, tracking + 15)
    wf_2 = ai.wallFeeler(1000, tracking - 15)
    
    print("wall feeler 1", wf_1)
    print("wall feeler 2", wf_2)

    enemy = ai.closestShipId()
    
    print("closest ships id:", enemy)

    # ai.closestRadarX(): closest ships x coord (0-256) -1 if no ships on radar
    enemy_x = ai.closestRadarX()
    # ai.closestRadarY(): closest ships y coord (0-256) -1 if no ships on radar
    enemy_y = ai.closestRadarY()
    
    print("closest radar ship X coord:", enemy_x)
    print("closest radar ship Y coord:", enemy_y)

    # angle between enemy and self???
    radar_angle = int(math.degrees(math.atan(abs(enemy_y)/abs(enemy_x + 0.00000001))))
    print("radar_angle:", radar_angle)

    heading_to_enemy = angleReduce(heading - ai.aimdir(0))
    heading_to_dodge = angleReduce(heading - ai.shotVelDir(0))
    print("heading_to_enemy:", heading_to_enemy)
    print("heading_to_dodge:", heading_to_dodge)

    renemy_x = enemy_x - ai.selfRadarX() # diff between enemy x cord and self x cord
    renemy_y = enemy_y - ai.selfRadarY() # diff between enemy y cord and self y cord
    print("renemy_x: diff between enemy x and self x", renemy_x)
    print("renemy_y: diff between enemy y and self y", renemy_y)

    # if x coord diff is negative and y coord diff is positive
    if renemy_x < 0 and renemy_y > 0:
        radar_angle = 180 - radar_angle

    # if x coord diff is negative and y coord diff is negative
    elif renemy_x < 0 and renemy_y < 0:
        radar_angle = 180 + radar_angle

    # if x coord diff is positive and y coord diff is negative
    elif renemy_x > 0 and renemy_y < 0:
        radar_angle = 360 - radar_angle
        
    print(radar_angle)

    print("frame initialized ---------------------------------------------------")


    #print("open_wall: ",open_wall(tracking, 100))

    #print("wf_1: ", wf_1)
    #print("wf_2: ", wf_2)

    #print("shot alert: ", ai.shotAlert(0))
    #print("enemy id: ", enemy)
    #print("aimdir: ", ai.aimdir(0))

    #print("heading to enemy: ", heading_to_enemy)
    #print("heading to dodge: ", heading_to_dodge)

    #print("renemy_x: ", renemy_x)
    #print("renemy_y: ", renemy_y)

    #print("radar angle: ", radar_angle)
    #print("-----------------------------------------------------------------------")




    print("first logic chunk ---------------------------------------------------")
    
    if ai.shotAlert(0) > -1 and ai.shotAlert(0) < 80:
        
        print("1")
        turn_to_degree(heading, heading_to_dodge)
        #turn_to_degree(ai.angleDiff(heading, ai.angleAdd(ai.shotVelDir(0), 180)))
        ai.thrust(1)
    

    elif ai.wallBetween(ai.selfX(), ai.selfY(), enemy_x, enemy_y) > -1:

        print("2")

        id = ai.closestShipId()
        print("id: ", id)
        #change_heading(open_wall(ai.enemyTrackingDeg(0), ai.enemyDistanceId(id)), heading)
        change_heading(open_wall(heading, ai.enemyDistanceId(id)), heading)
        
        if(ai.selfSpeed() < 6):
            ai.thrust(1)


    elif ai.enemyTrackingDeg(0) > -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) < 5:

        print("3")
        change_heading(ai.enemyHeadingDeg(0), heading)
        ai.fireShot()
    
    
    elif ai.enemyTrackingDeg(0) > -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) > 5:

        print("4")
        change_heading(ai.enemyHeadingDeg(0), heading)
    
    
    elif abs(angleDiff(ai.enemyHeadingDeg(0), heading)) < 5:

        print("5")
        change_tracking(ai.enemyHeadingDeg(0), tracking, heading)
        ai.fireShot()
        
        if (abs(angleDiff(tracking, ai.enemyHeadingDeg(0))) < 15) and (ai.selfSpeed() < 7):
            ai.thrust(1)
    
    
    elif not ai.closestRadarX() < 0:

        print("6")
        deg = angleDiff(heading,  ai.enemyHeadingDeg(0))
        turn_to_degree(heading, deg)
        #turn_to_degree(angleDiff(heading, ai.enemyHeadingDeg(0)))


    print("second logic chunk ---------------------------------------------------")


    if wf_1 == wf_2 and wf_1 < (20 * ai.selfSpeed()) and ai.selfSpeed() > 1:

        print("1")
        deg = angleDiff(heading, angleAdd(tracking, 180))
        turn_to_degree(heading, int(deg))
        #turn_to_degree(angleDiff(heading, angleAdd(tracking, 180)))
	

    elif wf_1 < wf_2 and wf_1 < (20 * ai.selfSpeed()) and ai.selfSpeed() > 1:
        
        print("2")
        turn_to_degree(heading, int(angleDiff(heading, angleAdd(180, angleAdd(-15, tracking)))))
        if angleDiff(heading, angleAdd(180, angleAdd(-15, tracking))) < 30:
            ai.thrust(1)
		

    elif wf_1 > wf_2 and wf_2 < (20 * ai.selfSpeed()) and ai.selfSpeed() > 1:
        
        print("3")
        turn_to_degree(heading, int(angleDiff(heading, angleAdd(180, angleAdd(15, tracking)))))

        if angleDiff(heading, angleAdd(180, angleAdd(15, tracking))) < 30:
            ai.thrust(1)


    print("---------------------------- END of frame -----------------------------")


ai.start(AI_loop,["-name","SelPy","-join","localhost"])
