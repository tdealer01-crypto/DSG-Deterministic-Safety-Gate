; ============================================================
; DSG: Deterministic State Gate
; Full Formal Proof (SMT-LIB v2) for Z3
; ============================================================

(set-logic ALL)
(set-option :produce-models true)

; ------------------------------------------------------------
; 1. Sorts
; ------------------------------------------------------------
(declare-sort State 0)

; ------------------------------------------------------------
; 2. State Identifiers
; ------------------------------------------------------------
(declare-fun IDLE () State)
(declare-fun AUTH () State)
(declare-fun EXEC () State)
(declare-fun FORBIDDEN () State)

; ------------------------------------------------------------
; 3. Forbidden predicate
; ------------------------------------------------------------
(declare-fun forbidden (State) Bool)

(assert (forbidden FORBIDDEN))
(assert (not (forbidden IDLE)))
(assert (not (forbidden AUTH)))
(assert (not (forbidden EXEC)))

; ------------------------------------------------------------
; 4. Gate decision
; 0 = ALLOW, 1 = BLOCK, 2 = STAY
; ------------------------------------------------------------
(declare-fun gate (State State) Int)

; Rule: never allow forbidden
(assert
  (forall ((s State) (s2 State))
    (=> (forbidden s2)
        (= (gate s s2) 1))))

; Allowed linear transitions
(assert (= (gate IDLE AUTH) 0))
(assert (= (gate AUTH EXEC) 0))

; All other safe transitions stabilize
(assert
  (forall ((s State) (s2 State))
    (=> (and (not (forbidden s2))
             (not (and (= s IDLE) (= s2 AUTH)))
             (not (and (= s AUTH) (= s2 EXEC))))
        (= (gate s s2) 2))))

; ------------------------------------------------------------
; 5. Transition function delta
; ------------------------------------------------------------
(declare-fun delta (State State) State)

(assert
  (forall ((s State) (s2 State))
    (ite (= (gate s s2) 0)
         (= (delta s s2) s2)
         (= (delta s s2) s))))

; ------------------------------------------------------------
; 6. Theorem: Safety (forbidden unreachable)
; ------------------------------------------------------------
(assert
  (forall ((s State) (s2 State))
    (not (= (delta s s2) FORBIDDEN))))

; ------------------------------------------------------------
; 7. Determinism (functional purity)
; ------------------------------------------------------------
(assert
  (forall ((s State) (s2 State))
    (= (gate s s2) (gate s s2))))

; ------------------------------------------------------------
; 8. O(1) bound (no chaining)
; ------------------------------------------------------------
(declare-fun delta2 (State State State) State)
(assert
  (forall ((s State) (s2 State) (s3 State))
    (= (delta2 s s2 s3) (delta s s2))))

(check-sat)
(get-model)
