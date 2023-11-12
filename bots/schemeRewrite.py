import random
import math

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
    wall_feeler0 = ai.wallFeeler(500, tracking)
    wall_feeler1 = ai.wallFeeler(500, tracking + 15)
    wall_feeler2 = ai.wallFeeler(500, tracking - 15)
    wall_feeler3 = ai.wallFeeler(500, tracking + 30)
    wall_feeler4 = ai.wallFeeler(500, tracking - 30)
    wall_feeler5 = ai.wallFeeler(500, tracking + 45)
    wall_feeler6 = ai.wallFeeler(500, tracking - 45)
    wall_feeler7 = ai.wallFeeler(500, tracking + 60)
    wall_feeler8 = ai.wallFeeler(500, tracking - 60)
    wall_feeler9 = ai.wallFeeler(500, tracking + 75)
    wall_feeler10 = ai.wallFeeler(500, tracking - 75)
    wall_feeler11 = ai.wallFeeler(500, tracking + 90)
    wall_feeler12 = ai.wallFeeler(500, tracking - 90)
    
    renemy_x = renemy_x - ai.selfRadarX()
    renemy_y = renemy_y - ai.selfRadarY()

 
    # Skipped msg stuff
    
    if ai.selfAlive() == 1:
        
        if (ai.shotAlert(0) > -1) and (ai.shotAlert(0) < 60):
            ai.turnToDeg(angleDiff(ai.selfHeadingDeg(), ai.angleAdd(ai.shotVelDir(0), 180))
            ai.thrust(1)

