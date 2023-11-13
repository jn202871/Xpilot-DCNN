#Xpilot-AI Team 2012
#Run: python3 Spinner.py
import libpyAI as ai
def AI_loop():
  ai.turnRight(1)
ai.start(AI_loop,["-name","Dummy","-join","localhost"])
