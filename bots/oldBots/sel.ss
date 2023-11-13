#! /usr/local/bin/csi -s
(require 'posix)
(use xpai)
(xpilot " -name Sel -join localhost -port 45000")

(randomize)
(define playtime (+ 900 (random 1500)))

(AI.setmaxturn 15)

(define alive.was 0)

(define feeler
	(lambda (range degree)
		(let ([beady (AI.wallbetween 
						(AIself.x?) (AIself.y?) 
						(+ (AIself.x?) (int (* range (cos (rad degree)))))
						(+ (AIself.y?) (int (* range (sin (rad degree))))))])
				(if (= beady -1)
					range
					beady))))

(define ship.xdir?
	(lambda (num)
		(letrec ((ncount 0)
			(onscreen
				(lambda (n)
					(if (= (AIship.x? n) -1)
						-1
						(if (= num ncount)
							(AIship.xdir? n)
							(begin 
								(set! ncount (add1 ncount))
								(onscreen (add1 n)))))))
			(radarscreen
				(lambda (n)
					(if (= (AIradar.x? n) -1)
						-1
						(if (= num ncount)
							(AIradar.xdir? n)
							(begin 
								(set! ncount (add1 ncount))
								(radarscreen (add1 n))))))))
			(let ((os (onscreen 0)))
				(if (= os -1)
					(radarscreen ncount)
					os)))))		
								
(define ship.x?
	(lambda (num)
		(letrec ((ncount 0)
			(onscreen
				(lambda (n)
					(if (= (AIship.x? n) -1)
						-1
						(if (= num ncount)
							(AIship.x? n)
							(begin 
								(set! ncount (add1 ncount))
								(onscreen (add1 n)))))))
			(radarscreen
				(lambda (n)
					(if (= (AIradar.x? n) -1)
						-1
						(if (= num ncount)
							(AIradar.x? n)
							(begin 
								(set! ncount (add1 ncount))
								(radarscreen (add1 n))))))))
			(let ((os (onscreen 0)))
				(if (= os -1)
					(radarscreen ncount)
					os)))))	


(define ship.y?
	(lambda (num)
		(letrec ((ncount 0)
			(onscreen
				(lambda (n)
					(if (= (AIship.x? n) -1)
						-1
						(if (= num ncount)
							(AIship.y? n)
							(begin 
								(set! ncount (add1 ncount))
								(onscreen (add1 n)))))))
			(radarscreen
				(lambda (n)
					(if (= (AIradar.x? n) -1)
						-1
						(if (= num ncount)
							(AIradar.y? n)
							(begin 
								(set! ncount (add1 ncount))
								(radarscreen (add1 n))))))))
			(let ((os (onscreen 0)))
				(if (= os -1)
					(radarscreen ncount)
					os)))))
			

(define ship.dist?
	(lambda (num)
		(letrec ((ncount 0)
			(onscreen
				(lambda (n)
					(if (= (AIship.x? n) -1)
						-1
						(if (= num ncount)
							(AIship.dist? n)
							(begin 
								(set! ncount (add1 ncount))
								(onscreen (add1 n)))))))
			(radarscreen
				(lambda (n)
					(if (= (AIradar.x? n) -1)
						-1
						(if (= num ncount)
							(AIradar.dist? n)
							(begin 
								(set! ncount (add1 ncount))
								(radarscreen (add1 n))))))))
			(let ((os (onscreen 0)))
				(if (= os -1)
					(radarscreen ncount)
					os)))))	
(define change-team
	(lambda (team)
		(AI.talk (string-append "/team " (number->string team)))))

(define switch-team
	(lambda ()
		(if (= 4 (AIself.team?)) (change-team 3)
			(change-team 4))))
					
(define enemy-num
	(lambda (n)
		(cond 
			[(= (AIradar.x? n) -1) -1]
			[(= (AIradar.enemy? n) 1) n]
			[else (enemy-num (add1 n))])))

(define swath-angle
	(lambda (n)
		(cond
			((= n 0) 0)
			((= n 1) 15)
			((= n 2) -15)
			((= n 3) 30)
			((= n 4) -30)
			((= n 5) 45)
			((= n 6) -45)
			((= n 7) 60)
			((= n 8) -60)
			((= n 9) 75)
			((= n 10) -75)
			((= n 11) 90)
			((= n 12) -90))))



(define wall-edge
	(lambda (xdir dist)
		(if (or (= -1 xdir) (= -1 dist))
			(angleadd (AIself.track?) 180))
		(letrec ((helper
			(lambda (n)
				(if (> n 12) 
					(list -1 -1)
					(let ((wb (feeler dist (angleadd xdir (swath-angle n)))))
						(if (= wb dist) 
							(list n wb)
							(let ((rb (helper (add1 n))))
								(if (> wb (cadr rb))
									(list n wb)
									rb))))))))
			(angleadd xdir (swath-angle (car (helper 0)))))))

(define trackto
	(lambda (a)
		(turnto (angleadd (AIself.track?) (anglediff a (AIself.track?))))))

(define turnto
	(lambda (a)
		(AIself.turn (anglediff (AIself.heading?) a))))
			
(define sel-main (lambda ()
	(if (equal? (AI.msg.to? 0) (AIself.name?))
		(cond
			((equal? (AI.msg.body? 0) "pause") (AI.presskey KEY_PAUSE) (AI.releasekey KEY_PAUSE))
			(else (AI.talk (AI.msg.body? 0))))) 

			
		(if (and (= (AIself.alive?) 0) (= alive.was 1) (= 1 (random 20)))
			(AI.talk (string-append "/team " (number->string (AIself.team?)))))
		(set! alive.was (AIself.alive?))
				
	(if (= 1 (AIself.alive?)) (begin
		(cond
			((and (> (AIshot.alert? 0) -1) (< (AIshot.alert? 0) 60))
				(begin 
					(AIself.turn (anglediff (AIself.heading?) (angleadd (AIshot.idir? 0) 180)))
					(AIself.thrust 1)))
			((not (= -1 (AI.wallbetween (AIself.x?) (AIself.y?) (ship.x? 0) (ship.y? 0))))
				;(AIself.turn (anglediff (AIself.heading?) (wall-edge (ship.xdir? 0) (ship.dist? 0))))
				(turnto (wall-edge (ship.xdir? 0) (ship.dist? 0)))
				(if (< (AIself.vel?) 8) (AIself.thrust 1)))
			((and (> (AIship.xdir? 0) -1) (< (abs (- (AIself.heading?) (AIship.aimdir? 0))) 5))
				(AIself.shoot 1)
				(turnto (AIship.aimdir? 0)))
			((and (> (AIship.xdir? 0) -1) (> (abs (- (AIself.heading?) (AIship.aimdir? 0))) 5))
				(turnto (AIship.aimdir? 0)))
			((< (abs (- (AIradar.xdir? 0) (AIself.heading?))) 5)
				(AIself.shoot 1)
				(trackto (AIradar.xdir? 0))
				(if (not (and (< (abs (anglediff (AIself.track?) (AIradar.xdir? 0))) 15) (< (AIself.vel?) 7)))
					(AIself.thrust 1)))
			((not (< (AIradar.x? 0) 0)) 
				(AIself.turn (anglediff (AIself.heading?) (angleadd (- (random 20) 10) (AIradar.xdir? 0))))))
		(cond
			((let ([feeler1 (feeler 500 (angleadd (AIself.track?) -15))]
				   [feeler2 (feeler 500 (angleadd (AIself.track?) 15))])
				(cond
					[(and (= feeler1 feeler2) (< feeler1 (* 20 (AIself.vel?))) (> (AIself.vel?) 1))
						(AIself.turn (anglediff (AIself.heading?) (angleadd 180 (AIself.track?))))
						(if (< (anglediff (AIself.heading?) (angleadd 180 (AIself.track?))) 30) (AIself.thrust 1))]
					[(and (< feeler1 feeler2) (< feeler1 (* 20 (AIself.vel?))) (> (AIself.vel?) 1))
						(AIself.turn (anglediff (AIself.heading?) (angleadd 180 (angleadd -15 (AIself.track?)))))
						(if (< (anglediff (AIself.heading?) (angleadd 180 (angleadd -15 (AIself.track?)))) 30) (AIself.thrust 1))]
					[(and (> feeler1 feeler2) (< feeler2 (* 20 (AIself.vel?))) (> (AIself.vel?) 1))
						(AIself.turn (anglediff (AIself.heading?) (angleadd 180 (angleadd 15 (AIself.track?)))))
						(if (< (anglediff (AIself.heading?) (angleadd 180 (angleadd 15 (AIself.track?)))) 30) (AIself.thrust 1))])))
			((and (= i 0) (= (AIself.alive?) 0)) (set! i 1) (AI.talk "You got me, tim"))
			((and (= i 1) (= (AIself.alive?) 1)) (set! i 0)))))))

(thread-sleep! 3)
(define AImain sel-main)

(define dosleep
	(lambda (time)
		(if (= time playtime) (noop))
		(thread-sleep! 1)
		(dosleep (add1 time))))

(dosleep 0)
