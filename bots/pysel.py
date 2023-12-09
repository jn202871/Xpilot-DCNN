''' 
Russell Kosovsky, Annika, Jay

    An attempt to rewrite the cherished bot, "sel" from C to Python.

'''

import math 
import libpyAI as ai

FEELER_DIRS = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75, 90, -90]

def turn_to_degree(heading, degree: float) -> None:
        '''turn_to_degree Turns the bot to the desired heading

        Args:
            degree (float): Heading to turn to
        '''
        #print(degree)
        delta = angleDiff(heading, degree)
        if abs(delta) > -360:
            if delta < 0:
                ai.turnRight(1)
            else:
                ai.turnLeft(1)
        else:
            turn_to_degree(heading, int(degree))


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
    return (angle1 + angle2 + 360) % 360

def angleReduce(angle):
    
    angle = angle % 360
    if (angle < 0):
        angle += 360
    #print(angle)
    return angle

def open_wall(xdir, dist):
    print("\n\nENTERED OPEN WALL")
    
    if(xdir == -1.0 and dist == 9999.0):
        return angleAdd(ai.selfTrackingDeg(), 180)
    
    else:
        max = -1
        for i in range(12):
            print("\ni: ", i)
            print("xdir: ", xdir)
            print("FEELER_DIRS[i]: ", FEELER_DIRS[i])
        
            feeler_angl = angleAdd(xdir, FEELER_DIRS[i])
            print("feeler_angl: ", feeler_angl)
            print("dist", dist)
            
            w = wall_feeler(int(dist), int(feeler_angl))
            
            if w == dist:
                return FEELER_DIRS[i]
                #return i
            elif w > max:
                #max = i
                max = FEELER_DIRS[i]
        #return i
        return FEELER_DIRS[i]
        


def change_heading(direc, heading):
    turn_to_degree(heading, int(angleDiff(heading, direc)))


def change_tracking(direc, tracking, heading):
    change_heading(angleAdd(tracking, angleDiff(direc, tracking)), heading)


def wall_feeler(Range, degree):
    
    res = ai.wallBetween(ai.selfX(), ai.selfY(), int(ai.selfX() + Range * math.cos(math.radians(degree))), int(ai.selfY() + Range * math.sin(math.radians(degree))))
	
    if res == -1: 
        return Range
    else:
        return res




def AI_loop():
    
    print("--------------------------- START of frame ----------------------------")
    
    ## matches sel
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)

    ai.setTurnSpeedDeg(20)
    ai.setPower(20)

    ## matches sel
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    
    ## matches sel
    #wf_1 = ai.wallFeeler(1000, tracking + 15)
    #wf_2 = ai.wallFeeler(1000, tracking - 15)

    wf_1 = wall_feeler(1000, 15)
    wf_2 = wall_feeler(1000, -15)

    enemy_id = ai.closestShipId() 

    print("frame initialized ---------------------------------------------------")


    print("\nfirst logic chunk ---------------------------------------------------")
    
    if ai.shotAlert(0) != -1 and ai.shotAlert(0) <= 80:
        
        print("\n--------- 1 --------- shot alert\n")

        print("heading", heading)
        print("shot vel dir", ai.shotVelDir(0))
        print("angle reduce:", angleReduce(heading - ai.shotVelDir(0)))

        #turn_to_degree(heading, angleReduce(heading - ai.shotVelDir(0)))
        turn_to_degree(heading, angleDiff(heading, angleAdd(ai.shotVelDir(0), 180)))
        ai.thrust(1)
    
    elif ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) != -1:
        
        print("\n--------- 2 --------- wall between self and enemy\n")



        if ai.enemyTrackingDegId(enemy_id) == None:
            print("enemy tracking is None")
            enemytracking = -1
        
        elif math.isnan(ai.enemyTrackingDegId(enemy_id)): 
            print("enemy tracking is NaN (not a number)")
            enemytracking = -1
        
        else:
            enemytracking = ai.enemyTrackingDegId(enemy_id)

        
        print("enemytracking:", enemytracking)
        print("enemyDistance:", ai.enemyDistanceId(enemy_id))
        print("heading:", heading)
        
        
        opn_wall = open_wall(enemytracking, ai.enemyDistanceId(enemy_id))

        print("opn_wall", opn_wall)

        #turn_to_degree(heading, int(angleDiff(heading, opn_wall)))
        
        change_heading(opn_wall, heading)
        if(ai.selfSpeed() <= 7):
            ai.thrust(1)


    elif ai.enemyTrackingDeg(0) != -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) < 5:
        print("\n--------- 3 ---------\n")

        change_heading(ai.enemyHeadingDeg(0), heading)
        ai.fireShot()
    
    
    elif ai.enemyTrackingDeg(0) != -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) > 5:
        print("\n--------- 4 ---------\n")
        
        change_heading(ai.enemyHeadingDeg(0), heading)
    
    
    elif abs(angleDiff(ai.enemyHeadingDeg(0), heading)) < 5:
        print("\n--------- 5 ---------\n")

        change_tracking(ai.enemyHeadingDeg(0), tracking, heading)
        ai.fireShot()
        
        if (abs(angleDiff(tracking, ai.enemyHeadingDeg(0))) < 15) and (ai.selfSpeed() < 7):
            ai.thrust(1)
    

    elif ai.closestRadarX() != -1:
        print("\n--------- 6 ---------\n")
        
        deg = angleDiff(heading, ai.enemyHeadingDeg(0))
        
        turn_to_degree(heading, deg)






    print("\n\nsecond logic chunk ---------------------------------------------------")

    print("wf1: ", wf_1)
    print("wf2: ", wf_2)


    #if wf_1 == wf_2 and wf_1 < (20 * ai.selfSpeed()) and ai.selfSpeed() > 1:
    if wf_1 == wf_2 and ai.selfSpeed() > 1:

        print("\n--------- 1 ---------\n")

        deg = angleDiff(heading, angleAdd(tracking, 180))
        turn_to_degree(heading, deg)
        
	

    elif wf_1 < wf_2 and ai.selfSpeed() > 1:
        print("\n--------- 2 ---------\n")

        turn_to_degree(heading, angleDiff(heading, angleAdd(180, angleAdd(-15, tracking))))
        
        if angleDiff(heading, angleAdd(180, angleAdd(-15, tracking))) < 30:
            ai.thrust(1)
		



    elif wf_1 > wf_2 and ai.selfSpeed() > 1:
        print("\n--------- 3 ---------\n")

        turn_to_degree(heading, angleDiff(heading, angleAdd(180, angleAdd(15, tracking))))

        if angleDiff(heading, angleAdd(180, angleAdd(15, tracking))) < 30:
            ai.thrust(1)


    print("---------------------------- END of frame -----------------------------\n\n\n")


ai.start(AI_loop,["-name","SelPy","-join","localhost"])
