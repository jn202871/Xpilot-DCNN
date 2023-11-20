#include "xpilot_ai.h"
#include <string.h>
#include <math.h>

int wall_feeler(int range, int degree);
int screen_enemy_num (int n);
int radar_enemy_num (int n);
int open_wall(int xdir, int dist);
int change_tracking(int dir);
int change_heading(int dir);
void init_feeler_dirs(void);

int feeler_dirs[13];

int main (int argc, char **argv) {
	init_feeler_dirs();
	AI_setmaxturn (20);
	AI_xpilot_setargs("-join slughorn.conncoll.edu -port 57489 -name SelX");
	AI_xpilot_launch();
	
	return 1;
}

void AImain(void) {
	int shipnum = screen_enemy_num(0);
	int rshipnum = radar_enemy_num(0);
	
	int wall_feeler1 = wall_feeler(500, feeler_dirs[1]);
	int wall_feeler2 = wall_feeler(500, feeler_dirs[2]);

	//xdir=direction to shoot to hit the ship, # degrees to represent direction you should shoot in
    //If we're alive then, do all these ifs and elifs
	if (AIself_alive()) {
		
		/**
		If we're getting shot at, but the danger is less than 80
		Then *see below* and thrust
		TODO: figure out what idir is, figure out what turn is (is it trying to do turnToDeg or turning to the right as much as it can?
		*/
		if ((AIshot_alert(0) > -1) && (AIshot_alert(0) < 80)) {
			AIself_turn(anglediff(AIself_heading(), angleadd(AIshot_idir(0), 180)));
			AIself_thrust(1);
		
		/**
		If there is a wall between us and the enemy
		Then call function change_heading (see below) with parameter being the 
		*/
		} else if (AI_wallbetween(AIself_x(), AIself_y(), AIship_x(shipnum), AIship_y(shipnum)) != -1) {
			change_heading(open_wall(AIship_xdir(shipnum), AIship_dist(shipnum)));
			if (AIself_vel() < 6) AIself_thrust(1);
		} else if ((AIship_xdir(shipnum) > -1) && (abs(anglediff(AIself_heading(), AIship_aimdir(shipnum))) < 5)) {
			change_heading(AIship_aimdir(shipnum));
			AIself_shoot(1);
		} else if ((AIship_xdir(shipnum) > -1) && (abs(anglediff(AIself_heading(), AIship_aimdir(shipnum))) > 5)) {
			change_heading(AIship_aimdir(shipnum));
		} else if (abs(anglediff(AIradar_xdir(rshipnum), AIself_heading())) < 5) {
			change_tracking(AIradar_xdir(rshipnum));
			AIself_shoot(1);
			if (!((abs(anglediff(AIself_track(), AIradar_xdir(rshipnum))) < 15) && (AIself_vel() < 7))) AIself_thrust(1);

			
		//RUSSELL: FIGURE OUT WHAT EACH OF THE CONDITIONALS BELOW ARE DOING (IN WORDS)	

		} else if (!(AIradar_x(rshipnum) < 0)) {
			AIself_turn(anglediff(AIself_heading(), AIradar_xdir(rshipnum)));
		}

		if ((wall_feeler1 == wall_feeler2) && (wall_feeler1 < (20 * AIself_vel())) && (AIself_vel() > 1)) {

			AIself_turn(anglediff(AIself_heading(), angleadd(AIself_track(), 180)));
		} 
		
		else if ((wall_feeler1 < wall_feeler2) && (wall_feeler1 < (20 * AIself_vel())) && (AIself_vel() > 1)) {

			AIself_turn(anglediff(AIself_heading(), angleadd(180, angleadd(-15, AIself_track()))));
			if (anglediff(AIself_heading(), angleadd(180, angleadd(-15, AIself_track()))) < 30) AIself_thrust(1);
		} 
		
		else if ((wall_feeler1 > wall_feeler2) && (wall_feeler2 < (20 * AIself_vel())) && (AIself_vel() > 1)) {
			
			AIself_turn(anglediff(AIself_heading(), angleadd(180, angleadd(15, AIself_track()))));
			if (anglediff(AIself_heading(), angleadd(180, angleadd(15, AIself_track()))) < 30) AIself_thrust(1);
		}
	}
	return;
}

int wall_feeler(int range, int degree) {
	int res = AI_wallbetween(AIself_x(), AIself_y(), AIself_x() +  range * cos( rad (degree)), AIself_y() + range * sin(rad( degree)));
	if (res == -1) 
		return range;
		return res;
}

int open_wall(int xdir, int dist) {
	if ((xdir == -1) || (dist == -1))
		return angleadd(AIself_track(), 180);
	else {
		int max = -1;
		int i;
		for (i = 0; i <= 12; i++) {
			int w = wall_feeler(dist, angleadd(xdir, feeler_dirs[i]));
			if (w == dist) return i;
			else if (w > max) max = i;
		}
		return i;
	}
}

int change_tracking(int dir) {
	change_heading(angleadd(AIself_track(), anglediff(dir, AIself_track())));
}
//TODO:  figure out what idir is, figure out what turn is (is it trying to do turnToDeg or turning to the right as much as it can?
int change_heading(int dir) {
	AIself_turn(anglediff(AIself_heading(), dir));
}

int screen_enemy_num (int n) {
	if (AIship_x(n) == -1) return -1;
	else if (AI_teamplay() == 1 && AIself_team() != AIship_team(n)) return n;
	else return screen_enemy_num(n + 1);
}

int radar_enemy_num (int n) {
	if (AIradar_x(n) == -1) return -1;
	else if (AIradar_enemy(n) == 1) return n;
	else return radar_enemy_num(n + 1);
}

void init_feeler_dirs(void) {
	feeler_dirs[0] = 0;
	feeler_dirs[1] = 15;
	feeler_dirs[2] = -15;
	feeler_dirs[3] = 30;
	feeler_dirs[4] = -30;
	feeler_dirs[5] = 45;
	feeler_dirs[6] = -45;
	feeler_dirs[7] = 60;
	feeler_dirs[8] = -60;
	feeler_dirs[9] = 75;
	feeler_dirs[10] = -75;
	feeler_dirs[11] = 90;
	feeler_dirs[12] = -90;
}
