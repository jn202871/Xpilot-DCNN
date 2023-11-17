(foreign-declare "
#include \"xpilot_ai.h\"")

(use srfi-18)

(define xpilot_setargs
	(foreign-safe-lambda void "AI_xpilot_setargs" c-string))

(define xpilot_launch
	(foreign-safe-lambda int "AI_xpilot_launch"))

(define xpilot
	(lambda (args)
		(begin
			(xpilot_setargs args)
			(thread-start! (make-thread xpilot_launch)))))

(define AImain
	(lambda () (noop)))

(define AImain_callback
	(foreign-safe-wrapper void "AImain"
		() (lambda () (AImain))))

(define-external (callback) void
	(thread-yield!))
	
(define AIself.thrust
	(foreign-safe-lambda void "AIself_thrust" int))

(define AIself.turn
	(foreign-safe-lambda void "AIself_turn" int))

(define AIself.shoot
	(foreign-safe-lambda void "AIself_shoot" int))

(define AIself.shield
	(foreign-safe-lambda void "AIself_shield_enable" int))
	
(define AIself.destruct
	(foreign-safe-lambda void "AIself_destruct"))

(define AI.talk 
	(foreign-safe-lambda void "AI_talk" c-string))

(define AI.msg.to?
	(foreign-safe-lambda c-string "AImsg_to" int))

(define AI.msg.from?
	(foreign-safe-lambda c-string "AImsg_from" int))

(define AI.msg.body?
	(foreign-safe-lambda c-string "AImsg_body" int))

(define AI.teamplay?
	(foreign-safe-lambda int "AI_teamplay"))


(define AIself.id?
	(foreign-safe-lambda int "AIself_id"))

(define AIself.alive?
	(foreign-safe-lambda int "AIself_alive"))

(define AIself.x?
	(foreign-safe-lambda int "AIself_x"))

(define AIself.y?
	(foreign-safe-lambda int "AIself_y"))

(define AIself.heading?
	(foreign-safe-lambda int "AIself_heading"))

(define AIself.vel?
	(foreign-safe-lambda int "AIself_vel"))

(define AIself.track?
	(foreign-safe-lambda int "AIself_track"))

(define AIself.mapx?
	(foreign-safe-lambda int "AIself_mapx"))

(define AIself.mapy?
	(foreign-safe-lambda int "AIself_mapy"))

(define AIself.team?
	(foreign-safe-lambda int "AIself_team"))

(define AIself.life?
	(foreign-safe-lambda int "AIself_life"))

(define AIself.shield?
	(foreign-safe-lambda int "AIself_shield"))

(define AIself.name?
	(foreign-safe-lambda c-string "AIself_name"))

(define AIself.score?
	(foreign-safe-lambda float "AIself_score"))

(define AIself.reload?
	(foreign-safe-lambda float "AIself_reload"))



(define AIself.HUD.name?
	(foreign-safe-lambda c-string "AIself_HUD_name" int))

(define AIself.HUD.score?
	(foreign-safe-lambda float "AIself_HUD_score" int))

(define AIself.HUD.time?
	(foreign-safe-lambda int "AIself_HUD_time" int))


(define AIship.x?
	(foreign-safe-lambda int "AIship_x" int))

(define AIship.y?
	(foreign-safe-lambda int "AIship_y" int))

(define AIship.heading?
	(foreign-safe-lambda int "AIship_heading" int))

(define AIship.vel?
	(foreign-safe-lambda int "AIship_vel" int))

(define AIship.acc?
	(foreign-safe-lambda int "AIship_acc" int))

(define AIship.track?
	(foreign-safe-lambda int "AIship_track" int))

(define AIship.dist?
	(foreign-safe-lambda int "AIship_dist" int))

(define AIship.id?
	(foreign-safe-lambda int "AIship_id" int))

(define AIship.xdir?
	(foreign-safe-lambda int "AIship_xdir" int))

(define AIship.shield?
	(foreign-safe-lambda int "AIship_shield" int))

(define AIship.life?
	(foreign-safe-lambda int "AIship_life" int))

(define AIship.team?
	(foreign-safe-lambda int "AIship_team" int))

(define AIship.reload?
	(foreign-safe-lambda int "AIship_reload" int))

(define AIship.name?
	(foreign-safe-lambda c-string "AIship_name" int))

(define AIship.aimdir?
	(foreign-safe-lambda int "AIship_aimdir" int))
	
	
(define AIshot.x?
	(foreign-safe-lambda int "AIshot_x" int))

(define AIshot.y?
	(foreign-safe-lambda int "AIshot_y" int))

(define AIshot.dist?
	(foreign-safe-lambda int "AIshot_dist" int))

(define AIshot.xdir?
	(foreign-safe-lambda int "AIshot_xdir" int))

(define AIshot.vel?
	(foreign-safe-lambda int "AIshot_vel" int))

(define AIshot.track?
	(foreign-safe-lambda int "AIshot_track" int))

(define AIshot.imaginary?
	(foreign-safe-lambda int "AIshot_imaginary" int))

(define AIshot.idir?
	(foreign-safe-lambda int "AIshot_idir" int))

(define AIshot.idist?
	(foreign-safe-lambda int "AIshot_idist" int))

(define AIshot.itime?
	(foreign-safe-lambda int "AIshot_itime" int))

(define AIshot.alert?
	(foreign-safe-lambda int "AIshot_alert" int))

(define AIshot.id?
	(foreign-safe-lambda int "AIshot_id" int))


(define AIradar.x?
	(foreign-safe-lambda int "AIradar_x" int))

(define AIradar.y?
	(foreign-safe-lambda int "AIradar_y" int))

(define AIradar.dist?
	(foreign-safe-lambda int "AIradar_dist" int))

(define AIradar.xdir?
	(foreign-safe-lambda int "AIradar_xdir" int))

(define AIradar.enemy?
	(foreign-safe-lambda int "AIradar_enemy" int))


;returns -1 if no wall between
(define AI.wallbetween
	(foreign-safe-lambda int "AI_wallbetween" int int int int))

(define AI.wallbetween.x
	(foreign-safe-lambda int "AI_wallbetween_x" int int int int))

(define AI.wallbetween.y
	(foreign-safe-lambda int "AI_wallbetween_y" int int int int))


(define AI.tomap
	(foreign-safe-lambda int "tomap" int))

(define AI.frmap
	(foreign-safe-lambda int "frmap" int))

(define AI.map?
	(foreign-safe-lambda int "AImap_get" int int))

(define AI.map.set
	(foreign-safe-lambda void "AImap_set" int int int))

(define anglediff
	(foreign-safe-lambda int "anglediff" int int))

(define angleadd
	(foreign-safe-lambda int "angleadd" int int))

(define rad
	(foreign-safe-lambda float "rad" int))

(define deg
	(foreign-safe-lambda int "deg" float))

(define AI.setmaxturn
	(foreign-safe-lambda void "AI_setmaxturn" int))

(define AI.presskey
	(foreign-safe-lambda void "AI_presskey" int))
	
(define AI.releasekey
	(foreign-safe-lambda void "AI_releasekey" int))

(define int
	(lambda (n)
		(inexact->exact (floor n))))
		
(define float
	(lambda (n)
		(* n 1.0)))


(define KEY_DUMMY					0)
(define KEY_LOCK_NEXT				1)		
(define KEY_LOCK_PREV				2)		
(define KEY_LOCK_CLOSE				3)		
(define KEY_CHANGE_HOME				4)		
(define KEY_SHIELD					5)								
(define KEY_FIRE_SHOT				6)		
(define KEY_FIRE_MISSILE			7)		
(define KEY_FIRE_TORPEDO			8)		
(define KEY_TOGGLE_NUCLEAR			9)				
(define KEY_FIRE_HEAT				10)			
(define KEY_DROP_MINE				11)		
(define KEY_DETACH_MINE				12)		
(define KEY_TURN_LEFT				13)		
(define KEY_TURN_RIGHT				14)		
(define KEY_SELF_DESTRUCT			15)		
(define KEY_LOSE_ITEM				16)			
(define KEY_PAUSE					17)		
(define KEY_TANK_DETACH				18)		
(define KEY_TANK_NEXT				19)		
(define KEY_TANK_PREV				20)						
(define KEY_TOGGLE_VELOCITY			21)		
(define KEY_TOGGLE_CLUSTER			22)				
(define KEY_SWAP_SETTINGS			23)		
(define KEY_REFUEL					24)		
(define KEY_CONNECTOR				25)		
(define KEY_INCREASE_POWER			26)		
(define KEY_DECREASE_POWER			27)		
(define KEY_INCREASE_TURNSPEED		28)		
(define KEY_DECREASE_TURNSPEED		29)		
(define KEY_THRUST					30)				
(define KEY_CLOAK					31)		
(define KEY_ECM						32)		
(define KEY_DROP_BALL				33)		
(define KEY_TRANSPORTER				34)		
(define KEY_TALK					35)		
(define KEY_FIRE_LASER				36)		
(define KEY_LOCK_NEXT_CLOSE			37)		
(define KEY_TOGGLE_COMPASS			38)		
(define KEY_TOGGLE_MINI				39)		
(define KEY_TOGGLE_SPREAD			40)					
(define KEY_TOGGLE_POWER			41)		
(define KEY_TOGGLE_AUTOPILOT		42)		
(define KEY_TOGGLE_LASER			43)		
(define KEY_EMERGENCY_THRUST		44)		
(define KEY_TRACTOR_BEAM			45)		
(define KEY_PRESSOR_BEAM			46)		
(define KEY_CLEAR_MODIFIERS			47)		
(define KEY_LOAD_MODIFIERS_1		48)		
(define KEY_LOAD_MODIFIERS_2		49)		
(define KEY_LOAD_MODIFIERS_3		50)				
(define KEY_LOAD_MODIFIERS_4		51)		
(define KEY_SELECT_ITEM				52)			
(define KEY_PHASING					53)		
(define KEY_REPAIR					54)		
(define KEY_TOGGLE_IMPLOSION		55)		
(define KEY_REPROGRAM				56)		
(define KEY_LOAD_LOCK_1				57)		
(define KEY_LOAD_LOCK_2				58)		
(define KEY_LOAD_LOCK_3				59)		
(define KEY_LOAD_LOCK_4				60)					
(define KEY_EMERGENCY_SHIELD		61)		
(define KEY_HYPERJUMP				62)			
(define KEY_DETONATE_MINES			63)		
(define KEY_DEFLECTOR				64)			
(define KEY_UNUSED_65				65)		
(define KEY_UNUSED_66				66)		
(define KEY_UNUSED_67				67)		
(define KEY_UNUSED_68				68)		
(define KEY_UNUSED_69				69)		
(define KEY_UNUSED_70				70)				
(define KEY_UNUSED_71				71)		
(define NUM_KEYS					72)

(define KEY_MSG_1					73)		; talk macros ;
(define KEY_MSG_2					74)		
(define KEY_MSG_3					75)		
(define KEY_MSG_4					76)		
(define KEY_MSG_5					77)		
(define KEY_MSG_6					78)		
(define KEY_MSG_7					79)		
(define KEY_MSG_8					80)		
(define KEY_MSG_9					81)		
(define KEY_MSG_10					82)		
(define KEY_MSG_11					83)		
(define KEY_MSG_12					84)		
(define KEY_MSG_13					85)		
(define KEY_MSG_14					86)		
(define KEY_MSG_15					87)		
(define KEY_MSG_16					88)		
(define KEY_MSG_17					89)		
(define KEY_MSG_18					90)		
(define KEY_MSG_19					91)		
(define KEY_MSG_20					92)		

(define KEY_ID_MODE					93)		
(define KEY_TOGGLE_OWNED_ITEMS		94)		
(define KEY_TOGGLE_MESSAGES			95)		
(define KEY_POINTER_CONTROL			96)		
(define KEY_TOGGLE_RECORD			97)		
(define KEY_PRINT_MSGS_STDOUT		98)		
(define KEY_TALK_CURSOR_LEFT		99)		
(define KEY_TALK_CURSOR_RIGHT		100)		
(define KEY_TALK_CURSOR_UP			101)		
(define KEY_TALK_CURSOR_DOWN		102)		
(define KEY_SWAP_SCALEFACTOR		103)		
(define NUM_CLIENT_KEYS				104)
