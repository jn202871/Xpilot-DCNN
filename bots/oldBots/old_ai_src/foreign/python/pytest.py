import xpai

def AImain():
	xpai.self_turn(10)
	return
	

xpai.set_AImain(AImain)

xpai.setargs("-name jim")
xpai.launch()
