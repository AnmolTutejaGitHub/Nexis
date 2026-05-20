(defpackage :my-app
  (:use :cl)
  (:export #:factorial #:fibonacci #:process-list))

(in-package :my-app)

(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(defun fibonacci (n)
  (cond
    ((= n 0) 0)
    ((= n 1) 1)
    (t (+ (fibonacci (- n 1)) (fibonacci (- n 2))))))

(defmacro with-retry (n &body body)
  `(let ((attempts ,n))
     (loop while (> attempts 0)
           do (progn ,@body)
           (decf attempts))))

(defmacro when-let ((var form) &body body)
  `(let ((,var ,form))
     (when ,var ,@body)))

(defun process-list (items)
  (mapcar #'factorial items))

(defun flatten (lst)
  (cond
    ((null lst) nil)
    ((listp (car lst)) (append (flatten (car lst)) (flatten (cdr lst))))
    (t (cons (car lst) (flatten (cdr lst))))))
