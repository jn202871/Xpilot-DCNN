/*foreign interface*/

void AI_xpilot_setargs (char *args);
void AI_xpilot_setargv (int argc, char **argv);
int AI_xpilot_launch (void);

void AIself_thrust (int thrust);
void AIself_turn (int turn);
void AIself_shoot (int shoot);
void AIself_shield_enable (int shield);

void AI_talk (char *message);
char* AImsg_to (int which);
char* AImsg_from (int which);
char* AImsg_body (int which);


int AI_teamplay (void);	

int AIself_id (void);
int AIself_alive (void);
int AIself_x (void);
int AIself_y (void);
int AIself_heading (void);
int AIself_vel (void);
int AIself_track (void);
int AIself_mapx (void);
int AIself_mapy (void);
int AIself_team (void);
int AIself_life (void);
int AIself_shield (void);
char* AIself_name (void);
float AIself_score (void);
int AIself_reload (void);
void AIself_destruct (void);

void AI_presskey(int key);
void AI_releasekey(int key);


char* AIself_HUD_name (int which);
float AIself_HUD_score (int which);
int AIself_HUD_time (int which);


int AIship_x (int which); 
int AIship_y (int which);
int AIship_heading (int which);
int AIship_vel (int which);
int AIship_acc (int which);
int AIship_track (int which);
int AIship_dist (int which);
int AIship_id (int which);
int AIship_xdir (int which);
int AIship_shield (int which);
int AIship_life (int which);
int AIship_team (int which);
int AIship_reload (int which);
char* AIship_name (int which);
int AIship_aimdir (int which);

int AIshot_x (int which);
int AIshot_y (int which);
int AIshot_dist (int which);
int AIshot_xdir (int which);
int AIshot_vel (int which);
int AIshot_track (int which);
int AIshot_imaginary (int which);	
int AIshot_idir (int which);
int AIshot_idist (int which);
int AIshot_itime (int which);
int AIshot_alert (int which);
int AIshot_id (int which);

int AIradar_x (int which);
int AIradar_y (int which);
int AIradar_dist (int which);
int AIradar_xdir (int which);
int AIradar_enemy (int which);

int AI_wallbetween (int x1, int y1, int x2, int y2);
int AI_wallbetween_x (int x1, int y1, int x2, int y2);
int AI_wallbetween_y (int x1, int y1, int x2, int y2);

unsigned int AImap_get (int mapx, int mapy);
void AImap_set (int mapx, int mapy, unsigned int value);
int tomap (int n);
int frmap (int mapn);

int anglediff (int angle1, int angle2);
int angleadd (int angle1, int angle2);

float rad (int deg);
int deg (float rad);

void AI_setmaxturn (int maxturn);

void AI_setcallback(void (*func)(void));



/*MAP tile definitions*/
#ifndef SETUP_H

#define SETUP_SPACE		0
#define SETUP_FILLED		1
#define SETUP_FILLED_NO_DRAW	2
#define SETUP_FUEL		3
#define SETUP_REC_RU		4
#define SETUP_REC_RD		5
#define SETUP_REC_LU		6
#define SETUP_REC_LD		7
#define SETUP_ACWISE_GRAV	8
#define SETUP_CWISE_GRAV	9
#define SETUP_POS_GRAV		10
#define SETUP_NEG_GRAV		11
#define SETUP_WORM_NORMAL	12
#define SETUP_WORM_IN		13
#define SETUP_WORM_OUT		14
#define SETUP_CANNON_UP		15
#define SETUP_CANNON_RIGHT	16
#define SETUP_CANNON_DOWN	17
#define SETUP_CANNON_LEFT	18
#define SETUP_SPACE_DOT		19
#define SETUP_TREASURE		20	/* + team number (10) */
#define SETUP_BASE_LOWEST	30	/* lowest base number */
#define SETUP_BASE_UP		30	/* + team number (10) */
#define SETUP_BASE_RIGHT	40	/* + team number (10) */
#define SETUP_BASE_DOWN		50	/* + team number (10) */
#define SETUP_BASE_LEFT		60	/* + team number (10) */
#define SETUP_BASE_HIGHEST	69	/* highest base number */
#define SETUP_TARGET		70	/* + team number (10) */
#define SETUP_CHECK		80	/* + check point number (26) */
#define SETUP_ITEM_CONCENTRATOR	110
#define SETUP_DECOR_FILLED	111
#define SETUP_DECOR_RU		112
#define SETUP_DECOR_RD		113
#define SETUP_DECOR_LU		114
#define SETUP_DECOR_LD		115
#define SETUP_DECOR_DOT_FILLED	116
#define SETUP_DECOR_DOT_RU	117
#define SETUP_DECOR_DOT_RD	118
#define SETUP_DECOR_DOT_LU	119
#define SETUP_DECOR_DOT_LD	120
#define SETUP_UP_GRAV		121
#define SETUP_DOWN_GRAV		122
#define SETUP_RIGHT_GRAV	123
#define SETUP_LEFT_GRAV		124
#define SETUP_ASTEROID_CONCENTRATOR	125

#define BLUE_UP			0x01
#define BLUE_RIGHT		0x02
#define BLUE_DOWN		0x04
#define BLUE_LEFT		0x08
#define BLUE_OPEN		0x10	/* diagonal botleft -> rightup */
#define BLUE_CLOSED		0x20	/* diagonal topleft -> rightdown */
#define BLUE_FUEL		0x30	/* when filled block is fuelstation */
#define BLUE_BELOW		0x40	/* when triangle is below diagonal */
#define BLUE_BIT		0x80	/* set when drawn with blue lines */

#define DECOR_LEFT		0x01
#define DECOR_RIGHT		0x02
#define DECOR_DOWN		0x04
#define DECOR_UP		0x08
#define DECOR_OPEN		0x10
#define DECOR_CLOSED		0x20
#define DECOR_BELOW		0x40
#endif

