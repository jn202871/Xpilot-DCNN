import xpai, math

#Morthon - sample simple bot. attacks, avoids walls (sort of), and dodges bullets
#to run this script enter "python morthon.py" in the command line, with no quotation marks

#wall feeler checks for walls at some degree and range from self ship
def wall_feeler(range, degree):
	res = xpai.wallbetween(xpai.self_x(), xpai.self_y(), xpai.self_x() + range * math.cos( xpai.rad (degree)), xpai.self_y() + range * math.sin( xpai.rad( degree)))
	if (res == -1):
		return range
	else:
		return res

#gets nearest enemy on screen or returns -1 if no enemy
def screen_enemy_num (n): 
	if (xpai.ship_x(n) == -1):
		return -1
	elif (xpai.teamplay() == 1 and  xpai.self_team() != xpai.ship_team(n)):
		return n
	else:
		return screen_enemy_num(n + 1)


#gets nearest enemy on radar or returns -1 if none
def radar_enemy_num (n):
	if (xpai.radar_x(n) == -1):
		return -1
	elif (xpai.radar_enemy(n) == 1):
		return n
	else:
		return radar_enemy_num(n + 1)

def AImain():
	xpai.setmaxturn(20)
	shipnum = screen_enemy_num(0)
	rshipnum = radar_enemy_num(0)
	wall_feeler1 = wall_feeler(500, xpai.angleadd(xpai.self_track(), -15))
	wall_feeler2 = wall_feeler(500, xpai.angleadd(xpai.self_track(), 15))

	if (xpai.shot_alert(0) > -1) and (xpai.shot_alert(0) < 80):
		xpai.self_turn(xpai.anglediff(xpai.self_heading(), xpai.angleadd(xpai.shot_idir(0), 90)))
		xpai.self_thrust(1)
	elif (shipnum > -1):
		xpai.self_turn(xpai.anglediff(xpai.self_heading(), xpai.ship_aimdir(shipnum)))
		xpai.self_shoot(1)
	elif (rshipnum > -1):
		xpai.self_turn(xpai.anglediff(xpai.self_heading(), xpai.radar_xdir(rshipnum)))
		if (xpai.self_vel() < 10):
			xpai.self_thrust(1)
		else:
			xpai.self_shoot(1)


	if ((wall_feeler1 == wall_feeler2) and (wall_feeler1 < (20 * xpai.self_vel())) and (xpai.self_vel() > 1)):
		xpai.self_turn(xpai.anglediff(xpai.self_heading(), xpai.angleadd(180, xpai.self_track())))
		xpai.self_thrust(1)
	elif ((wall_feeler1 < wall_feeler2) and (wall_feeler1 < (20 * xpai.self_vel())) and (xpai.self_vel() > 1)):
		xpai.self_turn(xpai.anglediff(xpai.self_heading(), xpai.angleadd(180, xpai.angleadd(-15, xpai.self_track()))))
		xpai.self_thrust(1)	
	elif ((wall_feeler1 > wall_feeler2) and (wall_feeler1 < (20 * xpai.self_vel())) and (xpai.self_vel() > 1)):
		xpai.self_turn(xpai.anglediff(xpai.self_heading(), xpai.angleadd(180, xpai.angleadd(15, xpai.self_track()))))
		xpai.self_thrust(1)

	return
	

xpai.set_AImain(AImain)


xpai.setargs("-join localhost -name Morthon")
xpai.launch()
