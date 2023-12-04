//    -In Xpilot-AI, 0 degrees is to the right and 90 degrees is up.
//
//    -Please note that many of the item related functions simulate keypresses. 
//     So, for example, if pressing Tab would not place a mine 
//     (say, because you have none), dropMine will not either.
//
//    -ID functions refer to a specific ship's ID, 
//     while IDX functions refer to the ship's index within your buffer.



//######################################################################
//######################################################################
//ALL the functions used in SEL that come from AI.c:

    int wall_feeler(int range, int degree);
        AI_wallbetween
        AIself_x() == selfX() 
        AIself_y() == selfY()

    int open_wall(int xdir, int dist);
        angleadd()
        AIself_track()

    int change_tracking(int dir);
        anglediff()
    
    int change_heading(int dir);
	AIself_turn()
        AIself_heading()

    int radar_enemy_num (int n);
        AIship_x()
        AI_teamplay()
        AIself_team()
        AIship_team()
    
    int radar_enemy_num (int n);
        AIradar_x()
        AIradar_enemy()

    void init_feeler_dirs(void);
    int feeler_dirs[13]; // array to store feeler directions



//######################################################################
//######################################################################
//AI.c:

    
    //##################################################################
    //AIself_x/AIself_y SRC:

    //they both return AIself.x (or y) 

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


    //AIship_calcVel/ AIship_calcVelDir SRC:

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
    

    //##################################################################
    //AI_wallbetween SRC:
        int AI_wallbetween (int x1, int y1, int x2, int y2) {
	        struct AImap_xy xy;
	        xy = AImap_wallbetween(x1, y1, x2, y2);
	        if (xy.x == 0 && xy.y == 0) return -1;
	        else
		        return AI_distance(x1, y1, xy.x, xy.y);
        }

        //its the same in libPyAI
        int wallBetween(int x1, int y1, int x2, int y2) 
        - If there is a wall between the given points it returns the distance from point 1 to the first found wall.  
        - If no wall is found it returns -1.

    //##################################################################
    //AIself_track == tracking
    //AIself_heading == heading

    
    //##################################################################
    //AIself_turn SRC:
    
    
    //##################################################################
    //anglediff SRC:


    //##################################################################
    //angleadd SRC:


    //##################################################################
    //AIship_x SRC:


    
    
    //##################################################################
    //AI_teamplay SRC:


    //##################################################################
    //AIself_team SRC:


    //##################################################################
    //AIship_team SRC:


    

    #
    AIradar_x SRC:


    
    AIradar_enemy SRC:





######################################################################
######################################################################
SEL MAIN Function:

    init feeler array
    set turnspeed limit
    set args
    launch
    return 1

    JIMSEL equivalent:
        ai.start(AI_loop,["-name","SelPy","-join","localhost"])



######################################################################
######################################################################
AI_LOOP:

