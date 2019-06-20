
(cl:in-package :asdf)

(defsystem "face_follower-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "rlist" :depends-on ("_package_rlist"))
    (:file "_package_rlist" :depends-on ("_package"))
  ))