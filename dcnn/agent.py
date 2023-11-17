# agent that reads the neural network from the .pt file to control the ship

def AI_loop():
    #Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setPower(25)

ai.start(AI_loop,["-name","dcnn-agent","-join","localhost"])