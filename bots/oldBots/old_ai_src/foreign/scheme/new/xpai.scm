;; Xpilot-AI module for Chicken Scheme v4. The convention I follow in
;; this file is that identifiers wrapped in percent signs (%) are
;; private functions and not exported.
(module xpai
  (xpilot xpilot-bg AI-main
   press-key release-key

   thrust shoot turn
   self-destruct talk shield

   anglediff anglesub angleadd
   deg->rad rad->deg

   alive? score teamplay?
   reload shield? id
   x-pos y-pos heading
   track vel team
   life name

   shot-x shot-y shot-dist
   shot-xdir shot-speed shot-track
   shot-imag shot-idir shot-idist
   shot-alert shot-id

   accel ship-dist radar-dist
   radar-x radar-y
   radar-xdir radar-enemy

   xdir aimdir

   HUD-time HUD-score HUD-name
   msg-to msg-from msg-body

   pos radar-pos on-radar?
   on-screen? wall-between
   tile tile-set! max-turn)
  
  (import scheme chicken foreign data-structures ports)
  (use srfi-1 srfi-18)
  
  (foreign-declare "#include <xpilot_ai.h>")

  ;; Utility functions
  (define (%stringify% . strings)
    (with-output-to-string
      (lambda ()
	(for-each (lambda (s)
		    (printf "~A " s))
		  strings))))
  
  (define (%to-int% . args)
    (apply values (map (o inexact->exact round) args)))
  
  ;;; Foreign functions

  ;;; Callback to C
  ;; Xpilot-ai will call the function 'AImain' each frame.
  (define %xp-thread% #f)
  (define-external (AImain) void
    ;; Yield to repl thread for interactive development
    (when %xp-thread% (thread-yield!))
    (AI-main))

  ;; Users will redefine AI-main scheme function.
  (define AI-main noop)

  ;; Functions to deal with the xpilot process. The function xpilot
  ;; takes a list of arguments to pass to the client-process and
  ;; launches the client.
  (define (%set-args% args-list)
    (unless (null? args-list)
	    ((foreign-safe-lambda void "AI_xpilot_setargs" c-string)
	     (apply %stringify% args-list))))

  ;; Returns #t on success
  (define (xpilot . args)
    (%set-args% args)
    ((foreign-safe-lambda bool "AI_xpilot_launch")))

  ;; Run in background thread
  (define (xpilot-bg . args)
    (set! %xp-thread%
	  (thread-start!
	   (lambda ()
	     (apply xpilot args)
	     (thread-terminate! %xp-thread%)
	     (set! %xp-thread% #f)))))

  (define press-key (o (foreign-safe-lambda void "AI_presskey" int)
		       inexact->exact round))
  (define release-key (o (foreign-safe-lambda void "AI_releasekey" int)
			 inexact->exact round))

  ;; Simple action functions. These functions may take a boolean or no
  ;; arguments. Supplying #f will inhibit the action, #t will enable
  ;; it.
  (define (thrust #!optional (t #t))
    ((foreign-safe-lambda void "AIself_thrust" bool) t))
  
  (define (shoot #!optional (t #t))
    ((foreign-safe-lambda void "AIself_shoot" bool) t))
  
  (define (self-destruct #!optional (t #t))
    (when t ((foreign-safe-lambda void "AIself_destruct"))))

  (define (shield #!optional (t #t))
    ((foreign-safe-lambda void "AIself_shield_enable" bool) t))
  
  (define (turn angle)
    ((foreign-safe-lambda void "AIself_turn" int) (round angle)))

  ;; Chat function - concatenates its arguments, which may be of any
  ;; printable type, to form the message string
  (define (talk . messages)
    ((foreign-safe-lambda void "AI_talk" c-string)
     (apply %stringify% messages)))
  
  ;;; Arithmetic
  (define (anglesub . args)
    (remainder (fold-right - 0 args)
	       360))
  
  ;; Add up n angles
  (define (angleadd . args)
    (remainder (reduce + 0 args)
	       360))

  ;; Shortest distance between two angles
  (define (anglediff a1 a2)
    (let ((l (- a1 a2))
	  (r (- (+ a1 360) a2)))
      (remainder (if (< (abs l) (abs r)) l r)
		 360)))

  (define deg->rad (o (foreign-safe-lambda float "rad" int)
			    inexact->exact round))
  
  (define rad->deg (o (foreign-safe-lambda int "deg" float)
			    exact->inexact))

  ;; State access functions: We use a macro to remove some redundancy.
  ;; In general, no arguments retrieves state for self. n arguments
  ;; retrieves state for n ships and returns multiple values. Some
  ;; arguments aren't applicable to other ships and vice versa. This
  ;; macro accounts for that.
  (define-syntax %get-state%
    (syntax-rules (self ship both)
      ((_ self ret name filter)
       (lambda ()
	 (filter ((foreign-safe-lambda ret name)))))
      ((_ self ret name)
       (%get-state% self ret name identity))

      ((_ ship ret name filter)
       (lambda (first . rest)
	 (apply values (map (o filter (foreign-safe-lambda ret name int))
			    (cons first rest)))))
      ((_ ship ret name)
       (%get-state% ship ret name identity))
      
      ((_ both ret self-name ship-name filter)
       (lambda idx
	 (if (null? idx)
	     ((%get-state% self ret self-name filter))
	     (apply (%get-state% ship ret ship-name filter) idx))))
      ((_ both ret self-name ship-name)
       (%get-state% both ret self-name ship-name identity))))

  ;; Xpilot-AI returns -1 to indicate an invalid value
  ;; sometimes. We'll return #f instead.
  (define (%filter-negative% x)
    (and (> x -1) x))

  (define (%filter-string% s)
    (and (> (string-length s) 0) s))
  
  (define alive?    (%get-state% self bool  "AIself_alive"))
  (define score     (%get-state% self float "AIself_score"))
  (define teamplay? (%get-state% self bool  "AI_teamplay"))

  (define reload  (%get-state% both int "AIself_reload" "AIship_reload" %filter-negative%))
  (define shield? (%get-state% both int "AIself_shield" "AIship_shield"
			       (lambda (r)
				 (> r 1))))
  (define id      (%get-state% both int  "AIself_id"    "AIship_id" %filter-negative%))
  (define x-pos   (%get-state% both int  "AIself_x"     "AIship_x" %filter-negative%))
  (define y-pos   (%get-state% both int  "AIself_y"     "AIship_y" %filter-negative%))
  (define heading (%get-state% both int  "AIself_heading" "AIship_heading" %filter-negative%))
  (define track   (%get-state% both int  "AIself_track" "AIship_track" %filter-negative%))
  (define vel     (%get-state% both int "AIself_vel"     "AIship_vel"     %filter-negative%))
  (define team    (%get-state% both int "AIself_team"    "AIship_team"    %filter-negative%))
  (define life    (%get-state% both int "AIself_life"    "AIship_life"    %filter-negative%))
  ;; c-string becomes #f if a NULL string is returned; exactly what we want
  (define name    (%get-state% both c-string "AIself_name" "AIship_name"))
  (define shot-x      (%get-state% ship int "AIshot_x"         %filter-negative%))
  (define shot-y      (%get-state% ship int "AIshot_y"         %filter-negative%))
  (define shot-dist   (%get-state% ship int "AIshot_dist"      %filter-negative%))
  (define shot-xdir   (%get-state% ship int "AIshot_xdir"      %filter-negative%))
  (define shot-speed  (%get-state% ship int "AIshot_vel"       %filter-negative%))
  (define shot-track  (%get-state% ship int "AIshot_track"     %filter-negative%))
  (define shot-imag   (%get-state% ship int "AIshot_imaginary" %filter-negative%))
  (define shot-idir   (%get-state% ship int "AIshot_idir"      %filter-negative%))
  (define shot-idist  (%get-state% ship int "AIshot_idist"     %filter-negative%))
  (define shot-alert  (%get-state% ship int "AIshot_alert"     %filter-negative%))
  (define shot-id     (%get-state% ship int "AIshot_id"        %filter-negative%))
  (define accel       (%get-state% ship int "AIship_acc"       %filter-negative%))
  (define ship-dist   (%get-state% ship int "AIship_dist"      %filter-negative%))
  (define radar-dist  (%get-state% ship int "AIradar_dist"     %filter-negative%))
  (define radar-x     (%get-state% ship int "AIradar_x"        %filter-negative%))
  (define radar-y     (%get-state% ship int "AIradar_y"        %filter-negative%))
  (define radar-xdir  (%get-state% ship int "AIradar_xdir"     %filter-negative%))
  (define radar-enemy (%get-state% ship int "AIradar_enemy"    %filter-negative%))
  (define xdir        (%get-state% ship int "AIship_xdir"      %filter-negative%))
  (define aimdir      (%get-state% ship int "AIship_aimdir"    %filter-negative%))
  ;; Not sure why this is needed, but we have to shift HUD-time return
  ;; value one place over
  (define HUD-time    (%get-state% ship int "AIself_HUD_time"  (o %filter-negative% sub1)))
  (define HUD-score   (%get-state% ship float "AIself_HUD_score"
				   (lambda (r)
				     (not (= r -99999.0)))))
  (define HUD-name    (%get-state% ship c-string "AIself_HUD_name" %filter-string%))
  (define msg-to      (%get-state% ship c-string "AImsg_to" %filter-string%))
  (define msg-from    (%get-state% ship c-string "AImsg_from" %filter-string%))
  (define msg-body    (%get-state% ship c-string "AImsg_body" %filter-string%))

  (define (pos . idx)
    (values (apply x-pos idx)
	    (apply y-pos idx)))

  (define (radar-pos idx)
    (values (radar-x idx) (radar-y idx)))

  ;; Return #t if ships are visible
  (define (on-radar? . idx)
    (apply values (map (o not not radar-enemy) idx)))
  
  (define (on-screen? . idx)
    (apply values (map (o not not id) idx)))

  ;; return distance and coordinates of wall between two points, or
  ;; wall between self and point if one point is given. Returns #f if
  ;; there is no wall.
  (define wall-between
    (let ((w  (compose %filter-negative%
		       (foreign-safe-lambda int "AI_wallbetween" int int int int)
		       %to-int%))
	  (wx (compose %filter-negative%
		       (foreign-safe-lambda int "AI_wallbetween_x" int int int int)
		       %to-int%))
	  (wy (compose %filter-negative%
		       (foreign-safe-lambda int "AI_wallbetween_y" int int int int)
		       %to-int%)))
      (case-lambda
       ((x y) (wall-between (x-pos) (y-pos) x y))
       ((x1 y1 x2 y2) (values (w  x1 y1 x2 y2)
			      (wx x1 y1 x2 y2)
			      (wy x1 y1 x2 y2))))))

  ;; Accessing map data
  (define (%to-map% x y)
    (values ((foreign-safe-lambda int "tomap" int) (%to-int% x))
	    ((foreign-safe-lambda int "tomap" int) (%to-int% y))))

  (define (tile #!optional (x (x-pos)) (y (y-pos)))
    ((compose (foreign-safe-lambda int "AImap_get" int int) %to-map%)
     x y))

  (define tile-set!
    (let ((set-tile (foreign-safe-lambda void "AImap_set" int int int)))
      (case-lambda
       ((val) ((compose (lambda (x y) (set-tile x y val)) %to-map% pos)))
       ((x y val) ((compose (lambda (xp yp) (set-tile xp yp val)) %to-map%) x y)))))

  ;; 20 is arbitrary, picked from AI.h file. TODO - get the real maxturn value
  (define max-turn
    (make-parameter 20
		    (each (o (foreign-safe-lambda void "AI_setmaxturn" int) %to-int%)
			  identity)))
  )


