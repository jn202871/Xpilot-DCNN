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
    if(xdir == -1.0 or dist == 9999.0):
        #print("open_wall: ", ai.selfTrackingDeg())
        return ai.selfTrackingDeg()
    else:
        max = -1
        for i in range(12):
            print("\ni: ", i)
            print("xdir: ", xdir)
            print("FEELER_DIRS[i]: ", FEELER_DIRS[i])
        
            
            feeler_angl = angleAdd(xdir, FEELER_DIRS[i])
            print("feeler_angl: ", feeler_angl)

            print("dist", dist)
            
            w = ai.wallFeeler(int(dist), int(feeler_angl))
            if w == dist:
                #print("open_wall: ", i)
                return FEELER_DIRS[i]
            elif w > max:
                max = FEELER_DIRS[i]
        #print("open_wall: ", i)
        return FEELER_DIRS[i]
        


def change_heading(direc, heading):
    #if (direc < 0):
    #    direc += 360

    turn_to_degree(heading, int(angleDiff(heading, direc)))
    #ai.turn(int(angleDiff(heading, direc)))


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
    
    ## matches sel
    wf_1 = ai.wallFeeler(1000, tracking + 15)
    wf_2 = ai.wallFeeler(1000, tracking - 15)

    enemy = ai.closestShipId()
    
    # ai.closestRadarX(): closest ships x coord (0-256) -1 if no ships on radar
    enemy_x = ai.closestRadarX()
    # ai.closestRadarY(): closest ships y coord (0-256) -1 if no ships on radar
    enemy_y = ai.closestRadarY()
    
    # angle between enemy and self???
    radar_angle = int(math.degrees(math.atan(abs(enemy_y)/abs(enemy_x + 0.00000001))))

    heading_to_enemy = angleReduce(heading - ai.aimdir(0))
    heading_to_dodge = angleReduce(heading - ai.shotVelDir(0))

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
    
    print("frame initialized ---------------------------------------------------")

    
    # print(heading)
    # print(tracking)

    # print("wall feeler 1", wf_1)
    # print("wall feeler 2", wf_2)
    # print("closest ships id:", enemy)
    # print("closest radar ship X coord:", enemy_x)
    # print("closest radar ship Y coord:", enemy_y)
    # print("radar_angle:", radar_angle)
    # print("heading_to_enemy:", heading_to_enemy)
    # print("heading_to_dodge:", heading_to_dodge)
    # print("renemy_x: diff between enemy x and self x", renemy_x)
    # print("renemy_y: diff between enemy y and self y", renemy_y)

    # print(radar_angle)
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


########################################################################################
########################################################################################
# LOGIC CHUNKS
# 

    print("\n--------- 1 --------- shot alert")

    # ai.shotAlert(0) > -1 
    # and
    # ai.shotAlert(0) < 80

#    int shotAlert(int idx) 
#        - Returns a danger rating of a shot, the smaller the 
#          number the more likely the shot is to hit the ship.
#        - will return -1 if the buffer has no shot at the given index.  

    # OG:
    print(ai.shotAlert(0) > -1 and ai.shotAlert(0) < 80)
    # IMPROVED:
    print(ai.shotAlert(0) != -1 and ai.shotAlert(0) <= 80)

########################################################################################
    
    print("\n--------- 2 --------- wall between self and enemy")

    # ai.wallBetween(ai.selfX(), ai.selfY(), enemy_x, enemy_y) > -1
    
#    int wallBetween(int x1, int y1, int x2, int y2) 
#       - If there is a wall between the given points it returns the distance from point 1 to the first found wall.  
#       - If no wall is found it returns -1.
    
    print(ai.selfX()) # Returns the ship's X position on the map.
    print(ai.selfY()) # Returns the ship's Y position on the map.

    # Ships are sorted from near (nearest at index 0) to far.  
    # Only ships that are on screen should be accessible.

    print(ai.screenEnemyX(0)) # Returns the specified enemy's X coordinate on the map. else -1
    print(ai.screenEnemyY(0)) # Returns the specified enemy's Y coordinate on the map. else -1


    
    # OG:
    print(ai.wallBetween(ai.selfX(), ai.selfY(), enemy_x, enemy_y) > -1)
    # IMPROVED:
    print(ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) != -1)

########################################################################################

    print("\n--------- 3 ---------")

    # ai.enemyTrackingDeg(0) > -1 
    # and 
    # abs(angleDiff(heading, ai.enemyHeadingDeg(0))) < 5

    print(angleDiff(heading, ai.enemyHeadingDeg(0)))
    print(abs(angleDiff(heading, ai.enemyHeadingDeg(0))))

    
    # OG:
    print(ai.enemyTrackingDeg(0) > -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) < 5)
    # IMPROVED:
    print(ai.enemyTrackingDeg(0) != -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) < 5)

########################################################################################

    print("\n--------- 4 ---------")

    # ai.enemyTrackingDeg(0) > -1 
    # and 
    # abs(angleDiff(heading, ai.enemyHeadingDeg(0))) > 5
    
    # OG:
    print(ai.enemyTrackingDeg(0) > -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) > 5)
    # IMPROVED:
    print(ai.enemyTrackingDeg(0) != -1 and abs(angleDiff(heading, ai.enemyHeadingDeg(0))) > 5)

########################################################################################

    print("\n--------- 5 ---------")

    # abs(angleDiff(ai.enemyHeadingDeg(0), heading)) < 5
    
    print(ai.enemyHeadingDeg(0))
    print(heading)
    print(abs(angleDiff(ai.enemyHeadingDeg(0), heading)))

    # OG:    
    print(abs(angleDiff(ai.enemyHeadingDeg(0), heading)) < 5)

########################################################################################

    print("\n--------- 6 ---------")  ## IMPROVED BUT STILL EQUIVALENT
    # not ai.closestRadarX() > 0
    
#    int closestRadarX() 
#        - Returns the closest ship's X radar coordinate. 
#          (0-256)  Returns -1 if there are no ships on the radar.

    # OG:
    print(not ai.closestRadarX() > 0)
    # IMPROVED:
    print(ai.closestRadarX() != -1)


########################################################################################
########################################################################################

    print("\n--------- 1 ---------")

    print("\n--------- 2 ---------")

    print("\n--------- 3 ---------")
    
########################################################################################
########################################################################################


    print("\nfirst logic chunk ---------------------------------------------------")
    
    if ai.shotAlert(0) != -1 and ai.shotAlert(0) <= 80:
        print("\n--------- 1 --------- shot alert\n")

        turn_to_degree(heading, heading_to_dodge)
        #turn_to_degree(ai.angleDiff(heading, ai.angleAdd(ai.shotVelDir(0), 180)))
        ai.thrust(1)
    

    elif ai.wallBetween(ai.selfX(), ai.selfY(), ai.screenEnemyX(0), ai.screenEnemyY(0)) != -1:
        print("\n--------- 2 --------- wall between self and enemy\n")

        id = ai.closestShipId()

        if ai.enemyTrackingDegId(id) == None:
            print("enemy tracking is None")
            enemytracking = -1
        elif math.isnan(ai.enemyTrackingDegId(id)): 
            print("enemy tracking is NaN (not a number)")
            enemytracking = -1
        else:
            enemytracking = ai.enemyTrackingDegId(id)

        print("ID", id)
        print("ai.enemyTrackingDegId(id):", ai.enemyTrackingDegId(id))
        print("enemytracking", enemytracking)
        print("ai.enemyDistanceId(id) (dist):", ai.enemyDistanceId(id))
        print("heading", heading)
        
        opn_wall = open_wall(enemytracking, ai.enemyDistanceId(id))

        print("opn_wall", opn_wall)

        change_heading(opn_wall, heading)
        
        if(ai.selfSpeed() < 6):
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
        
        deg = angleDiff(heading,  ai.enemyHeadingDeg(0))
        
        turn_to_degree(heading, deg)



    print("\n\nsecond logic chunk ---------------------------------------------------")


    if wf_1 == wf_2 and wf_1 < (20 * ai.selfSpeed()) and ai.selfSpeed() > 1:
        print("\n--------- 1 ---------\n")

        deg = angleDiff(heading, angleAdd(tracking, 180))
        turn_to_degree(heading, deg)
        #turn_to_degree(angleDiff(heading, angleAdd(tracking, 180)))
	

    elif wf_1 < wf_2 and wf_1 < (20 * ai.selfSpeed()) and ai.selfSpeed() > 1:
        print("\n--------- 2 ---------\n")

        turn_to_degree(heading, angleDiff(heading, angleAdd(180, angleAdd(-15, tracking))))
        if angleDiff(heading, angleAdd(180, angleAdd(-15, tracking))) < 30:
            ai.thrust(1)
		

    elif wf_1 > wf_2 and wf_2 < (20 * ai.selfSpeed()) and ai.selfSpeed() > 1:
        print("\n--------- 3 ---------\n")

        turn_to_degree(heading, angleDiff(heading, angleAdd(180, angleAdd(15, tracking))))

        if angleDiff(heading, angleAdd(180, angleAdd(15, tracking))) < 30:
            ai.thrust(1)


    print("---------------------------- END of frame -----------------------------\n\n\n")


ai.start(AI_loop,["-name","SelPy","-join","localhost"])
