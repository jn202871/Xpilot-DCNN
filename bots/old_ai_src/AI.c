/*AI.c client AI interface for Xpilot*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifndef _WINDOWS
# include <X11/Xlib.h>
# include <X11/Xos.h>
# include <X11/Xutil.h>
# include <X11/keysym.h>
# include <X11/Xatom.h>
# include <X11/Xmd.h>
# ifdef	__apollo
#  include <X11/ap_keysym.h>
# endif
#endif

#ifdef _WINDOWS
# include "NT/winX.h"
# include "NT/winAudio.h"
# include "NT/winClient.h"
# include "NT/winXKey.h"
#endif

#include "config.h"
#include "const.h"
#include "paint.h"
#include "keys.h"
#include "netclient.h"
#include "paintdata.h"
#include "xevent.h"

#include "AI.h"
#include "xpilot_ai.h"

keys_t AIkey = KEY_DUMMY;

int AItimer = -14;

/* Since we can't send talk messages continuously, we'll keep
   them in a ring buffer -- DAA */

/* Size of (outgoing) message buffer */
#define AI_BUFLEN   32

char	AI_talkbuf[AI_BUFLEN][AI_MSGLEN];
int	AI_talkbuf_beg;
int	AI_talkbuf_end;
int	AI_talkbuf_siz;
/* Timer to avoid being kicked for flooding */
int	AI_floodguard;
int	AI_max_turnspeed;

void	AI_msg_enQ(char *msg);
char *	AI_msg_deQ(void);

/* redefine AImain to do ai, and use callback for threads */
/* We should be able to remove all of this and just leave one
   function prototype for the callback - DAA*/
extern void AImain(void);
extern void callback(void);

void (*AImain_callback) (void) = NULL;

void AI_setcallback(void (*func) ())
{
    AImain_callback = func;
    return;
}


void AIinit(void)
{
    AIteamplay = 0;
    AI_delaystart = -5;
    AIship_resetArray();
    AImap_init();
    AImap_ship_buffer_reset();
    AImap_ship_reset();
    AIshot_buffer_reset();
    AIshot_reset();
    /* What's going on here? -DAA */
    AIshot_image_reset(0);
    AIshot_image_reset(1);
    AIshot_image_reset(2);

    AIself_HUD_erase();
    AIshot_toggle = 1;
    AI_shotspeed = -1;
    AI_repeatrate = -1;
    AI_max_turnspeed = AIMAX_TURNSPEED;
    AIself.reload = 0;
    AIself.thrust = 0;
    AIself.shoot = 0;
    AIself.shield_enable = 1;
    AI_alerttimemult = 5;
    AIself_HUD_items = 0;
    
    AI_talkbuf_beg = 0;
    AI_talkbuf_end = 0;
    AI_talkbuf_siz = 0;
    AI_floodguard  = 0;

    AI_turnspeed = 0.0;
    return;
}


void AIdoAction(void)
{
    int i;

    AIself_HUD_update();

    if (AI_turnspeed == 0.0) {
	turnspeed = 64.0;
	power = 55.0;
	Send_turnspeed(turnspeed);
	Send_power(power);
	Send_turnresistance(0.0);
	AI_turnspeed = 64.0;
    }

    for (i = 0; i < AISHIP_MAX; i++) {
	if (AIship[i].id != -1 && AIship[i].reload > 0)
	    AIship[i].reload--;
    }

    if (AIshot_toggle > 0)
	AIshot_shipping_refresh();

    AIself.thrust_old = AIself.thrust;
    AIself.shoot_old = AIself.shoot;

    AIself.thrust = 0;
    AIself.turn = 0;
    AIself.shoot = 0;

    if (AI_delaystart > 2) {
	AImain();
	if (AImain_callback)
	    AImain_callback();
    }
    else {
	if (AI_delaystart == -5) {
	    AItalk("/get shotspeed");
	    AItalk("/get firerepeatrate");
	}
	/* Is there a more reliable way to get this information? -- DAA */
	else if (AI_delaystart < 2) {
	     sscanf(AI_msg[0].body, "The value of shotspeed is %d", &AI_shotspeed);
	     sscanf(AI_msg[0].body, "The value of firerepeatrate is %d", &AI_repeatrate);
	}

	if ((AI_shotspeed != -1 && AI_repeatrate != -1) || AI_delaystart < 1)
	    AI_delaystart++;
    }

    AIcontrol_turn(AIself.turn);


/*BELOW IS NOT BOT CODE*/



    if ((!AIself.shoot && AIself.shoot_old) || AIself.alive == 0)
	AIreleaseKey(KEY_FIRE_SHOT);
    else if (AIself.shoot) {
	if (AIself.reload == 0)
	    AIself.reload = AI_repeatrate;
	AIpressKey(KEY_FIRE_SHOT);
    }

    if (--AI_floodguard == 0)
	AItalk(NULL);

    /* Reload resets on death */
    AIself.reload = AIself.alive ? AIself.reload - 1 : 0;

    if (AIself.thrust == 0 && AIself.thrust_old == 1)
	AIreleaseKey(KEY_THRUST);
    else if (AIself.thrust == 1)
	AIpressKey(KEY_THRUST);


    if (AIself.shield_enable == 1 && AIself.shield != 1)
	AIpressKey(KEY_SHIELD);
    else if (AIself.shield_enable == 0 && AIself.shield == 1)
	AIreleaseKey(KEY_SHIELD);


    AItimer++;
    AIself.alive = 0;		/*assume death, and the paint function will reset to 1 if still alive */

    for (i = 0; i < AI_MSGMAX; i++ ) {
	 AI_msg[i].body[0] = '\0';
	 AI_msg[i].from[0] = '\0';
	 AI_msg[i].to[0] = '\0';
    }

    AIself_HUD_erase();
    callback();
    return;
}

void AIcontrol_turn(int deg)
{
     deg = deg<0 ? MAX(deg, -AI_max_turnspeed) : MIN(deg, AI_max_turnspeed);
     if (deg)
	  Send_pointer_move(deg * -128 / 360);
}

void AIpressKey(int key)
{
    AIkey = key;
    Key_press(AIkey);
    Net_key_change();
    AIkey = KEY_DUMMY;
    return;
}

void AIreleaseKey(int key)
{
    AIkey = key;
    Key_release(AIkey);
    Net_key_change();
    AIkey = KEY_DUMMY;
    return;
}

void AI_putstore(int d)
{
    int i;
    if (d == -1) {
	for (i = 0; i < 32 && AIstore[i] != -1; i++) {
	    printf("%d\n", AIstore[i]);
	    AIstore[i] = -1;
	}
	return;
    }
    else {
	for (i = 0; i < 32 && AIstore[i] != -1 && AIstore[i] != d; i++);
	if (AIstore[i] == d || i == 32)
	    return;
	else
	    AIstore[i] = d;
    }
    return;
}


void AIself_HUD_erase(void)
{
    int i = 0;
    while (i < AIHUD_MAX) {
	AIself_HUD_prev[i].score = AIself_HUD[i].score;
	AIself_HUD_prev[i].time = AIself_HUD[i].time;
	if (AIself_HUD[i].score != AIHUD_NOSCORE);
	strcpy(AIself_HUD_prev[i].name, AIself_HUD[i].name);
	AIself_HUD[i].score = AIHUD_NOSCORE;
	AIself_HUD[i].time = -1;
	AIself_HUD[i].name[0] = 0;
	i++;
    }
    return;
}

void AIself_HUD_update(void)
{
    int i = 0, same = 1;

    int findsame(int slot) {
	int i = 0;
	while (i < AIHUD_MAX && AIself_HUD_prev[i].score != AIHUD_NOSCORE)
	    i++;
	i--;
	while (i >= 0) {
	    if (strcmp(AIself_HUD_prev[i].name, AIself_HUD[slot].name) == 0
		&& AIself_HUD_prev[i].score == AIself_HUD[slot].score)
		return i;
	    i--;
	}
	return -1;
    }

    while (i < AIHUD_MAX && AIself_HUD_prev[i].score != AIHUD_NOSCORE) {
	if (strcmp(AIself_HUD_prev[i].name, AIself_HUD[i].name) < 0
	    || AIself_HUD_prev[i].score != AIself_HUD[i].score) {
	    same = 0;
	    break;
	}
	i++;
    }
    if (same) {
	i = 0;
	while (i < AIHUD_MAX && AIself_HUD_prev[i].score != AIHUD_NOSCORE) {
	    AIself_HUD[i].time = AIself_HUD_prev[i].time + 1;
	    i++;
	}
    }
    else {
	i = AIself_HUD_avail() - 1;
	while (i >= 0) {
	    if (i < 0)
		break;
	    else {
		if (findsame(i) == -1)
		    AIself_HUD[i].time = 0;
		else
		    AIself_HUD[i].time =
			AIself_HUD_prev[findsame(i)].time + 1;
	    }
	    i--;
	}
    }
    return;
}


int AIself_HUD_avail(void)
{
    int i = 0;
    while (i < AIHUD_MAX && AIself_HUD[i].score != AIHUD_NOSCORE)
	i++;
    return i;
}

void AI_getmsg(char *msg)
{
    int i, next;
    char buf[128];

    strcpy(buf, msg);
    for (next = 0; next < AI_MSGMAX && *AI_msg[next].body; next++);

    if (buf[strlen(buf) - 1] == '.') {
	strcpy(AI_msg[next].body, buf);
    }
    else {
	buf[strlen(buf) - 1] = '\0';
	for (i = strlen(buf) - 1; i > 0 && buf[i] != '['; i--);
	if (i > 0) {
	    if (buf[i - 1] == ':' && buf[i - 2] == ']') {
		strcpy(AI_msg[next].to, &buf[i + 1]);
		buf[i] = '\0';

		for (i -= 2; i > 0 && buf[i] != '['; i--);
		strcpy(AI_msg[next].from, &buf[i + 1]);
	    }
	    else {
		strcpy(AI_msg[next].from, &buf[i + 1]);
	    }
	    buf[i - 1] = '\0';
	    strcpy(AI_msg[next].body, buf);
	}
    }
}

void AI_msg_enQ(char *msg)
{
     if (AI_talkbuf_siz < AI_BUFLEN) {
	  AI_talkbuf_end = (AI_talkbuf_end + 1) % AI_BUFLEN;
	  strncpy(AI_talkbuf[AI_talkbuf_end], msg, AI_MSGLEN);
	  AI_talkbuf_siz++;
     }
}

/* Return next message or NULL if empty */
char * AI_msg_deQ(void)
{
     if (AI_talkbuf_siz) {
	  AI_talkbuf_siz--;
	  return AI_talkbuf[AI_talkbuf_beg = (AI_talkbuf_beg + 1) % AI_BUFLEN];
     }
     else
	  return NULL;
}

void AItalk(char *msg)
{
     char *head;
     if (msg)
	  AI_msg_enQ(msg);
     if (!AI_floodguard && (head = AI_msg_deQ())) {
	  Net_talk(head);
	  AI_floodguard = 3;
     }
}


void AIself_handle(int x, int y, int dir, int vx, int vy)
{
    AIself.x = x;
    AIself.y = y;
    AIself.heading = dir;
    AIself.vel = AIship_calcVel(x, y, x + vx, y + vy);
    AIself.veldir = AIship_calcVelDir(x, y, x - vx, y - vy, AIself.vel);
    //printf("self:vel: %d, veldir, %d\n",AIself.vel, AIself.veldir);
    return;
}


/*direction self must turn to point at x, y*/
int AIself_dirto(int x, int y)
{
    float distance = sqrt(sqr(abs(x - AIself.x)) + sqr(abs(y - AIself.y)));
    if (y - AIself.y < 0) {
	return (int) (360.0 -
		      (360.0 / (2.0 * M_PI)) *
		      acos((float) ((float) (x - AIself.x) / distance)));
    }
    else {
	return (int) (360.0 / (2.0 * M_PI)) *
	    acos((float) ((float) (x - AIself.x) / distance));
    }
}

void AI_self_destruct(void)
{
    AIpressKey(KEY_SELF_DESTRUCT);
    AIreleaseKey(KEY_SELF_DESTRUCT);
    return;
}

void AIship_resetArray()
{
    int i = 0;

    while (i < AISHIP_MAX) {
	AIship_erase(i);
	AIship_pointer[i] = -1;
	AIship_pointer_buffer[i] = -1;
	i++;
    }

    return;
}

void AIship_handle(int id, int x, int y, int dir, int shield)
{
    int si = AIship_find(id);	/*ship index */

    AIship[si].id = id;
    AIship_newXYdir(si, x, y, dir);
    AIship[si].xdir = AIship_calcxdir(si);
    AIship[si].shield = shield;
    if (AIship[si].dist[0] != 0 || AIship[si].id != AIself.id) {
	AIship_pointer_insert(si);
    }
    else {
	AIself.shield = shield;
	AIself.id = id;
    }

    return;
}

void AIship_newXYdir(int si, int x, int y, int dir)
{
    int i = AISHIP_MEMORY - 1;
    while (i > 0) {
	AIship[si].x[i] = AIship[si].x[i - 1];
	AIship[si].y[i] = AIship[si].y[i - 1];
	AIship[si].vel[i] = AIship[si].vel[i - 1];
	AIship[si].veldir[i] = AIship[si].veldir[i - 1];
	AIship[si].acc[i] = AIship[si].acc[i - 1];
	//printf("id: %d, vel: %d, acc: %d\n",AIship[si].id,AIship[si].vel[i-1],AIship[si].acc[i-1]);
	AIship[si].heading[i] = AIship[si].heading[i - 1];
	AIship[si].dist[i] = AIship[si].dist[i - 1];
	i--;
    }
    AIship[si].x[0] = x;
    AIship[si].y[0] = y;
    AIship[si].dist[0] =
	sqrt(sqr(abs(x - AIself.x)) + sqr(abs(y - AIself.y)));
    AIship[si].vel[0] =
	AIship_calcVel(x, y, AIship[si].x[1], AIship[si].y[1]);
    AIship[si].veldir[0] =
	AIship_calcVelDir(x, y, AIship[si].x[1], AIship[si].y[1],
			  AIship[si].vel[0]);
    //printf("si: %d, vel: %d, veldir: %d\n", si, AIship[si].vel[0], AIship[si].veldir[0]);
    AIship[si].acc[0] =
	AIship_calcAcc(AIship[si].vel[0], AIship[si].vel[1]);
    AIship[si].heading[0] = dir;
    return;
}

int AIship_calcVel(int newX, int newY, int oldX, int oldY)
{
    if (oldX == -1 && oldY == -1)
	return -1;
    else
	return sqrt(sqr(abs(newX - oldX)) + sqr(abs(newY - oldY)));
}

int AIship_calcVelDir(int newX, int newY, int oldX, int oldY, int vel)
{
    if (oldX == -1)
	return -1;
    else if (vel > 0) {
	if (newY - oldY < 0) {
	    return (int) (360.0 -
			  (360.0 / (2.0 * M_PI)) *
			  acos((float)
			       ((float) (newX - oldX) / (float) vel)));
	}
	else {
	    return (int) (360.0 / (2.0 * M_PI)) *
		acos((float) ((float) (newX - oldX) / (float) vel));
	}
    }
    else
	return 0;
}

int AIship_calcAcc(int oldVel, int newVel)
{
    if (oldVel == -1)
	return 0;
    else
	return (newVel - oldVel);
}

int AIship_calcxdir(int si)
{
    if (AIship[si].y[0] - AIself.y < 0) {
	return (int) (360.0 -
		      (360.0 / (2.0 * M_PI)) *
		      acos((float)
			   ((float) (AIship[si].x[0] - AIself.x) /
			    (float) AIship[si].dist[0])));
    }
    else {
	return (int) (360.0 / (2.0 * M_PI)) *
	    acos((float)
		 ((float) (AIship[si].x[0] - AIself.x) /
		  (float) AIship[si].dist[0]));
    }
}

int AIship_calcfxdir(int si)
{
    float Bx, By, Bvel, Cx, Cy, Svx, Svy, Sx, Sy, forgo, tugo, mugo;
    float degs1, degs2, time1, time2, Bvx;

    Bx = (float) AIself.x;
    By = (float) AIself.y;

    Bvel = (float) AI_shotspeed;
    Cx = cos(AI_radian(AIself.veldir)) * AIself.vel;
    Cy = sin(AI_radian(AIself.veldir)) * AIself.vel;

    Svx = cos(AI_radian(AIship[si].veldir[0])) * AIship[si].vel[0];
    Svy = sin(AI_radian(AIship[si].veldir[0])) * AIship[si].vel[0];

    Sx = AIship[si].x[0];
    Sy = AIship[si].y[0];

    tugo =
	pow(pow(Bvel * Sx - Bvel * Bx, 2) + pow(Bvel * By - Bvel * Sy, 2),
	    0.5);

    mugo = AI_degree(acos((Bvel * Sx - Bvel * Bx) / tugo));

    forgo =
	AI_degree(asin
		  ((By * Svx - Bx * Svy + Bx * Cy - By * Cx + Sx * Svy -
		    Sy * Svx - Cy * Sx + Sy * Cx) / tugo));

    degs1 = fabs(forgo + mugo);

    degs2 = fabs(forgo - mugo);

    Bvx =
	cos(AI_radian(degs1)) * Bvel +
	cos(AI_radian(AIself.veldir)) * AIself.vel;
    time1 = (Bx - Sx) / (Svx - Bvx);
    //printf("time1: %f\n", time1);

    //printf("shipy: %f, selfy: %f\n",Sy + Svy * time1, (AIself.y + sin(AI_radian(AIself.veldir)) * AIself.vel * time1));

    Bvx =
	cos(AI_radian(degs2)) * Bvel +
	cos(AI_radian(AIself.veldir)) * AIself.vel;
    time2 = (Bx - Sx) / (Svx - Bvx);
    //printf("time2: %f\n", time2);

    //printf("shipy: %f, selfy: %f\n",Sy + Svy * time2, (AIself.y + sin(AI_radian(AIself.veldir)) * AIself.vel * time2));


    /*It's because those asin and acos that I must do all the below, because they return values that may or may not be in the correct quadrant.  Someone must figure out how to tell what quadrant they should be in */

    if (time1 < 0 && time2 < 0) {
	return -1.0;
    }
    else if (time1 < 0) {
	if ((Sy + Svy * time2) <=
	    (AIself.y +
	     sin(AI_radian(AIself.veldir)) * AIself.vel * time2)) {
	    //printf("(2)\ndeg1: %f\ndeg2: %f\n", degs1, 360.0 - degs2);
	    return 360.0 - degs2;
	}
	else {
	    //printf("(1)\ndeg1: %f\ndeg2: %f\n", degs1, 360.0 - degs2);
	    return -1.0;
	}
    }
    else if (time2 < 0) {
	if ((Sy + Svy * time1) >=
	    (AIself.y +
	     sin(AI_radian(AIself.veldir)) * AIself.vel * time1)) {
	    //printf("(2)\ndeg1: %f\ndeg2: %f\n", degs1, 360.0 - degs2);
	    return degs1;
	}
	else {
	    return -1.0;
	}
    }
    else {
	if ((Sy + Svy * time1) >=
	    (AIself.y +
	     sin(AI_radian(AIself.veldir)) * AIself.vel * time1)) {
	    //printf("(2)\ndeg1: %f\ndeg2: %f\n", degs1, 360.0 - degs2);
	    return degs1;
	}
	else if ((Sy + Svy * time2) <
		   (AIself.y +
		    sin(AI_radian(AIself.veldir)) * AIself.vel * time2)) {
	    //printf("(1)\ndeg1: %f\ndeg2: %f\n", degs1, 360.0 - degs2);
	    return 360.0 - degs2;
	}
	else {
	    return degs2;
	}
    }
    return -1;
}



void AIship_pointer_erase()
{
    int i = 0;
    while (i < AISHIP_MAX) {
	AIship_pointer[i] = -1;
	i++;
    }
    return;
}


void AIship_pointer_insert(int si)
{
    int i = 0;
    while (AIship_pointer_buffer[i] != -1)
	i++;
    AIship_pointer_buffer[i] = si;
    return;
}


void AIship_pointer_refresh(void)
{
    int i = 1;
    while (i > 0)
	i = AIship_pointer_sort();

    i = 0;
    AIship_pointer_erase();
    while (AIship_pointer_buffer[i] != -1) {
	AIship_pointer[i] = AIship_pointer_buffer[i];
	AIship_pointer_buffer[i] = -1;
	i++;
    }

    return;
}


int AIship_pointer_sort(void)
{
    int i = 0, swapped = 0;
    void swap(si1, si2) {
	int ssi;
	ssi = AIship_pointer_buffer[si2];
	AIship_pointer_buffer[si2] = AIship_pointer_buffer[si1];
	AIship_pointer_buffer[si1] = ssi;
	return;
    }
    while (AIship_pointer_buffer[i + 1] != -1) {
	if (AIship[AIship_pointer_buffer[i]].dist[0] >
	    AIship[AIship_pointer_buffer[i + 1]].dist[0]) {
	    swap(i, i + 1);
	    swapped++;
	}
	i++;
    }
    return swapped;
}




/*returns location of ship with id 'id' in AIship array. or adds it at first available*/
int AIship_find(int id)
{
    int i = 0;
    int firstavailable = -1;
    while (i < AISHIP_MAX) {
	if (AIship[i].id == id)
	    return i;
	else if (AIship[i].id == -1 && firstavailable == -1)
	    firstavailable = i;
	i++;
    }
    //printf("first: %d\n", firstavailable);
    return firstavailable;
}


void AIship_erase(int si)
{
    int i = 0;
    AIship[si].id = -1;
    AIship[si].xdir = -1;
    AIship[si].shield = -1;
    AIship[si].reload = -1;
    AIship[si].shape = 0;
    while (i < AISHIP_MEMORY) {
	AIship[si].x[i] = -1;
	AIship[si].y[i] = -1;
	AIship[si].dist[i] = -1;
	AIship[si].vel[i] = -1;
	AIship[si].acc[i] = -1;
	AIship[si].heading[i] = -1;
	AIship[si].veldir[i] = -1;
	i++;
    }
    return;
}



void AIshot_reset(void)
{
    int i = 0;
    while (i < AISHOT_MAX && AIshot[i].x != -1) {
	AIshot[i].x = -1;
	AIshot[i].y = -1;
	AIshot[i].dist = -1;
	AIshot[i].xdir = -1;
	AIshot[i].vel = -1;
	AIshot[i].veldir = -1;
	AIshot[i].idir = -1;
	AIshot[i].idist = -1;
	AIshot[i].itime = -1;
	AIshot[i].imaginary = -1;
	AIshot[i].fresh_shot = -1;
	AIshot[i].alert = -1;
	i++;
    }
    return;
}

void AIshot_buffer_reset(void)
{
    int i = 0;
    while (i < AISHOT_MAX && AIshot_buffer[i].x != -1) {
	AIshot_buffer[i].x = -1;
	AIshot_buffer[i].y = -1;
	AIshot_buffer[i].dist = -1;
	AIshot_buffer[i].xdir = -1;
	AIshot_buffer[i].vel = -1;
	AIshot_buffer[i].veldir = -1;
	AIshot_buffer[i].idir = -1;
	AIshot_buffer[i].idist = -1;
	AIshot_buffer[i].itime = -1;
	AIshot_buffer[i].imaginary = -1;
	AIshot_buffer[i].fresh_shot = -1;
	AIshot_buffer[i].alert = -1;
	i++;
    }
    return;
}

void AIshot_image_reset(int index)
{
    int i = index;
    while (i < AISHOT_MAX && AIshot_image[index][i].x != -1) {
	AIshot_image[index][i].x = -1;
	AIshot_image[index][i].y = -1;
	i++;
    }
    return;
}

/* this calculates the velocity and direction of each shot by comparing all possible velocites and directions for three images of shot locations: present, first past, second past.  If it can't find two matching velocites and directions in a row for a present shot, it will check to see if a ship was there two frames ago that could have shot it.  works farely well but occasionally there are some bad calculations where shots that don't really exist are added*/
void AIshot_addshot(int px, int py)
{
    int i1, i2;
    float tempvel1, tempdir1, tempvel2, tempdir2;
    int found = 0;
    int i = 0;

    if (AIshot_toggle == 0)
	AIshot_reset();

    while (AIshot_image[0][i].x != -1 && i < AISHOT_MAX)
	i++;

    AIshot_image[0][i].x = AIself.x - ext_view_width / 2 + WINSCALE(px);
    AIshot_image[0][i].y = AIself.y + ext_view_height / 2 - WINSCALE(py);

    i1 = 0;
    while (i1 < AISHOT_MAX && AIshot_image[1][i1].x != -1) {
	tempvel1 =
	    AIshot_calcVel(AIshot_image[0][i].x, AIshot_image[0][i].y,
			   AIshot_image[1][i1].x, AIshot_image[1][i1].y);
	tempdir1 =
	    AIshot_calcVelDir(AIshot_image[0][i].x, AIshot_image[0][i].y,
			      AIshot_image[1][i1].x, AIshot_image[1][i1].y,
			      tempvel1);
	i2 = 0;
	while (i2 < AISHOT_MAX && AIshot_image[2][i2].x != -1) {
	    tempvel2 =
		AIshot_calcVel(AIshot_image[1][i1].x,
			       AIshot_image[1][i1].y,
			       AIshot_image[2][i2].x,
			       AIshot_image[2][i2].y);
	    if (fabs(tempvel1 - tempvel2) < 6.0) {
		tempdir2 =
		    AIshot_calcVelDir(AIshot_image[1][i1].x,
				      AIshot_image[1][i1].y,
				      AIshot_image[2][i2].x,
				      AIshot_image[2][i2].y, tempvel2);
		if (fabs(tempdir1 - tempdir2) < 6.0) {
		    AIshot_addtobuffer(AIshot_image[0][i].x,
				       AIshot_image[0][i].y,
				       (tempvel1 + tempvel2) / 2.0,
				       (tempdir1 + tempdir2) / 2.0, 0, -1);
		    found = 1;
		    i2 = AISHOT_MAX;
		    i1 = AISHOT_MAX;
		}
	    }
	    i2++;
	}
	if (found == 0) {
	    i2 = 0;
	    while (i2 < AISHIP_MAX && AIship_pointer[i2] != -1) {
		tempvel2 =
		    AIshot_calcVel(AIshot_image[1][i1].x,
				   AIshot_image[1][i1].y,
				   AIship[AIship_pointer[i2]].x[2] +
				   (int) (18.0 *
					  cos(AI_radian
					      ((float)
					       AIship[AIship_pointer[i2]].
					       heading[2]))),
				   AIship[AIship_pointer[i2]].y[2] +
				   (int) (18.0 *
					  sin(AI_radian
					      ((float)
					       AIship[AIship_pointer[i2]].
					       heading[2]))));
		if (fabs(tempvel1 - tempvel2) < 17.0) {
		    tempdir2 =
			AIshot_calcVelDir(AIshot_image[1][i1].x,
					  AIshot_image[1][i1].y,
					  AIship[AIship_pointer[i2]].x[2] +
					  (int) (18.0 *
						 cos(AI_radian
						     ((float)
						      AIship[AIship_pointer
							     [i2]].
						      heading[2]))),
					  AIship[AIship_pointer[i2]].y[2] +
					  (int) (18.0 *
						 sin(AI_radian
						     ((float)
						      AIship[AIship_pointer
							     [i2]].
						      heading[2]))),
					  tempvel2);
		    if (fabs(tempdir1 - tempdir2) < 17.0) {
			//printf("--------FRESH SHOT\n");
			AIshot_addtobuffer(AIshot_image[0][i].x,
					   AIshot_image[0][i].y,
					   (tempvel1 + tempvel2) / 2.0,
					   (tempdir1 + tempdir2) / 2.0, 0,
					   AIship_pointer[i2]);
			AIship[AIship_pointer[i2]].reload =
			    AI_repeatrate - 1;
			//printf("tempvel:1: %d, 2: %d, dir:1: %d, 2: %d\n", (int)tempvel1, (int)tempvel2, (int)tempdir1, (int)tempdir2);
			found = 1;
			i2 = AISHIP_MAX;
			i1 = AISHOT_MAX;
		    }
		}
		i2++;
	    }
	}
	i1++;
    }

    AIshot_toggle++;
    return;
}

void AIshot_addships(void)
{
    float nosex, nosey, newxvel, newyvel, newvel, newveldir;
    int i = 0;

    while (AIship_pointer[i] != -1
	   && AIship[AIship_pointer[i]].vel[0] != -1) {
	nosex =
	    AIship[AIship_pointer[i]].x[0] +
	    (int) (15.0 *
		   cos(AI_radian
		       ((float) AIship[AIship_pointer[i]].heading[0])));
	nosey =
	    AIship[AIship_pointer[i]].y[0] +
	    (int) (15.0 *
		   sin(AI_radian
		       ((float) AIship[AIship_pointer[i]].heading[0])));

	newxvel =
	    cos(AI_radian((float) AIship[AIship_pointer[i]].veldir[0])) *
	    (float) AIship[AIship_pointer[i]].vel[0] +
	    cos(AI_radian((float) AIship[AIship_pointer[i]].heading[0])) *
	    (float) AI_shotspeed;

	newyvel =
	    sin((float) AIship[AIship_pointer[i]].veldir[0]) *
	    (float) AIship[AIship_pointer[i]].vel[0] +
	    sin((float) AIship[AIship_pointer[i]].heading[0]) *
	    (float) AI_shotspeed;

	newvel = sqrt(sqr(newxvel) + sqr(newyvel));

	if (newyvel < 0) {
	    newveldir =
		360.0 -
		(360.0 / (2.0 * M_PI)) * acos(newxvel /
					      (newvel + 0.000001));
	}
	else {
	    newveldir =
		(360.0 / (2.0 * M_PI)) * acos(newxvel /
					      (newvel + 0.000001));
	}

	AIshot_addtobuffer(nosex, nosey, newvel, newveldir, 1, -1);
	i++;
    }
    return;
}


void AIshot_addtobuffer(int x, int y, float vel, float veldir,
			int imaginary, int fresh_shot)
{
    float theta1, theta2;
    float A, B, C, BAC;
    int newx1, newx2, newy1, newy2;
    int i = 0;
    while (i < AISHOT_MAX && AIshot_buffer[i].x != -1)
	i++;

    AIshot_buffer[i].x = x;
    AIshot_buffer[i].y = y;
    AIshot_buffer[i].vel = (int) vel;
    AIshot_buffer[i].veldir = (int) veldir;
    AIshot_buffer[i].imaginary = imaginary;
    AIshot_buffer[i].fresh_shot = fresh_shot;

    theta1 = AI_radian((float) AIself.veldir);
    theta2 = AI_radian(veldir);

    A = pow(AIself.vel * sin(theta1) - vel * sin(theta2),
	    2) + pow(AIself.vel * cos(theta1) - vel * cos(theta2), 2);
    B = 2 * ((AIself.y - y) *
	     (AIself.vel * sin(theta1) - vel * sin(theta2)) + (AIself.x -
							       x) *
	     (AIself.vel * cos(theta1) - vel * cos(theta2)));
    C = pow(AIself.x - x, 2) + pow(AIself.y - y, 2);

    BAC = pow(B, 2) - 4 * A * C;

    if (BAC >= 0) {
	BAC = (-1 * B + pow(BAC, .5));
	if ((BAC / (2 * A)) < 0)
	    BAC = (-1 * B - pow(pow(B, 2) - 4 * A * C, .5));
	AIshot_buffer[i].itime = BAC / (2 * A);
	AIshot_buffer[i].idist = 777;
	AIshot_buffer[i].idir = 777;
    }
    else {
	AIshot_buffer[i].itime = (-1 * B) / (2 * A);
	AIshot_buffer[i].idist = C - pow(B, 2) / (4 * A);
	AIshot_buffer[i].idir = 777;
    }

    newx1 = AIself.x + AIself.vel * cos(theta1) * AIshot_buffer[i].itime;
    newx2 = x + vel * cos(theta2) * AIshot_buffer[i].itime;
    newy1 = AIself.y + AIself.vel * sin(theta1) * AIshot_buffer[i].itime;
    newy2 = y + vel * sin(theta2) * AIshot_buffer[i].itime;

    AIshot_buffer[i].idist = AI_distance(newx1, newy1, newx2, newy2);

    if ((newy2 - newy1) < 0) {
	AIshot_buffer[i].idir =
	    (int) (360.0 -
		   (360.0 / (2.0 * M_PI)) *
		   acos((float)
			((float) (newx2 - newx1) /
			 (float) AIshot_buffer[i].idist)));
    }
    else {
	AIshot_buffer[i].idir =
	    (int) (360.0 / (2.0 * M_PI)) *
	    acos((float)
		 ((float) (newx2 - newx1) /
		  (float) AIshot_buffer[i].idist));
    }

    AIshot_buffer[i].alert =
	abs(AIshot_buffer[i].idist +
	    (int) (AIshot_buffer[i].itime * AI_alerttimemult));


    if (AIshot_buffer[i].itime < 0 || AIshot_buffer[i].itime == 0) {
	AIshot_buffer[i].alert = 30000;
    }

    AIshot[i].id = i;
    return;
}

void AIshot_refresh(void)
{
    int i;
    if (AIshot_toggle > 0) {
	AIshot_addships();
	i = 1;
	while (i > 0)
	    i = AIshot_buffer_sort();

	AIshot_reset();
	i = 0;
	while (i < AISHOT_MAX && AIshot_buffer[i].x != -1) {
	    AIshot[i].x = AIshot_buffer[i].x;
	    AIshot[i].y = AIshot_buffer[i].y;
	    AIshot[i].dist =
		sqrt(sqr(abs(AIshot[i].x - AIself.x)) +
		     sqr(abs(AIshot[i].y - AIself.y)));
	    AIshot[i].xdir = AIshot_calcxdir(i);
	    AIshot[i].vel = AIshot_buffer[i].vel;
	    AIshot[i].veldir = AIshot_buffer[i].veldir;
	    AIshot[i].itime = AIshot_buffer[i].itime;
	    AIshot[i].imaginary = AIshot_buffer[i].imaginary;
	    AIshot[i].fresh_shot = AIshot_buffer[i].fresh_shot;
	    AIshot[i].idist = AIshot_buffer[i].idist;
	    AIshot[i].idir = AIshot_buffer[i].idir;

	    AIshot[i].alert = AIshot_buffer[i].alert;
	    i++;
	}

	AIshot_image_reset(2);
	i = 0;
	while (i < AISHOT_MAX && AIshot_image[1][i].x != -1) {
	    AIshot_image[2][i].x = AIshot_image[1][i].x;
	    AIshot_image[2][i].y = AIshot_image[1][i].y;
	    i++;
	}

	AIshot_image_reset(1);
	i = 0;
	while (i < AISHOT_MAX && AIshot_image[0][i].x != -1) {
	    AIshot_image[1][i].x = AIshot_image[0][i].x;
	    AIshot_image[1][i].y = AIshot_image[0][i].y;
	    i++;
	}

	AIshot_image_reset(0);

	AIshot_buffer_reset();
	//printf("\n*\n");
	//printf("setup:h: %d, w: %d\n",ext_view_height,ext_view_width);

	AIshot_toggle = 0;
    }

    return;
}

/*for when there are no bullets but only ships*/
void AIshot_shipping_refresh(void)
{
    int i;
    if (AIshot_toggle > 0) {
	AIshot_buffer_reset();
	AIshot_addships();
	i = 1;
	while (i > 0)
	    i = AIshot_buffer_sort();

	AIshot_reset();
	i = 0;
	while (i < AISHOT_MAX && AIshot_buffer[i].x != -1) {
	    AIshot[i].x = AIshot_buffer[i].x;
	    AIshot[i].y = AIshot_buffer[i].y;
	    AIshot[i].dist =
		sqrt(sqr(abs(AIshot[i].x - AIself.x)) +
		     sqr(abs(AIshot[i].y - AIself.y)));
	    AIshot[i].xdir = AIshot_calcxdir(i);
	    AIshot[i].vel = AIshot_buffer[i].vel;
	    AIshot[i].veldir = AIshot_buffer[i].veldir;
	    AIshot[i].itime = AIshot_buffer[i].itime;
	    AIshot[i].imaginary = AIshot_buffer[i].imaginary;
	    AIshot[i].fresh_shot = AIshot_buffer[i].fresh_shot;
	    AIshot[i].idist = AIshot_buffer[i].idist;
	    AIshot[i].idir = AIshot_buffer[i].idir;

	    AIshot[i].alert = AIshot_buffer[i].alert;
	    i++;
	}
    }

    return;
}

int AIshot_buffer_sort(void)
{
    int i = 0, swapped = 0;

    void swap(si1, si2) {
	struct AIshot_struct ssi;
	ssi = AIshot_buffer[si2];
	AIshot_buffer[si2] = AIshot_buffer[si1];
	AIshot_buffer[si1] = ssi;
	return;
    }
    while (AIshot_buffer[i + 1].x != -1) {
	if (AIshot_buffer[i].alert > AIshot_buffer[i + 1].alert) {
	    swap(i, i + 1);
	    swapped++;
	}
	i++;
    }
    return swapped;
}


float AIshot_calcVel(int newX, int newY, int oldX, int oldY)
{
    if (oldX == -1 && oldY == -1)
	return -1.0;
    else
	return sqrt(sqr(fabs((float) newX - (float) oldX)) +
		    sqr(fabs((float) newY - (float) oldY)));
}

float AIshot_calcVelDir(int newX, int newY, int oldX, int oldY, float vel)
{
    if (oldX == -1)
	return -1.0;
    else if (vel > 0.0) {
	if (newY - oldY < 0) {
	    return (360.0 -
		    (360.0 / (2.0 * M_PI)) *
		    acos((float) ((float) (newX - oldX) / vel)));
	}
	else {
	    return (360.0 / (2.0 * M_PI)) *
		acos((float) ((float) (newX - oldX) / vel));
	}
    }
    else
	return 0.0;
}

int AIshot_calcxdir(int si)
{
    if (AIshot[si].y - AIself.y < 0) {
	return (int) (360.0 -
		      (360.0 / (2.0 * M_PI)) *
		      acos((float)
			   ((float) (AIshot[si].x - AIself.x) /
			    (float) AIshot[si].dist)));
    }
    else {
	return (int) (360.0 / (2.0 * M_PI)) *
	    acos((float)
		 ((float) (AIshot[si].x - AIself.x) /
		  (float) AIshot[si].dist));
    }
}

void AIshot_calcIntercept(int si)
{
    float time1, time2, time;
    float self_xvel, self_yvel, shot_xvel, shot_yvel;
    float a, b, c, d;
    int distance;
    int xdir;

    self_xvel =
	cos(AI_radian((float) AIself.veldir)) * (float) AIself.vel +
	0.00001;
    self_yvel =
	sin(AI_radian((float) AIself.veldir)) * (float) AIself.vel +
	0.00001;
    shot_xvel =
	cos(AI_radian((float) AIshot_buffer[si].veldir)) *
	(float) AIshot_buffer[si].vel + 0.00001;
    shot_yvel =
	sin(AI_radian((float) AIshot_buffer[si].veldir)) *
	(float) AIshot_buffer[si].vel + 0.00001;

    a = self_yvel * (float) (AIself.y - AIshot_buffer[si].y);
    b = sqr(self_yvel) - self_yvel * shot_yvel;
    c = self_xvel * (float) (AIself.x - AIshot_buffer[si].x);
    d = sqr(self_xvel) - self_xvel * shot_xvel;

    time1 = (a - c) / (d - b);
    time2 = -1.0 * (a + c) / (b + d);

    if (time1 < 0 && time2 < 0)
	time = 999999;
    else
	time = MAX(time1, time2);

    //time = time2;

    distance =
	(int)
	sqrt(sqr
	     (fabs
	      (((float) AIshot_buffer[si].x + shot_xvel * (float) time) -
	       ((float) AIself.x + self_xvel * (float) time))) +
	     sqr(fabs
		 (((float) AIshot_buffer[si].y +
		   shot_yvel * (float) time) - ((float) AIself.y +
						self_yvel *
						(float) time))));

    xdir =
	(int) AIshot_calcVelDir((AIshot_buffer[si].x + shot_xvel * time),
				(AIshot_buffer[si].y + shot_yvel * time),
				(AIself.x + self_xvel * time),
				(AIself.y + self_yvel * time), distance);


    printf("self:x: %d, y: %d, xvel: %d, yvel: %d\n", AIself.x, AIself.y,
	   (int) self_xvel, (int) self_yvel);
    printf("shot:x: %d, y: %d, xvel: %d, yvel: %d\n", AIshot_buffer[si].x,
	   AIshot_buffer[si].y, (int) shot_xvel, (int) shot_yvel);
    printf("     veldir: %d, vel: %d\n", AIshot_buffer[si].veldir,
	   AIshot_buffer[si].vel);
    printf("time = %3.3f\n", time);
    printf("dist = %d\n", distance);
    printf("xdir = %d\n\n", xdir);

    return;
}



void AImap_init(void)
{
    int i = 0, j = 0;
    while (i < AIMAP_MAXSIZE) {
	j = 0;
	while (j < AIMAP_MAXSIZE) {
	    AImap[i][j] = AImap[i][j] | AIMAP_UNSEEN;
	    j++;
	}
	i++;
    }
    return;
}


void AImap_getship(int i, int x, int y)
{
    int xw, yw;
    int s = radar_ptr[i].size;

    xw = radar_ptr[i].x * AImap_width / 256;
    yw = radar_ptr[i].y * AImap_height / 256;

    if (i == 0) {
	//printf("S: x: %d %d, y: %d %d, alive: %d\n",x,AImap_selfx,y,AImap_selfy,AIself.alive);
	AImap_selfx = x;
	AImap_selfy = y;
	//AImap[xw][yw] = AImap[xw][yw] ^ AIMAP_SELF;
    }
    else if ((s & 0x80) == 0) {
	//AImap[xw][yw] = AImap[xw][yw] ^ AIMAP_ENEMY;
	AImap_ship_insert(xw, yw, 1);
    }
    else if ((s & 0x80) != 0) {
	//AImap[xw][yw] = AImap[xw][yw] ^ AIMAP_FRIEND;
	AImap_ship_insert(xw, yw, 0);
    }

    return;
}

int AImap_calcdistance(int xi, int yi)
{
    int x = xi * AIMAP_PPB + AIMAP_PPB / 2;
    int y = yi * AIMAP_PPB + AIMAP_PPB / 2;
    int tempo = sqr(abs(AIself.x - x)) + sqr(abs(AIself.y - y));
    return (int) sqrt(tempo);
}

int AImap_calcxdir(int xi, int yi, int distance)
{
    int x = xi * AIMAP_PPB + AIMAP_PPB / 2;
    int y = yi * AIMAP_PPB + AIMAP_PPB / 2;

    if (y - AIself.y < 0) {
	return (int) (360.0 -
		      (360.0 / (2.0 * M_PI)) *
		      acos((float)
			   ((float) (x - AIself.x) / (float) distance)));
    }
    else {
	return (int) (360.0 / (2.0 * M_PI)) *
	    acos((float) ((float) (x - AIself.x) / (float) distance));
    }
}


void AImap_ship_insert(int xi, int yi, int enemy)
{
    int i = 0;
    while (AImap_ship_buffer[i].distance != -1)
	i++;

    AImap_ship_buffer[i].xi = xi;
    AImap_ship_buffer[i].yi = yi;
    AImap_ship_buffer[i].enemy = enemy;
    AImap_ship_buffer[i].distance = AImap_calcdistance(xi, yi);
    AImap_ship_buffer[i].xdir =
	AImap_calcxdir(xi, yi, AImap_ship_buffer[i].distance);

    return;
}


void AImap_ship_reset(void)
{
    int i = 0;
    while (i < AISHIP_MAX && AImap_ship[i].xi != -1) {
	AImap_ship[i].xi = -1;
	AImap_ship[i].yi = -1;
	AImap_ship[i].distance = -1;
	AImap_ship[i].xdir = -1;
	AImap_ship[i].enemy = -1;
	i++;
    }
    return;
}

void AImap_ship_buffer_reset(void)
{
    int i = 0;
    while (i < AISHIP_MAX && AImap_ship_buffer[i].xi != -1) {
	AImap_ship_buffer[i].xi = -1;
	AImap_ship_buffer[i].yi = -1;
	AImap_ship_buffer[i].distance = -1;
	AImap_ship_buffer[i].xdir = -1;
	AImap_ship_buffer[i].enemy = -1;
	i++;
    }
    return;
}


void AImap_ship_refresh(void)
{
    int i = 1;
    while (i > 0)
	i = AImap_ship_buffer_sort();

    i = 0;
    AImap_ship_reset();
    while (AImap_ship_buffer[i].distance != -1) {
	AImap_ship[i] = AImap_ship_buffer[i];
	i++;
    }
    AImap_ship_buffer_reset();
    return;
}

int AImap_ship_buffer_sort(void)
{
    int i = 0, swapped = 0;
    void swap(si1, si2) {
	struct AImap_ship_struct ssi;
	ssi = AImap_ship_buffer[si2];
	AImap_ship_buffer[si2] = AImap_ship_buffer[si1];
	AImap_ship_buffer[si1] = ssi;
	return;
    }
    while (AImap_ship_buffer[i + 1].distance != -1) {
	if (AImap_ship_buffer[i].distance >
	    AImap_ship_buffer[i + 1].distance) {
	    swap(i, i + 1);
	    swapped++;
	}
	i++;
    }
    return swapped;
}



/*if values of x02,y02 are out of the map the point on the border of the map where the line from x1,y1 to x02,y02 intersects will be used*/

struct AImap_xy AImap_wallbetween(int x1, int y1, int x02, int y02)
{
    int wallxi_min, wallxi_max, wallyi_min, wallyi_max;
    int wallxi, wallyi;
    int x, y;
    int x2, y2;
    struct AImap_xy ret;

    int closestx, closesty;

    int x_min, x_max, y_min, y_max;

    int go_up;			/* go up or down, starting at wherever first coordinate Y is */
    int go_right;		/* go right instead of to the left */

    /*conditional for the y while loop */
    int oky(void) {
	if (go_up) {
	    if (wallyi <= wallyi_max && wallyi < AIMAP_MAXSIZE)
		return 1;
	    else
		return 0;
	}
	else {
	    if (wallyi >= wallyi_min && wallyi >= 0)
		return 1;
	    else
		return 0;
	}
    }

    /*conditional for x while loop */
    int okx(void) {
	if (go_right) {
	    if (wallxi <= wallxi_max && wallxi < AIMAP_MAXSIZE)
		return 1;
	    else
		return 0;
	}
	else {
	    if (wallxi >= wallxi_min && wallxi >= 0)
		return 1;
	    else
		return 0;
	}
    }
    x2 = x02;
    y2 = y02;
    closestx = -1;
    closesty = -1;
    ret.x = 0;
    ret.y = 0;
    //printf("Bef:x2: %d, y2: %d\n",x2,y2);

    /*if x2,y2 is off the map then figure out where the line between x1,y1 and x2,y2 intersects with the border of map */
    /*if (x2 > AImap_width * 35 || x2 < 0 || y2 > AImap_height * 35 || y2 < 0) {
       distance = sqrt(sqr(abs(x2 - x1)) + sqr(abs(y2 - y1)));
       //get angle between x1,y1 and x2,y2
       if (y2 - y1 < 0) {
       angle = (int)(360.0 - (360.0/(2.0 * M_PI))*acos((float)((float)(x2 - x1)/(float)distance)));
       }
       else {
       angle = (int)(360.0/(2.0 * M_PI))*acos((float)((float)(x2 - x1)/(float)distance));
       }

       slope = (float)(y2 - y1) / ((float)(x2 - x1) + 0.00001);

       //printf("x1: %d, y1: %d\n",x1,y1);
       //printf("dist: %d, angle: %d, cos:%f, sin:%f, slope: %f\n", distance, angle, cos(AI_radian(angle)), sin(AI_radian(angle)), slope);
       if (cos(AI_radian((float)angle)) >=0 && sin(AI_radian((float)angle)) >= 0) {
       y2 = (int)(slope * (float)(AImap_width * 35 - x1) + y1);
       //x2 = AImap_width * 35;
       x2 = (int)((float)(y2 - y1)/(slope + 0.00001) + x1);
       //printf("1\n");
       if (x2 > AImap_width * 35 || x2 < 0 || y2 > AImap_height * 35 || y2 < 0) {
       //printf("2\n");
       x2 = (int)((float)(AImap_height * 35 - y1)/(slope + 0.00001) + x1);
       //y2 = AImap_height * 35;
       y2 = (int)(slope * (float)(x2 - x1) + y1);
       }
       }
       else if (cos(AI_radian((float)angle)) <= 0 && sin(AI_radian((float)angle)) >= 0) {
       y2 = (int)(slope * (float)(0 - x1) + y1);
       //x2 = 0;
       x2 = (int)((float)(y2 - y1)/(slope + 0.00001) + x1);
       //printf("3\n");
       if (x2 > AImap_width * 35 || x2 < 0 || y2 > AImap_height * 35 || y2 < 0) {
       //printf("4\n");
       x2 = (int)((float)(AImap_height * 35 - y1)/(slope + 0.00001) + x1);
       //y2 = AImap_height * 35;
       y2 = (int)(slope * (float)(x2 - x1) + y1);
       }
       }
       else if (cos(AI_radian((float)angle)) <= 0 && sin(AI_radian((float)angle)) <= 0) {
       //printf("5\n");
       y2 = (int)(slope * (float)(0 - x1) + y1);
       //x2 = 0;
       x2 = (int)((float)(y2 - y1)/(slope + 0.00001) + x1);
       if (x2 > AImap_width * 35 || x2 < 0 || y2 > AImap_height * 35 || y2 < 0) {
       //printf("6\n");
       x2 = (int)((float)(0 - y1)/(slope + 0.00001) + x1);
       //y2 = 0;
       y2 = (int)(slope * (float)(x2 - x1) + y1);
       }
       }
       else if (cos(AI_radian((float)angle)) >= 0 && sin(AI_radian((float)angle)) <= 0) {
       //printf("7\n");
       y2 = (int)(slope * (float)(AImap_width * 35 - x1) + y1);
       //x2 = AImap_width * 35;
       x2 = (int)((float)(y2 - y1)/(slope + 0.00001) + x1);
       if (x2 > AImap_width * 35 || x2 < 0 || y2 > AImap_height * 35 || y2 < 0) {
       //printf("8\n");
       x2 = (int)((float)(0 - y1)/(slope + 0.00001) + x1);
       //y2 = 0;
       y2 = (int)(slope * (float)(x2 - x1) + y1);
       }
       } */



    //printf("AFT:x2: %d, y2: %d AFT\n",x2,y2);
    /*if (x2 < 0 || x2 > AImap_width * 35 || y2 < 0 || y2 > AImap_height * 35) {
       ret.x = 7;
       ret.y = 7;
       return ret;
       } */

    /*if (x2 < 0)
       x2 = 0;
       else if (x2 > AImap_width * 35)
       x2 = AImap_width * 35;
       else if (y2 < 0)
       y2 = 0;
       else if (y2 > AImap_height * 35)
       y2 = AImap_height * 35; */

    //}
    x2 = x02;
    y2 = y02;

    if (x1 < x2) {
	x_min = x1;
	x_max = x2;
	go_right = 1;
	/*yconst = y1; */
    }
    else {
	x_min = x2;
	x_max = x1;
	go_right = 0;
	/*yconst = y2; */
    }

    if (y1 < y2) {
	y_min = y1;
	y_max = y2;
	go_up = 1;
    }
    else {
	y_min = y2;
	y_max = y1;
	go_up = 0;
    }

    /*xslope = (float)(y2 - y1) / ((float)(x2 - x1) + 0.00001);
       yslope = 1.0 / xslope; */

    wallxi_min = x_min / AIMAP_PPB;
    wallxi_max = x_max / AIMAP_PPB;
    /*wallxi_pmax = x_max / AIMAP_PPB; */

    wallyi_min = y_min / AIMAP_PPB;
    wallyi_max = y_max / AIMAP_PPB;

    /*yconst = yconst / AIMAP_PPB; */

    if (go_up)
	wallyi = wallyi_min;
    else
	wallyi = wallyi_max;


    while (oky()) {
	if (go_right)
	    wallxi = wallxi_min;
	else
	    wallxi = wallxi_max;

	/*for this commented code I was trying to get it to check only the possible squares
	   in a diagonal between the two ships.  I got it mostly working, but then decided
	   it's probably faster the regular way where it checks all blocks, because most of
	   the time it's just skipping over empty blocks */
	/*temp1 = (1.0 / xslope ) * (wallyi - 1) - (yconst / xslope) + wallxi_min;
	   temp2 = (1.0 / xslope) * (wallyi + 1) - (yconst / xslope) + wallxi_min;
	   if (temp1 <= temp2) {
	   wallxi = temp1;
	   wallxi_max = temp2;
	   }
	   else {
	   wallxi = temp2;
	   wallxi_max = temp1;
	   }
	   if (wallxi < wallxi_min)
	   wallxi = wallxi_min;
	   if (wallxi_max > wallxi_pmax)
	   wallxi_max = wallxi_pmax; */

	/*printf("xslope: %f, yslope: %f, yconst: %d\n",xslope,yslope,yconst);
	   printf("x1: %d, y1: %d, x2: %d, y2: %d\n", x1, y1, x2, y2);
	   printf("wallyi: %d, wallxi_min: %d, wallxi: %d, wallxi_max: %d\n",wallyi ,wallxi_min, wallxi, wallxi_max); */

	while (okx()) {
	    if ((AImap[wallxi][wallyi] & BLUE_BIT)
		&& (AImap[wallxi][wallyi] & BLUE_UP)) {
		x = AIintersect_atX(wallxi * AIMAP_PPB,
				    wallyi * AIMAP_PPB + AIMAP_PPB,
				    wallxi * AIMAP_PPB + AIMAP_PPB,
				    wallyi * AIMAP_PPB + AIMAP_PPB, x1, y1,
				    x2, y2);
		//printf("up:x: %d, nx_min: %d, nx_max: %d\n", x, wallxi * AIMAP_PPB, wallxi * AIMAP_PPB + AIMAP_PPB);
		if (x >= wallxi * AIMAP_PPB
		    && x <= wallxi * AIMAP_PPB + AIMAP_PPB) {
		    y = AIintersect_atY(wallxi * AIMAP_PPB,
					wallyi * AIMAP_PPB + AIMAP_PPB,
					wallxi * AIMAP_PPB + AIMAP_PPB,
					wallyi * AIMAP_PPB + AIMAP_PPB, x1,
					y1, x2, y2);
		    //printf("up:y: %d, ny_must: %d\n", y, wallyi * AIMAP_PPB + AIMAP_PPB); 
		    if (y == wallyi * AIMAP_PPB + AIMAP_PPB)
			//printf("up: x: %d, y: %d\n",x,y);
			//return (wallxi << 16) | wallyi;
			closestx = x;
		    closesty = y;
		    //return (x << 16) | y;
		}
	    }
	    if ((AImap[wallxi][wallyi] & BLUE_BIT)
		&& (AImap[wallxi][wallyi] & BLUE_DOWN)) {
		x = AIintersect_atX(wallxi * AIMAP_PPB, wallyi * AIMAP_PPB,
				    wallxi * AIMAP_PPB + AIMAP_PPB,
				    wallyi * AIMAP_PPB, x1, y1, x2, y2);
		if (x >= wallxi * AIMAP_PPB
		    && x <= wallxi * AIMAP_PPB + AIMAP_PPB) {
		    y = AIintersect_atY(wallxi * AIMAP_PPB,
					wallyi * AIMAP_PPB,
					wallxi * AIMAP_PPB + AIMAP_PPB,
					wallyi * AIMAP_PPB, x1, y1, x2,
					y2);
		    //printf("dn:x: %d, y: %d, ymust: %d\n", x, y, wallyi * AIMAP_PPB);
		    if (y == wallyi * AIMAP_PPB)
			//printf("down: x: %d, y: %d\n",x,y);
			//return (wallxi << 16) | wallyi;
			if (closestx == -1
			    || AI_distance(x, y, x1,
					   y1) < AI_distance(closestx,
							     closesty, x1,
							     y1)) {
			    closestx = x;
			    closesty = y;
			}
		    //return (x << 16) | y;
		}
	    }
	    /*if ((AImap[wallxi][wallyi] & BLUE_BIT) && (AImap[wallxi][wallyi] & BLUE_DOWN)) {
	       x = AIintersect_atX(wallxi * AIMAP_PPB, wallyi * AIMAP_PPB, wallxi * AIMAP_PPB + AIMAP_PPB, wallyi * AIMAP_PPB, x1, y1, x2, y2);
	       if (x >= wallxi * AIMAP_PPB && x <= wallxi * AIMAP_PPB + AIMAP_PPB) {
	       y = AIintersect_atY(wallxi * AIMAP_PPB, wallyi * AIMAP_PPB, wallxi * AIMAP_PPB + AIMAP_PPB, wallyi * AIMAP_PPB, x1, y1, x2, y2);
	       if (y == wallyi * AIMAP_PPB)
	       //printf("wall: x: %d, y: %d\n",x,y);
	       //return (wallxi << 16) | wallyi;
	       if (closestx == -1 || AI_distance(x, y, x1, y1) < AI_distance(closestx, closesty, x1, y1)) {
	       closestx = x;
	       closesty = y;
	       }
	       //return (x << 16) | y;
	       }
	       } */
	    if ((AImap[wallxi][wallyi] & BLUE_BIT)
		&& (AImap[wallxi][wallyi] & BLUE_LEFT)) {
		y = AIintersect_atY(wallxi * AIMAP_PPB,
				    wallyi * AIMAP_PPB + AIMAP_PPB,
				    wallxi * AIMAP_PPB, wallyi * AIMAP_PPB,
				    x1, y1, x2, y2);
		if (y >= wallyi * AIMAP_PPB
		    && y <= wallyi * AIMAP_PPB + AIMAP_PPB) {
		    x = AIintersect_atX(wallxi * AIMAP_PPB,
					wallyi * AIMAP_PPB + AIMAP_PPB,
					wallxi * AIMAP_PPB,
					wallyi * AIMAP_PPB, x1, y1, x2,
					y2);
		    //printf("left:x: %d, y: %d, ymin: %d, ymax: %d, xmust: %d\n", x, y, wallyi * AIMAP_PPB, wallyi * AIMAP_PPB + AIMAP_PPB, wallxi * AIMAP_PPB);
		    if (x == wallxi * AIMAP_PPB)
			//printf("left: x: %d, y: %d\n",x,y);
			//return (wallxi << 16) | wallyi;
			if (closestx == -1
			    || AI_distance(x, y, x1,
					   y1) < AI_distance(closestx,
							     closesty, x1,
							     y1)) {
			    closestx = x;
			    closesty = y;
			}
		    //return (x << 16) | y;
		}
	    }
	    if ((AImap[wallxi][wallyi] & BLUE_BIT)
		&& (AImap[wallxi][wallyi] & BLUE_RIGHT)) {
		y = AIintersect_atY(wallxi * AIMAP_PPB + AIMAP_PPB,
				    wallyi * AIMAP_PPB + AIMAP_PPB,
				    wallxi * AIMAP_PPB + AIMAP_PPB,
				    wallyi * AIMAP_PPB, x1, y1, x2, y2);
		if (y >= wallyi * AIMAP_PPB
		    && y <= wallyi * AIMAP_PPB + AIMAP_PPB) {
		    x = AIintersect_atX(wallxi * AIMAP_PPB + AIMAP_PPB,
					wallyi * AIMAP_PPB + AIMAP_PPB,
					wallxi * AIMAP_PPB + AIMAP_PPB,
					wallyi * AIMAP_PPB, x1, y1, x2,
					y2);
		    //printf("right:x: %d, y: %d, ymin: %d, ymax: %d, xmust: %d\n", x, y, wallyi * AIMAP_PPB, wallyi * AIMAP_PPB + AIMAP_PPB, wallxi * AIMAP_PPB);
		    if (x == wallxi * AIMAP_PPB + AIMAP_PPB)
			//printf("right: x: %d, y: %d\n",x,y);
			//return (wallxi << 16) | wallyi;
			if (closestx == -1
			    || AI_distance(x, y, x1,
					   y1) < AI_distance(closestx,
							     closesty, x1,
							     y1)) {
			    closestx = x;
			    closesty = y;
			}
		    //return (x << 16) | y;
		}
	    }
	    if ((AImap[wallxi][wallyi] & BLUE_CLOSED)
		&& (AImap[wallxi][wallyi] & BLUE_BIT)
		&& !(AImap[wallxi][wallyi] & BLUE_OPEN)) {
		y = AIintersect_atY(wallxi * AIMAP_PPB,
				    wallyi * AIMAP_PPB + AIMAP_PPB,
				    wallxi * AIMAP_PPB + AIMAP_PPB,
				    wallyi * AIMAP_PPB, x1, y1, x2, y2);
		if (y >= wallyi * AIMAP_PPB
		    && y <= wallyi * AIMAP_PPB + AIMAP_PPB) {
		    x = AIintersect_atX(wallxi * AIMAP_PPB,
					wallyi * AIMAP_PPB + AIMAP_PPB,
					wallxi * AIMAP_PPB + AIMAP_PPB,
					wallyi * AIMAP_PPB, x1, y1, x2,
					y2);
		    //printf("closed:x: %d, y: %d, ymin: %d, ymax: %d, xmin: %d, xmax: %d\n", x, y, wallyi * AIMAP_PPB, wallyi * AIMAP_PPB + AIMAP_PPB, wallxi * AIMAP_PPB, wallxi * AIMAP_PPB + AIMAP_PPB);
		    if (x >= wallxi * AIMAP_PPB
			&& x <= wallxi * AIMAP_PPB + AIMAP_PPB)
			//printf("wall: x: %d, y: %d\n",x,y);
			//return (wallxi << 16) | wallyi;
			if (closestx == -1
			    || AI_distance(x, y, x1,
					   y1) < AI_distance(closestx,
							     closesty, x1,
							     y1)) {
			    closestx = x;
			    closesty = y;
			}
		    //return (x << 16) | y;
		}
	    }
	    if (!(AImap[wallxi][wallyi] & BLUE_CLOSED)
		&& (AImap[wallxi][wallyi] & BLUE_BIT)
		&& (AImap[wallxi][wallyi] & BLUE_OPEN)) {
		y = AIintersect_atY(wallxi * AIMAP_PPB, wallyi * AIMAP_PPB,
				    wallxi * AIMAP_PPB + AIMAP_PPB,
				    wallyi * AIMAP_PPB + AIMAP_PPB, x1, y1,
				    x2, y2);
		if (y >= wallyi * AIMAP_PPB
		    && y <= wallyi * AIMAP_PPB + AIMAP_PPB) {
		    x = AIintersect_atX(wallxi * AIMAP_PPB,
					wallyi * AIMAP_PPB,
					wallxi * AIMAP_PPB + AIMAP_PPB,
					wallyi * AIMAP_PPB + AIMAP_PPB, x1,
					y1, x2, y2);
		    //printf("open:x: %d, y: %d, ymin: %d, ymax: %d, xmin: %d, xmax: %d\n", x, y, wallyi * AIMAP_PPB, wallyi * AIMAP_PPB + AIMAP_PPB, wallxi * AIMAP_PPB, wallxi * AIMAP_PPB + AIMAP_PPB);
		    if (x >= wallxi * AIMAP_PPB
			&& x <= wallxi * AIMAP_PPB + AIMAP_PPB)
			//printf("wall: x: %d, y: %d\n",x,y);
			//return (wallxi << 16) | wallyi;
			if (closestx == -1
			    || AI_distance(x, y, x1,
					   y1) < AI_distance(closestx,
							     closesty, x1,
							     y1)) {
			    closestx = x;
			    closesty = y;
			}
		    //return (x << 16) | y;
		}
	    }
	    if (closestx != -1) {
		//return (closestx << 16) | closesty;
		ret.x = closestx;
		ret.y = closesty;
		return ret;
	    }
	    if (go_right)
		wallxi++;
	    else
		wallxi--;
	}
	if (go_up)
	    wallyi++;
	else
	    wallyi--;
    }
    ret.x = 0;
    ret.y = 0;
    return ret;
}


int AIintersect_atX(int L1x1, int L1y1, int L1x2, int L1y2, int L2x1,
		    int L2y1, int L2x2, int L2y2)
{
    float L1m, L1c, L2m, L2c;

    /*get slope of L1 */
    L1m = (L1y2 - L1y1 + 0.00001) / (L1x2 - L1x1 + 0.00001);	/*add 0.00001 to prevent divide by zero */

    /*get the C constant for the L1 line equation */
    if (L1x2 < L1x1)
	L1c = L1y2 + L1m * -L1x2;
    else
	L1c = L1y1 + L1m * -L1x1;


    /*get slope of L2 */
    L2m = (L2y2 - L2y1 + 0.00001) / (L2x2 - L2x1 + 0.00001);	/*add 0.00001 to prevent divide by zero */

    /*get the C constant for the L2 line equation */
    if (L2x2 < L2x1)
	L2c = L2y2 + L2m * -L2x2;
    else
	L2c = L2y1 + L2m * -L2x1;

    /*return X that intersects */
    return (int) (0.5 + (L2c - L1c) / (L1m - L2m));

}


int AIintersect_atY(int L1x1, int L1y1, int L1x2, int L1y2, int L2x1,
		    int L2y1, int L2x2, int L2y2)
{
    float L1m, L1c, L2m, L2c;

    /*get slope of L1 */
    L1m = (L1x2 - L1x1 + 0.00001) / (L1y2 - L1y1 + 0.00001);	/*add 0.00001 to prevent divide by zero */

    /*get the C constant for the L1 line equation */
    if (L1y2 < L1y1)
	L1c = L1x2 + L1m * -L1y2;
    else
	L1c = L1x1 + L1m * -L1y1;

    /*get slope of L2 */
    L2m = (L2x2 - L2x1 + 0.00001) / (L2y2 - L2y1 + 0.00001);	/*add 0.00001 to prevent divide by zero */

    /*get the C constant for the L2 line equation */
    if (L2y2 < L2y1)
	L2c = L2x2 + L2m * -L2y2;
    else
	L2c = L2x1 + L2m * -L2y1;

    /*return X that intersects */

    return (int) (0.5 + (L2c - L1c) / (L1m - L2m));	/*+0.5 rounds up */
}


int AI_distance(int x1, int y1, int x2, int y2)
{
    return (int) sqrt(sqr(abs(x1 - x2)) + sqr(abs(y1 - y2)));
}

float AI_radian(float degree)
{
    return 2.0 * M_PI / 360.0 * degree;
}

float AI_degree(float radian)
{
    return (360.0 * radian) / (2.0 * M_PI);
}


void AImain(void)
{
    return;
}				/* do nothing, redefine later for use */

void callback(void)
{
    return;
}
