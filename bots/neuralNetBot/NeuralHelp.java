// Xpilot agent controlled by a neural network
// Jay Nash & Russell Kosovsky

import java.io.*;
import java.util.*;

class NeuralHelp extends javaAI {
        static Network net = null;
        @Override
        public void AI_loop() {
            thrust(0);
            turnRight(0);
            turnLeft(0);
            int heading = (int)selfHeadingDeg();
            int tracking = (int)selfTrackingDeg();
            double rawDist = enemyDistance(0);
            double aimDiff = ((aimdir(0)-heading+540)%360)-180;
            double trackDiff = ((tracking-heading+540)%360)-180;
            
            double modDist;
            if (rawDist > 10000 || rawDist == -1) {
            	modDist = 10000;
            } else {
            	modDist = rawDist;
            }
            
            int wallBetween = 0;
            
            if (wallBetween(selfX(),selfY(),screenEnemyX(0),screenEnemyY(0),-1,0) != -1) {
            	wallBetween = 1;
            } else {wallBetween = 0;}

            double[] inputs = {
                selfHeadingDeg()/360,
                selfTrackingDeg()/360,
  
                wallFeeler(1000,heading)/800,
                wallFeeler(1000,heading+10)/800,
                wallFeeler(1000,heading-10)/800,
                
                //wallFeeler(1000,heading+45)/1000,
                //wallFeeler(1000,heading+135)/1000,
  
                wallFeeler(1000,heading+90)/800,
                wallFeeler(1000,heading+100)/800,
                wallFeeler(1000,heading+80)/800,
                
                //wallFeeler(1000,heading-45)/1000,
                //wallFeeler(1000,heading-135)/1000,
  
                wallFeeler(1000,heading+270)/800,
                wallFeeler(1000,heading+280)/800,
                wallFeeler(1000,heading+260)/800,
  
                wallFeeler (1000,heading+180)/800,
                wallFeeler(1000,heading+190)/800,
                wallFeeler(1000,heading+170)/800,
  
                wallFeeler(1000,tracking)/800,
                wallFeeler(1000,tracking+10)/800,
                wallFeeler(1000,tracking-10)/800,
                
                modDist/10000,
                aimDiff/180,
                trackDiff/180,
                selfSpeed()/15,
                //wallBetween
            };
            double[] actions = net.think(inputs);
            int thrust = 0;
            int shoot = 0;
            int left = 0;
            int right = 0;
            if (actions[0] > 0.5) {
                thrust(1);
                thrust = 1;
            }
            if (actions[1] > 0.5) {
                turnLeft(1);
                left = 1;
            }
            if (actions[2] > 0.5) {
                turnRight(1);
                right = 1;
            }
            if (actions[3] > 0.5) {
                fireShot();
                shoot = 1;
            }
            
            if (selfSpeed() == 0) {
            	thrust(1);
            	thrust = 1;
            }
            if (selfAlive() == 1) {
            	record(thrust,shoot,left,right);
            System.out.println(Arrays.toString(actions));
            }
        }

        public NeuralHelp(String args[]) {
                super(args);
        }
        
        public static void main(String args[]) {
            String[] new_args = {"-name","Help","-join","localhost"};
            try {
                FileInputStream file = new FileInputStream("net.ser");
                ObjectInputStream in = new ObjectInputStream(file);

                net = (Network)in.readObject();

                in.close();
                file.close();
                System.out.println("Nerual Net Loaded");
            } catch(IOException ex) {
                System.out.println("IOException");
            } catch(ClassNotFoundException ex) {
                System.out.println("Net File Not Found");
            }
                NeuralHelp help = new NeuralHelp(new_args);
        }
        
        private void record(int thrust, int shoot, int left, int right) {
            
            int[][] area = new int[112][112];
            for (int i = 0; i < 112; i++) {
            	area[i][0] = 1;
            	area[i][111] = 1;
            	area[0][i] = 1;
            	area[111][i] = 1;
            }
            
            int x_cord = (int)(selfX() / 10);
        	int y_cord = 111 - (int)(selfY() / 10);
        	area[y_cord][x_cord] = 3;
        	double aimdir = aimdir(0);
        	if (aimdir < 0) {
            	aimdir = -1;
        	}
        	area[y_cord][x_cord + 1] = (int)selfSpeed();
        	area[y_cord][x_cord - 1] = (int)aimdir;
        	area[y_cord + 1][x_cord] = (int)selfHeadingDeg();
        	area[y_cord - 1][x_cord] = (int)selfTrackingDeg();

        	// Enemy Heading And Position Tracking
        	int enemy = closestShipId();
        	if (enemy != -1) {
            	int ex_cord = (int)(screenEnemyX(0) / 10);
            	int ey_cord = 111 - (int)(screenEnemyY(0) / 10);
            	area[ey_cord][ex_cord] = 4;
            	area[ey_cord][ex_cord + 1] = (int)enemySpeed(0);
            	area[ey_cord + 1][ex_cord] = (int)enemyHeadingDeg(0);
            	double enemyTracking = enemyTrackingDeg(0);
            	if (Double.isNaN(enemyTracking)) {
                	enemyTracking = enemyHeadingDeg(0);
            	}
            	area[ey_cord - 1][ex_cord] = (int)enemyTracking;
        	}

        	// Bullet Tracking
        	int bulletIndex = 0;
        	List<int[]> bullets = new ArrayList<>();
        	while(shotAlert(bulletIndex) != -1) {
            	int bulletX = (int)(shotX(bulletIndex) / 10);
            	int bulletY = 111 - (int)(shotY(bulletIndex) / 10);
            	int bulletAlert = (int)shotAlert(bulletIndex);
            	if (bulletAlert == 30000) {
                	bulletAlert = 0;
            	}
            	bullets.add(new int[]{bulletX, bulletY, bulletAlert});
            	bulletIndex++;
        	}
        	for (int[] bullet : bullets) {
            	area[bullet[1]][bullet[0]] = 5;
            	area[bullet[1]][bullet[0] + 1] = bullet[2];
        	}
        	StringBuilder frameStrBuilder = new StringBuilder();
			for (int[] innerlist : area) {
    			for (int item : innerlist) {
        			frameStrBuilder.append(item).append(",");
    			}
			}
			// Remove the last comma
			String frameStr = frameStrBuilder.toString();
			if (frameStr.length() > 0) {
    			frameStr = frameStr.substring(0, frameStr.length() - 1);
			}

			String actionStr = thrust + "," + shoot + "," + left + "," + right;
        	
        	try {
        		FileWriter fw = new FileWriter("data.txt", true);
   			BufferedWriter bw = new BufferedWriter(fw);
    			bw.write(frameStr);
    			bw.newLine();
    			bw.write(actionStr);
    			bw.newLine();
    			bw.close();
    			//FileWriter fw = new FileWriter("actions", true);
   			//BufferedWriter bw = new BufferedWriter(fw);
    			//bw.write("Spain");
    			//bw.newLine();
    			//bw.close();
        	} catch (Exception e) {
        		System.out.println("IO ERROR");
        	}
        }
}

