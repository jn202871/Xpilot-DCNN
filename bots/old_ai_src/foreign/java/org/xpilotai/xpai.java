package org.xpilotai;

import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Platform;
import com.sun.jna.Callback;

/** Simple example of native library declaration and usage. */
public abstract class xpai {

	private interface AImain_callback extends Callback
	{
		void callback ();
	}

    private interface xpilot_ai extends Library {
        xpilot_ai INSTANCE = (xpilot_ai)
            Native.loadLibrary((Platform.isWindows() ? "xpilot_ai" : "xpilot_ai"),
                               xpilot_ai.class);
    	
		void AI_xpilot_setargs (String args);
		int AI_xpilot_launch();
		void AI_setcallback(AImain_callback func);

		void AIself_thrust (int thrust);
		void AIself_turn (int turn);
		void AIself_shoot (int shoot);
		void AIself_shield_enable (int shield);

		void AI_talk (String message);
		String AImsg_to (int which);
		String AImsg_from (int which);
		String AImsg_body (int which);
		
		
		int AI_teamplay ();	
		
		int AIself_id ();
		int AIself_alive ();
		int AIself_x ();
		int AIself_y ();
		int AIself_heading ();
		int AIself_vel ();
		int AIself_track ();
		int AIself_mapx ();
		int AIself_mapy ();
		int AIself_team ();
		int AIself_life ();
		int AIself_shield ();
		String AIself_name ();
		float AIself_score ();
		int AIself_reload ();
		void AIself_destruct ();
		
		void AI_presskey(int key);
		void AI_releasekey(int key);
		
		
		String AIself_HUD_name (int which);
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
		String AIship_name (int which);
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
		
		int AImap_get (int mapx, int mapy);
		void AImap_set (int mapx, int mapy, int value);
		int tomap (int n);
		int frmap (int mapn);
		
		int anglediff (int angle1, int angle2);
		int angleadd (int angle1, int angle2);
		
		float rad (int deg);
		int deg (float rad);
		
		void AI_setmaxturn (int maxturn);

    }

	public abstract void AImain();
	
	public void xpilot (String commandargs) {

		AImain_callback func;
		func = new AImain_callback()
		{
			public void callback()
			{	
				AImain();
			}

		};

		xpilot_ai.INSTANCE.AI_setcallback(func);	
		
		xpilot_ai.INSTANCE.AI_xpilot_setargs(commandargs);
		xpilot_ai.INSTANCE.AI_xpilot_launch();

	}
	
	
	
	public void AIself_thrust (int thrust) {	
		xpilot_ai.INSTANCE.AIself_thrust (thrust);
	}	
	public void AIself_turn (int turn) {	
		xpilot_ai.INSTANCE.AIself_turn (turn);
	}	
	public void AIself_shoot (int shoot) {	
		xpilot_ai.INSTANCE.AIself_shoot (shoot);
	}	
	public void AIself_shield_enable (int shield) {	
		xpilot_ai.INSTANCE.AIself_shield_enable (shield);

	}	
	public void AI_talk (String message) {	
		xpilot_ai.INSTANCE.AI_talk (message);
	}	
	public String AImsg_to (int which) {	
		return xpilot_ai.INSTANCE.AImsg_to (which);
	}	
	public String AImsg_from (int which) {	
		return xpilot_ai.INSTANCE.AImsg_from (which);
	}	
	public String AImsg_body (int which) {	
		return xpilot_ai.INSTANCE.AImsg_body (which);
	
	}	
	public int AI_teamplay () {	
		return xpilot_ai.INSTANCE.AI_teamplay ();	
		
	}	
	public int AIself_id () {	
		return xpilot_ai.INSTANCE.AIself_id ();
	}	
	public int AIself_alive () {	
		return xpilot_ai.INSTANCE.AIself_alive ();
	}	
	public int AIself_x () {	
		return xpilot_ai.INSTANCE.AIself_x ();
	}	
	public int AIself_y () {	
		return xpilot_ai.INSTANCE.AIself_y ();
	}	
	public int AIself_heading () {	
		return xpilot_ai.INSTANCE.AIself_heading ();
	}	
	public int AIself_vel () {	
		return xpilot_ai.INSTANCE.AIself_vel ();
	}	
	public int AIself_track () {	
		return xpilot_ai.INSTANCE.AIself_track ();
	}	
	public int AIself_mapx () {	
		return xpilot_ai.INSTANCE.AIself_mapx ();
	}	
	public int AIself_mapy () {	
		return xpilot_ai.INSTANCE.AIself_mapy ();
	}	
	public int AIself_team () {	
		return xpilot_ai.INSTANCE.AIself_team ();
	}	
	public int AIself_life () {	
		return xpilot_ai.INSTANCE.AIself_life ();
	}	
	public int AIself_shield () {	
		return xpilot_ai.INSTANCE.AIself_shield ();
	}	
	public String AIself_name () {	
		return xpilot_ai.INSTANCE.AIself_name ();
	}	
	public float AIself_score () {	
		return xpilot_ai.INSTANCE.AIself_score ();
	}	
	public int AIself_reload () {	
		return xpilot_ai.INSTANCE.AIself_reload ();
	}	
	public void AIself_destruct () {	
		xpilot_ai.INSTANCE.AIself_destruct ();
		
	}	
	public void AI_presskey(int key) {	
		xpilot_ai.INSTANCE.AI_presskey(key);
	}	
	public void AI_releasekey(int key) {	
		xpilot_ai.INSTANCE.AI_releasekey(key);
		
		
	}	
	public String AIself_HUD_name (int which) {	
		return xpilot_ai.INSTANCE.AIself_HUD_name (which);
	}	
	public float AIself_HUD_score (int which) {	
		return xpilot_ai.INSTANCE.AIself_HUD_score (which);
	}	
	public int AIself_HUD_time (int which) {	
		return xpilot_ai.INSTANCE.AIself_HUD_time (which);
		
		
	}	
	public int AIship_x (int which) {	
		return xpilot_ai.INSTANCE.AIship_x (which); 
	}	
	public int AIship_y (int which) {	
		return xpilot_ai.INSTANCE.AIship_y (which);
	}	
	public int AIship_heading (int which) {	
		return xpilot_ai.INSTANCE.AIship_heading (which);
	}	
	public int AIship_vel (int which) {	
		return xpilot_ai.INSTANCE.AIship_vel (which);
	}	
	public int AIship_acc (int which) {	
		return xpilot_ai.INSTANCE.AIship_acc (which);
	}	
	public int AIship_track (int which) {	
		return xpilot_ai.INSTANCE.AIship_track (which);
	}	
	public int AIship_dist (int which) {	
		return xpilot_ai.INSTANCE.AIship_dist (which);
	}	
	public int AIship_id (int which) {	
		return xpilot_ai.INSTANCE.AIship_id (which);
	}	
	public int AIship_xdir (int which) {	
		return xpilot_ai.INSTANCE.AIship_xdir (which);
	}	
	public int AIship_shield (int which) {	
		return xpilot_ai.INSTANCE.AIship_shield (which);
	}	
	public int AIship_life (int which) {	
		return xpilot_ai.INSTANCE.AIship_life (which);
	}	
	public int AIship_team (int which) {	
		return xpilot_ai.INSTANCE.AIship_team (which);
	}	
	public int AIship_reload (int which) {	
		return xpilot_ai.INSTANCE.AIship_reload (which);
	}	
	public String AIship_name (int which) {	
		return xpilot_ai.INSTANCE.AIship_name (which);
	}	
	public int AIship_aimdir (int which) {	
		return xpilot_ai.INSTANCE.AIship_aimdir (which);
		
	}	
	public int AIshot_x (int which) {	
		return xpilot_ai.INSTANCE.AIshot_x (which);
	}	
	public int AIshot_y (int which) {	
		return xpilot_ai.INSTANCE.AIshot_y (which);
	}	
	public int AIshot_dist (int which) {	
		return xpilot_ai.INSTANCE.AIshot_dist (which);
	}	
	public int AIshot_xdir (int which) {	
		return xpilot_ai.INSTANCE.AIshot_xdir (which);
	}	
	public int AIshot_vel (int which) {	
		return xpilot_ai.INSTANCE.AIshot_vel (which);
	}	
	public int AIshot_track (int which) {	
		return xpilot_ai.INSTANCE.AIshot_track (which);
	}	
	public int AIshot_imaginary (int which) {	
		return xpilot_ai.INSTANCE.AIshot_imaginary (which);	
	}	
	public int AIshot_idir (int which) {	
		return xpilot_ai.INSTANCE.AIshot_idir (which);
	}	
	public int AIshot_idist (int which) {	
		return xpilot_ai.INSTANCE.AIshot_idist (which);
	}	
	public int AIshot_itime (int which) {	
		return xpilot_ai.INSTANCE.AIshot_itime (which);
	}	
	public int AIshot_alert (int which) {	
		return xpilot_ai.INSTANCE.AIshot_alert (which);
	}	
	public int AIshot_id (int which) {	
		return xpilot_ai.INSTANCE.AIshot_id (which);
		
	}	
	public int AIradar_x (int which) {	
		return xpilot_ai.INSTANCE.AIradar_x (which);
	}	
	public int AIradar_y (int which) {	
		return xpilot_ai.INSTANCE.AIradar_y (which);
	}	
	public int AIradar_dist (int which) {	
		return xpilot_ai.INSTANCE.AIradar_dist (which);
	}	
	public int AIradar_xdir (int which) {	
		return xpilot_ai.INSTANCE.AIradar_xdir (which);
	}	
	public int AIradar_enemy (int which) {	
		return xpilot_ai.INSTANCE.AIradar_enemy (which);
		
	}	
	public int AI_wallbetween (int x1, int y1, int x2, int y2) {	
		return xpilot_ai.INSTANCE.AI_wallbetween (x1, y1, x2, y2);
	}	
	public int AI_wallbetween_x (int x1, int y1, int x2, int y2) {	
		return xpilot_ai.INSTANCE.AI_wallbetween_x (x1, y1, x2, y2);
	}	
	public int AI_wallbetween_y (int x1, int y1, int x2, int y2) {	
		return xpilot_ai.INSTANCE.AI_wallbetween_y (x1, y1, x2, y2);
		
	}	
	public int AImap_get (int mapx, int mapy) {	
		return xpilot_ai.INSTANCE.AImap_get (mapx, mapy);
	}	
	public void AImap_set (int mapx, int mapy, int value) {	
		xpilot_ai.INSTANCE.AImap_set (mapx, mapy, value);
	}	
	public int tomap (int n) {	
		return xpilot_ai.INSTANCE.tomap (n);
	}	
	public int frmap (int mapn) {	
		return xpilot_ai.INSTANCE.frmap (mapn);
		
	}	
	public int anglediff (int angle1, int angle2) {	
		return xpilot_ai.INSTANCE.anglediff (angle1, angle2);
	}	
	public int angleadd (int angle1, int angle2) {	
		return xpilot_ai.INSTANCE.angleadd (angle1, angle2);
		
	}	
	public float rad (int deg) {	
		return xpilot_ai.INSTANCE.rad (deg);
	}	
	public int deg (float rad) {	
		return xpilot_ai.INSTANCE.deg (rad);
		
	}	
	public void AI_setmaxturn (int maxturn) {	
		xpilot_ai.INSTANCE.AI_setmaxturn (maxturn);
	}
}
