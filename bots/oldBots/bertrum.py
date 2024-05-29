import math
import random
import libpyAI as ai


def turn_to_degree(heading, degree: float) -> None:
        '''turn_to_degree Turns the bot to the desired heading

        Args:
            degree (float): Heading to turn to
        '''
        #print(degree)
        delta = angle_diff(heading, degree)
        if abs(delta) > -360:
            if delta < 0:
                ai.turnRight(1)
            else:
                ai.turnLeft(1)
        else:
            turn_to_degree(heading, int(degree))


def angle_diff(a1: float, a2: float) -> float:
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

def angle_add(angle1, angle2):
    return (angle1 + angle2 + 360) % 360

def angleReduce(angle):
    
    angle = angle % 360
    if (angle <= 0):
        angle += 360
    #print(angle)
    return angle


def change_heading(direc, heading):
    turn_to_degree(heading, int(angle_diff(heading, direc)))


def change_tracking(direc, tracking, heading):
    change_heading(angle_add(tracking, angle_diff(direc, tracking)), heading)


def wall_feeler(Range, degree):
    
    res = ai.wallBetween(ai.selfX(), ai.selfY(), int(ai.selfX() + Range * math.cos(math.radians(degree))), int(ai.selfY() + Range * math.sin(math.radians(degree))))
	
    if res == -1: 
        return Range
    else:
        return res


max_speed: int = 3
desired_speed: int = 3
safety_margin: int = 12
turnspeed: int = 20
power_level: float = 28.0
scan_distance: int = 1000
cpa_check_distance = 500
thrust_heading_tolerance: int = 10
e_thrust_heading_tolerance: int = 15
wall_threshold: int = 50
firing_threshold: int = 5
max_shot_distance: int = 800

desired_heading: float = 0
desired_thrust: int = 0
last_radar_heading: float = 0
global current_frame

def AI_loop():
    '''run_loop Runs on every frame to control the bot
    '''

    print("--------------------------- START of frame ----------------------------")

    if ai.selfAlive() == 0:
        current_frame = 0

    current_frame = current_frame + 1

    # reset default flags
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeedDeg(turnspeed)
    ai.setPower(power_level)   
    
    max_turntime = math.ceil(180 / turnspeed)



    #check_walls()

    # check_walls Checks for possible wall collisions and sets flags accordingly if necessary
    x = ai.selfX()
    y = ai.selfY()
    x_vel = ai.selfVelX()
    y_vel = ai.selfVelY()
    
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    speed: float = ai.selfSpeed()
    track_wall = ai.wallFeeler(scan_distance, tracking)
    
    tt_tracking = math.ceil(track_wall / (speed + 0.0000001))
    tt_retro = math.ceil(speed / power_level)

    # update_closest_wall Updates the closest wall distance and heading
    closest_wall = scan_distance
    closest_wall_heading = -1
    
    for degree in range(0, 360, 30):
        wall = ai.wallFeeler(scan_distance, degree)
        if wall < closest_wall:
            closest_wall = wall
            closest_wall_heading = degree

    if closest_wall < wall_threshold:
        turn = True
        desired_heading = angle_add(closest_wall_heading, 180)
        
        tolerance = thrust_heading_tolerance
        if abs(angle_diff(heading, desired_heading)) < tolerance:
            thrust = True

        if tt_tracking < tt_retro + 1:
            thrust = True

        # if an enemy is all lined up     
        nearest_aim_dir = ai.aimdir(0)
        if nearest_aim_dir != -1:
            delta = abs(angle_diff(heading, nearest_aim_dir))
            if delta < 10:
                shoot = True


    ##print(f'speed: {speed} tth: {tt_tracking} dist: {track_wall} ttr: {tt_retro}')
    if tt_tracking < max_turntime + tt_retro + safety_margin:
        turn = True
        desired_heading = angle_add(tracking, 180)
        
        tolerance = thrust_heading_tolerance
        if abs(angle_diff(heading, desired_heading)) < tolerance:
            thrust = True

        # if an enemy is all lined up     
        nearest_aim_dir = ai.aimdir(0)
        if nearest_aim_dir != -1:
            delta = abs(angle_diff(heading, nearest_aim_dir))
            if delta < 10:
                shoot = True
        
###############################################################################################################################

    #check_shots():

    '''check_shots Checks for possible bullet collisions using shot alert values and sets flags accordingly if necessary
    '''

    idx = 0
    lowest_idx = -1
    lowest_alert = 3000
    next_shot_alert = ai.shotAlert(idx)
    while next_shot_alert != -1:
        if next_shot_alert < lowest_alert:
            lowest_alert = next_shot_alert
        idx += 1
        next_shot_alert = ai.shotAlert(idx)
    
    if lowest_alert < 50:
        shot_vel_dir = tracking
        turn = True
        left_option = angle_add(shot_vel_dir, 75)
        right_option = angle_add(shot_vel_dir, -75)
        
        if angle_diff(heading, left_option) < angle_diff(heading, right_option):
            desired_heading = left_option
        desired_heading = right_option

        e_thrust_heading_tolerance = thrust_heading_tolerance
        if abs(angle_diff(heading, desired_heading)) < e_thrust_heading_tolerance:
            thrust = True
        if lowest_alert < 50:
            thrust = True
        
        ##print(f'Dodging shot, turning to {desired_heading}')


    
###############################################################################################################################

    #check_kills()

    ##print(f'{username}: Aggressive')

    if ai.aimdir(0) != -1:
        turn = True
        desired_heading = ai.aimdir(0)

        if abs(angle_diff(heading, desired_heading)) < 5:
            shoot = True
            ##print(f'{username}: Shooting')


        if current_frame % 133 == 0:
            thrust = True


###############################################################################################################################

    #check_ships():
    ##print(f'{username}: Avoiding ship')

    # check_ships Checks for possible ship collisions using CPA prediction and sets flags accordingly if necessary
     
    idx = 0
    next_ship_dist = ai.enemyDistance(idx)
    
    while next_ship_dist != -1 and next_ship_dist < cpa_check_distance:
        enemy_x = ai.screenEnemyX(idx)
        enemy_y = ai.screenEnemyY(idx)
        enemy_speed = ai.enemySpeed(idx)
        enemy_tracking = ai.enemyTrackingDeg(idx)
        

        heading_rad = math.radians(enemy_tracking)
        enemy_x_vel: float = enemy_speed * math.cos(heading_rad)
        enemy_y_vel: float = enemy_speed * math.sin(heading_rad)

        found_min = False
        last_dist: float = math.sqrt((enemy_x - enemy_x) ** 2 + (enemy_y - enemy_y) ** 2)
        t: int = 1
        while not found_min:
            
            current_dist = math.sqrt((enemy_x + x_vel * t - enemy_x + enemy_x_vel * t) ** 2 + (enemy_y + y_vel * t - enemy_y + enemy_y_vel * t) ** 2)
            
            if current_dist < last_dist:
                t += 1
                last_dist = current_dist
            else:
                found_min = True
        
        enemy_cpa_time = t
        enemy_cpa_distance = last_dist


        if enemy_speed < 1:
            break
        
        ##print(f'{ai.enemyName(idx)} cpa time: {enemy_cpa_time} - dist: {enemy_cpa_distance}')
        if enemy_cpa_distance < 50:
            if enemy_cpa_time < max_turntime:
                turn = True
                left_option = angle_add(enemy_tracking, 90)
                right_option = angle_add(enemy_tracking, -90)
                
                if angle_diff(heading, left_option) < angle_diff(heading, right_option):
                    desired_heading = left_option
                desired_heading = right_option
                ##print(f'{ai.enemyName(idx)} is close, turning to {desired_heading}')
                thrust = True

            if enemy_cpa_time < tt_retro + safety_margin + max_turntime:
                turn = True
                left_option = angle_add(enemy_tracking, 90)
                right_option = angle_add(enemy_tracking, -90)
                
                if angle_diff(heading, left_option) < angle_diff(heading, right_option):
                    desired_heading = left_option
                desired_heading = right_option
                
                
                tolerance = thrust_heading_tolerance
                if abs(angle_diff(heading, desired_heading)) < tolerance:
                    thrust = True
                
                ##(f'{ai.enemyName(idx)} is close, turning to {desired_heading}')

                # if an enemy is all lined up     
                nearest_aim_dir = ai.aimdir(0)
                if nearest_aim_dir != -1:
                    delta = abs(angle_diff(heading, nearest_aim_dir))
                    if delta < 10:
                        shoot = True

        idx += 1
        next_ship_dist = ai.enemyDistance(idx)


    
###############################################################################################################################
    #check_speed():
    ##print(f'{username}: Slowing down')

    #check_speed Checks if the ship is going faster than the set maximum speed and sets flags accordingly if necessary
   
    if speed > max_speed:
        desired_heading = angle_add(tracking, 180)
        turn = True
        
        tolerance = thrust_heading_tolerance
        if abs(angle_diff(heading, desired_heading)) < tolerance:
            thrust = True

    
###############################################################################################################################
    #check_position():
    ##print(f'{username}: Moving to center')

    # check_position Brings the ship closer to the center of the screen if it is too far away
     
    if closest_wall < 400:
        turn = True
        desired_heading = angle_add(
            closest_wall_heading, 180)
        delta = abs(angle_diff(
            tracking, closest_wall_heading))
        delta_desired = abs(angle_diff(
            heading, desired_heading))
        if delta_desired < 30 and (delta < 140 or speed < desired_speed):
            thrust = True
    elif speed > 1:
        turn = True
        desired_heading = angle_add(tracking, 180)
        
        if abs(angle_diff(heading, desired_heading)) < 5:
            thrust = True

###############################################################################################################################
    #check_radar():
    ##print(f'{username}: Enemy Detected On Radar')

        # check_radar Checks for enemies on the radar and sets flags accordingly if necessary
    
    x_diff = ai.closestRadarX()
    if x_diff != -1:
        y_diff = ai.closestRadarY()
        x_diff = ai.selfRadarX()
        y_diff = ai.selfRadarY()

        x_diff = x_diff - x_diff
        y_diff = y_diff - y_diff

        radar_angle = math.degrees(
            math.atan(abs(y_diff) / abs(x_diff + 0.0000001)))

        if x_diff < 0 and y_diff > 0:
            radar_angle = 180 - radar_angle
        elif x_diff < 0 and y_diff < 0:
            radar_angle = 180 + radar_angle
        elif x_diff > 0 and y_diff < 0:
            radar_angle = 360 - radar_angle
        #temp = last_radar_heading
        #last_radar_heading = radar_angle
        #radar_angle += angle_diff(temp, radar_angle)
        desired_heading = radar_angle
        turn = True

        if abs(angle_diff(heading, desired_heading)) < 5 and abs(x_diff) > 8 and abs(y_diff) > 8 and current_frame % 48 == 0:
            shoot = True
        ##print(f'Radar@ {x_diff},{y_diff} - {radar_angle}')

    '''production_system Uses the three flags to execute the desired actions for the bot
    '''
    if turn and thrust and shoot:
        turn_to_degree(heading, desired_heading)
        ai.thrust(1)
        ai.fireShot()
    elif turn and thrust:
        turn_to_degree(heading, desired_heading)
        ai.thrust(1)
    elif turn and shoot:
        turn_to_degree(heading, desired_heading)
        ai.thrust(0)
        ai.fireShot()
    elif thrust and shoot:
        ai.thrust(1)
        ai.fireShot()
    elif turn:
        turn_to_degree(heading, desired_heading)
        ai.thrust(0)
    elif thrust:
        ai.thrust(1)
    elif shoot:
        ai.fireShot()
    else:
        ai.thrust(0)


    print("---------------------------- END of frame -----------------------------\n\n\n")


ai.start(AI_loop,["-name","BERTRUM","-join","localhost"])
