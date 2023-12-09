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
current_frame: int = 0

def AI_loop():
    '''run_loop Runs on every frame to control the bot
    '''

    print("--------------------------- START of frame ----------------------------")

    if ai.selfAlive() == 0:
        current_frame = 0
    
    ai.setTurnSpeedDeg(turnspeed)
    current_frame += 1

    # reset default flags
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeedDeg(20)
    ai.setPower(20)

    # reset action flags
    turn, thrust, shoot = False, False, False
    
    max_turntime = math.ceil(180 / turnspeed)

    ## set_flags Progressively examines the bot's environment until a flag is set

    # check_walls Checks for possible wall collisions and sets flags accordingly if necessary
    x = ai.selfX()
    y = ai.selfY()
    x_vel = ai.selfVelX()
    y_vel = ai.selfVelY()
    
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    speed: float = ai.selfSpeed()
    track_wall = ai.wallFeeler(scan_distance, tracking)
    tt_tracking = math.ceil(
        track_wall / (speed + 0.0000001))
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
        desired_heading = angle_add(
            closest_wall_heading, 180)
        
        if tolerance is None:
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
        
        if tolerance is None:
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

        if e_thrust_heading_tolerance is None:
            e_thrust_heading_tolerance = thrust_heading_tolerance
        if abs(angle_diff(heading, desired_heading)) < e_thrust_heading_tolerance:
            thrust = True
        if lowest_alert < 50:
            thrust = True
        
        ##print(f'Dodging shot, turning to {desired_heading}')


    
###############################################################################################################################

    ##print(f'{username}: Aggressive')

    if ai.aimdir(0) != -1:
        turn = True
        desired_heading = ai.aimdir(0)

        if abs(angle_diff(heading, desired_heading)) < 5:
            shoot = True
            ##print(f'{self.username}: Shooting')


        if current_frame % 133 == 0:
            thrust = True


###############################################################################################################################

    #check_ships():
    ##print(f'{username}: Avoiding ship')



    
###############################################################################################################################

    #check_speed():
    ##print(f'{username}: Slowing down')

    
###############################################################################################################################

    #check_position():
    ##print(f'{username}: Moving to center')


###############################################################################################################################

    #check_radar():
    ##print(f'{username}: Enemy Detected On Radar')


###############################################################################################################################

    else:
        desired_heading = heading + random.randint(0, 20)
        turn = True
        shoot = False


    '''production_system Uses the three flags to execute the desired actions for the bot
    '''
    if turn and thrust and shoot:
        turn_to_degree(desired_heading)
        ai.thrust(1)
        ai.fireShot()
    elif turn and thrust:
        turn_to_degree(desired_heading)
        ai.thrust(1)
    elif turn and shoot:
        turn_to_degree(desired_heading)
        ai.thrust(0)
        ai.fireShot()
    elif thrust and shoot:
        ai.thrust(1)
        ai.fireShot()
    elif turn:
        turn_to_degree(desired_heading)
        ai.thrust(0)
    elif thrust:
        ai.thrust(1)
    elif shoot:
        ai.fireShot()
    else:
        ai.thrust(0)


    #Gotta get those free spawn kills
    if current_frame < 5:
        ai.fireShot()
        if current_frame < 2:
            ai.thrust(1)


    print("---------------------------- END of frame -----------------------------\n\n\n")


ai.start(AI_loop,["-name","SelPy","-join","localhost"])
