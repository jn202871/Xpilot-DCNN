/* AI.h AI interface for xpilot */
#include "draw.h"

#define AISHIP_MAX 		128	/*limit of onscreen ships */
#define AIMAPSHIP_MAX		512	/*limit of radar ships */
#define AISHIP_MEMORY		2
#define AISHOT_MAX		100	/*max number of shots */
#define AIMAX_TURNSPEED		180	/*max turn degrees per frame */

#define AIMAP_MAXSIZE		900	/*900x900 squares */
#define AIMAP_PPB		35	/*pixels per block in map */
#define AIHUD_MAX 		10
#define AIHUD_NOSCORE		-99999

/*Map block types*/
#define AIMAP_SELF		0x0100
#define AIMAP_FRIEND		0x0200
#define AIMAP_ENEMY		0x0400
#define AIMAP_UNSEEN		0x8000	/*unseen parts of map */

/* This timer counts from -5 to 2. Why not count down from 7 to 0? -DAA */
int AI_delaystart;
float AI_turnspeed;
int AI_shotspeed;
int AI_repeatrate;
int AI_alerttimemult;		/*alert time multiplier */

/* Max length of a message */
#define AI_MSGLEN   256
/* Size of (incoming) message buffer - default maxMessage is 8 */
#define AI_MSGMAX   16

struct AI_msg_struct {
    char body[AI_MSGLEN];
    char from[32];
    char to[32];
} AI_msg[AI_MSGMAX];
void	AI_getmsg(char *msg);

struct AIself_HUD_struct {
    char name[32];
    float score;
    int time;
} AIself_HUD[AIHUD_MAX], AIself_HUD_prev[AIHUD_MAX];
int AIself_HUD_items;

int AI_max_turnspeed;
int AItimer;
int AIteamplay;			/*1 if teamplay and 0 if not */

/*FRAME by FRAME info*/
/*self*/

/*self ship*/
struct AIself_struct {
    int id;
    int alive;
    int x;
    int y;
    int heading;
    int vel;
    int veldir;
    int team;
    int life;
    int shield;
    int reload;
    int thrust;
    int thrust_old;
    int shoot;
    int shoot_old;
    int shield_enable;
    int turn;
    char *name;
    float score;
} AIself;

/*other ships on screen*/
struct AIship_struct {
    int x[AISHIP_MEMORY];
    int y[AISHIP_MEMORY];
    int heading[AISHIP_MEMORY];	/*direction ship is pointing */
    int vel[AISHIP_MEMORY], acc[AISHIP_MEMORY];
    int veldir[AISHIP_MEMORY];	/*direction of velocity */
    int dist[AISHIP_MEMORY];	/*distance from self to ship */
    int id;			/*id of other ship */
    int xdir;			/*direction from self to ship */
    int shield;			/*0 or 1 */
    int life;			/*number of lives */
    int team;			/*team number */
    int reload;			/*time to reload */
    char *name;			/*pointer to name string */
    struct shipobj *shape;
} AIship[AISHIP_MAX];

/*array of pointers to other ships, from closest to farthest away from self*/
int AIship_pointer[AISHIP_MAX];
/*buffer of above*/
int AIship_pointer_buffer[AISHIP_MAX];

struct AIshot_struct {
    int x;
    int y;
    int dist;
    int xdir;
    int vel;
    int veldir;
    int imaginary;		/* 1 if just a predicted shot and 0 if a real shot */
    int fresh_shot;		/* -1 if not, and index pointer of ship who shot if */
    int idir;			/* direction from you shot will intercept nearest */
    int idist;			/* intercept distance */
    int itime;			/* time to intercept */
    int alert;			/*MIN(yatx + timex, xaty + timey) */
    int id;			/*bullet id */
} AIshot[AISHOT_MAX];
struct AIshot_struct AIshot_buffer[AISHOT_MAX];

struct AIshot_image_struct {
    int x;
    int y;
} AIshot_image[3][AISHOT_MAX];

int AIshot_toggle;
int AIshot_previoustoggle;
int AIshot_shipping;

/*AImap_ship array is ordered from least to greatest distance*/
struct AImap_ship_struct {
    int xi;
    int yi;
    int distance;
    int xdir;
    int enemy;
} AImap_ship[AIMAPSHIP_MAX];

struct AImap_ship_struct AImap_ship_buffer[AISHIP_MAX];
int AImap_selfx, AImap_selfy;
int AImap_width, AImap_height;
unsigned int AImap[AIMAP_MAXSIZE][AIMAP_MAXSIZE];

struct AImap_xy {
    int x;
    int y;
};

/*BEGIN FUNCTIONS*/


void AIinit(void);		/*runs when first joining server */

void AIdoAction(void);		/*main loop, runs every frame */

void AIcontrol_turn(int degrees);	/*sends packet to turn ship x degrees */

void AIpressKey(int);		/*sends a packet of the particular key press */
void AIreleaseKey(int);		/*sends packet of the key release */

 /*SELF*/ int AIstore[32];
void AI_putstore(int d);

void AIself_HUD_erase(void);
void AIself_HUD_update(void);
int AIself_HUD_avail(void);

void AItalk(char *msg);

/*handles info about your self, called every frame, stores info in AIself struct*/
void AIself_handle(int x, int y, int dir, int vx, int vy);

/*returns the direction that position x, y is from self*/
int AIself_dirto(int x, int y);

void AIself_handlescore(float score);

void AI_self_destruct(void);

 /*SHIPS*/
/*these functions get info about the other ships on screen and stores that info in the AIship array, as AIship_struct's.  This info is saved in the array until the player leaves the game, each player having their own unique ship index id.  When the player leaves the visible screen, most values will be set to -1, such as x and y position, however, you could possibly store values such as a 'dangerous' level that goes up when a particular ship kills you often, that would be saved for the same ship throughout the entire game.  There is an array called AIship_pointer that saves the ship index the ships on screen in order of their distance from self, so to access the 'x' position of the ship nearest to self, you would use AIship[AIship_pointer[0]].x*/
void AIship_resetArray(void);

void AIship_handle(int id, int x, int y, int dir, int shield);
void AIship_newXYdir(int si, int x, int y, int dir);
int AIship_calcVel(int newX, int newY, int oldX, int oldY);
int AIship_calcVelDir(int newX, int newY, int oldX, int oldY, int vel);
int AIship_calcAcc(int oldVel, int newVel);
int AIship_calcxdir(int si);	/* direction from self */


/*right now you have to call calcfxdir manually because it doesn't work very well.  It only works about 1/3 of the time do to the asin and acos, which both return values that aren't necessarily in the correct quadrant.  This I hope will be improved*/

int AIship_calcfxdir(int si);	/* direction to shoot to hit ship, assuming no acceleration */


void AIship_pointer_erase(void);
void AIship_pointer_insert(int si);
void AIship_pointer_refresh(void);
int AIship_pointer_sort(void);

int AIship_find(int id);

void AIship_erase(int si);

/*Shots - enemy shots*/
/*for every shot on screen there is calculated: time until collision with x-axis, distance from self at that point, and direction (either 180 or 0), and time until collision with y-axis, distance from self at that point, and direction (either 90 or 270).  This info is stored as two seperate bullets, since it is equally important to dodge both collisions as if they were each their own bullet.  It would be nicer to just have it calculate the direction that the bullet will be closest to self, anywhere from 0 to 360 degrees, but thus far I have been unable to make such a calculation.*/

void AIshot_reset(void);
void AIshot_buffer_reset(void);
void AIshot_image_reset(int index);

void AIshot_addshot(int px, int py);
void AIshot_addships(void);
void AIshot_addtobuffer(int x, int y, float vel, float veldir,
			int imaginary, int fresh_shot);
void AIshot_refresh(void);
void AIshot_shipping_refresh(void);
int AIshot_buffer_sort(void);

float AIshot_calcVel(int newX, int newY, int oldX, int oldY);
float AIshot_calcVelDir(int newX, int newY, int oldX, int oldY, float vel);

int AIshot_calcxdir(int si);

void AIshot_calcIntercept(int shotindex);

 /*MAP*/
/*the map array is made up of blocks which eachrepresent a 35*35 block on the screen.  This is the size of one of those blue wall blocks.  As the ship flies around it gathers the map data and saves it in the array.  It uses the radar to get other ship's locations into the array.  Each type of wall, whether a square wall or empty or a triangle wall, or a home base or a fuel block, is stored in the array.  */
void AImap_init(void);

void AImap_getship(int i, int x, int y);

int AImap_calcdistance(int xi, int yi);
int AImap_calcxdir(int xi, int yi, int distance);

void AImap_ship_insert(int xi, int yi, int enemy);
void AImap_ship_reset(void);
void AImap_ship_buffer_reset(void);
void AImap_ship_refresh(void);
int AImap_ship_buffer_sort(void);


struct AImap_xy AImap_wallbetween(int x1, int y1, int x2, int y2);

int AIintersect_atX(int L1x1, int L1y1, int L1x2, int L1y2, int L2x1,
		    int L2y1, int L2x2, int L2y2);

int AIintersect_atY(int L1x1, int L1y1, int L1x2, int L1y2, int L2x1,
		    int L2y1, int L2x2, int L2y2);

int AI_distance(int x1, int y1, int x2, int y2);

float AI_radian(float degree);	/*converts degree to radian */
float AI_degree(float radian);	/*converts radian to degree */

int xpilot_setargv(int argc, char **argv);
int xpilot_launch();
