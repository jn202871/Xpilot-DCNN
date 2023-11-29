/*functions to get variable from AI and Specifics modules to a foreign program*/
#include <stdlib.h>

#include "AI.h"
#include "xpilot_ai.h"
#include "string.h"
 
void AI_xpilot_setargs (char *s) { 
    int i;
    char *a;
    char *argv[128];

    for(i=0,a=strtok(s," "); i<128 && s; i++,s=strtok(NULL, " "))
        argv[i] = a;

    xpilot_setargv(i - 1, argv);
}

void AI_xpilot_setargv (int argc, char **argv) {
	xpilot_setargv(argc, argv);
}

int AI_xpilot_launch (void) {
	xpilot_launch();
	return 1;
}

void AIself_thrust        (int b) { AIself.thrust        = b; }
void AIself_turn          (int b) { AIself.turn          = b; }
void AIself_shoot         (int b) { AIself.shoot         = b; }
void AIself_shield_enable (int b) { AIself.shield_enable = b; }

/* Consider defining functions here, removing AI_self_destruct() - DAA */
void AIself_destruct (void) { AI_self_destruct(); }
void AI_talk (char *message) { AItalk(message); }

char* AImsg_to   (int which) { return AI_msg[which].to; }
char* AImsg_from (int which) { return AI_msg[which].from; }
char* AImsg_body (int which) { return AI_msg[which].body; }

int AI_teamplay (void) { return AIteamplay; }

int AIself_id      (void) { return AIself.id; }
int AIself_alive   (void) { return AIself.alive; }
int AIself_x       (void) { return AIself.x; }
int AIself_y       (void) { return AIself.y; }
int AIself_heading (void) { return AIself.heading; }
int AIself_vel     (void) { return AIself.vel; }
int AIself_track   (void) { return AIself.veldir; }
int AIself_mapx    (void) { return AIself.x / AIMAP_PPB; }
int AIself_mapy    (void) { return AIself.y / AIMAP_PPB; }
int AIself_team    (void) { return AIself.team; }
int AIself_life    (void) { return AIself.life; }
int AIself_shield  (void) { return AIself.shield; }
char* AIself_name  (void) { return AIself.name; }
float AIself_score (void) { return AIself.score; }
int AIself_reload  (void) { return AIself.reload; }

/* Again, is the indirection really needed? - DAA */
void AI_presskey(int key) {
	return AIpressKey(key);
}

void AI_releasekey(int key) {
	return AIreleaseKey(key);
}

char* AIself_HUD_name  (int which) { return AIself_HUD[which].name; }
float AIself_HUD_score (int which) { return AIself_HUD[which].score; }
int   AIself_HUD_time  (int which) { return AIself_HUD[which].time; }

#define AI_PROPERTY(idx, name) AIship_pointer[idx]!= -1? AIship[AIship_pointer[idx]].name: -1
int AIship_x       (int idx) { return AI_PROPERTY(idx, x[0]); }
int AIship_y       (int idx) { return AI_PROPERTY(idx, y[0]); }
int AIship_heading (int idx) { return AI_PROPERTY(idx, heading[0]); }
int AIship_vel     (int idx) { return AI_PROPERTY(idx, vel[0]); }
int AIship_acc     (int idx) { return AI_PROPERTY(idx, acc[0]); }
int AIship_track   (int idx) { return AI_PROPERTY(idx, veldir[0]); }
int AIship_dist    (int idx) { return AI_PROPERTY(idx, dist[0]); }
int AIship_id      (int idx) { return AI_PROPERTY(idx, id); }
int AIship_xdir    (int idx) { return AI_PROPERTY(idx, xdir); }
int AIship_shield  (int idx) { return AI_PROPERTY(idx, shield); }
int AIship_life    (int idx) { return AI_PROPERTY(idx, life); }
int AIship_team    (int idx) { return AI_PROPERTY(idx, team); }
int AIship_reload  (int idx) { return AI_PROPERTY(idx, reload); }
int AIship_aimdir  (int idx) { return AIship_calcfxdir(AIship_pointer[idx]); }

int AIshot_x         (int idx) { return AIshot[idx].x; }
int AIshot_y         (int idx) { return AIshot[idx].y; }
int AIshot_dist      (int idx) { return AIshot[idx].dist; }
int AIshot_xdir      (int idx) { return AIshot[idx].xdir; }
int AIshot_vel       (int idx) { return AIshot[idx].vel; }
int AIshot_track     (int idx) { return AIshot[idx].veldir; }
int AIshot_imaginary (int idx) { return AIshot[idx].imaginary; }
int AIshot_idir      (int idx) { return AIshot[idx].idir; }
int AIshot_idist     (int idx) { return AIshot[idx].idist; }
int AIshot_itime     (int idx) { return AIshot[idx].itime; }
int AIshot_alert     (int idx) { return AIshot[idx].alert; }
int AIshot_id        (int idx) { return AIshot[idx].id; }
char* AIship_name    (int idx) { return AIship_pointer[idx]!= -1? AIship[AIship_pointer[idx]].name: NULL; }

int AIradar_x (int idx) { return AImap_ship[idx].xi!= -1? AImap_ship[idx].xi * AIMAP_PPB: -1; }
int AIradar_y (int idx) { return AImap_ship[idx].xi!= -1? AImap_ship[idx].yi * AIMAP_PPB: -1; }
int AIradar_dist  (int which) { return AImap_ship[which].distance; }
int AIradar_xdir  (int which) { return AImap_ship[which].xdir; }
int AIradar_enemy (int which) { return AImap_ship[which].enemy; }

/* Consider unifying these functions into one that takes extra pointers to store wall coords */
int AI_wallbetween (int x1, int y1, int x2, int y2) {
	struct AImap_xy xy;
	xy = AImap_wallbetween(x1, y1, x2, y2);
	if (xy.x == 0 && xy.y == 0) return -1;
	else
		return AI_distance(x1, y1, xy.x, xy.y);
}

int AI_wallbetween_x (int x1, int y1, int x2, int y2) {
	struct AImap_xy xy;
	xy = AImap_wallbetween(x1, y1, x2, y2);
	if (xy.x == 0 && xy.y == 0) return -1;
	else
		return xy.x;
}

int AI_wallbetween_y (int x1, int y1, int x2, int y2) {
	struct AImap_xy xy;
	xy = AImap_wallbetween(x1, y1, x2, y2);
	if (xy.x == 0 && xy.y == 0) return -1;
	else
		return xy.y;
}

unsigned int AImap_get (int mapx, int mapy) { 
	if (mapx >= 0 && mapx < AIMAP_MAXSIZE && mapy >= 0 && mapy < AIMAP_MAXSIZE)
		return AImap[mapx][mapy];
	else
		return AIMAP_UNSEEN;
}

void AImap_set (int mapx, int mapy, unsigned int value) { 
	if (mapx >= 0 && mapx < AIMAP_MAXSIZE && mapy >= 0 && mapy < AIMAP_MAXSIZE)
		AImap[mapx][mapy] = value;
	return;
}

int tomap (int n) { return n / AIMAP_PPB; }
int frmap (int n) { return n * AIMAP_PPB; }

int anglediff (int angle1, int angle2)
{
  int left = angle2 - angle1;
  int right= angle1 + 360 - angle2;
  
  return (abs(left) < abs(right) ? left: right) % 360;
}

int angleadd (int angle1, int angle2)
{
  return (angle1 + angle2) % 360;
}

/* Does such a simple multiplication need a function? */
float rad (int deg) { return AI_radian ((float)deg); }

int deg (float rad) {
	return (int) AI_degree (rad);
}

void AI_setmaxturn (int maxturn) { AI_max_turnspeed = maxturn; return; }
