# Use python 3.10 for this 
#If getting version bugs then use this:
#cd "C:\Users\teren\OneDrive\Desktop\Python\ YOUR FILE HERE"
#py -3.10 -m venv mp_env
#mp_env\Scripts\activate
#now you should be in python 3.1

import cv2
import mediapipe as mp
import math
import time

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

start_time = time.time()
ready = False
DELAY = 5
go_time = None
GO_DELAY = 7

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    model_complexity=0,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def angle_3pts(a, b, c):
    """
    Angle at point b (in degrees), given 3 points a, b, c as (x, y).
    Returns None if something is degenerate.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c

    ba = (ax - bx, ay - by)
    bc = (cx - bx, cy - by)

    mag_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    if mag_ba == 0 or mag_bc == 0:
        return None

    dot = ba[0]*bc[0] + ba[1]*bc[1]
    cosang = dot / (mag_ba * mag_bc)
    cosang = max(min(cosang, 1.0), -1.0)
    return math.degrees(math.acos(cosang))

rep_count = 0           # total counted reps (based on elbow motion)
proper_count = 0        # reps where all 3 checks are OK at bottom
state = "up"            # "up" or "down"
current_has_bottom = False
current_is_proper = False

ELBOW_DOWN_THRESHOLD = 100  # when angle gets smaller than this, you are going down
ELBOW_UP_THRESHOLD   = 100   # when angle gets bigger than this again, you're back up
ELBOW_MIN            = 20   # bottom zone lower bound
ELBOW_MAX            = 70   # bottom zone upper bound

while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = pose.process(rgb_frame)
    frame_h, frame_w, _ = frame.shape

    now = time.time()
    elapsed = int(now-start_time)

    if not ready:
        remaining_time = (DELAY - elapsed)

    if remaining_time > 0:
        cv2.putText(frame, f"Starting in: {remaining_time}", (240, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
        cv2.imshow("Push-up Form - Counter & Analysis", frame)
        cv2.waitKey(1)
        continue 
    else:
        ready = True
    if GO_DELAY - elapsed > 0 and GO_DELAY - elapsed < 3:
        cv2.putText(frame, "GO!", (280,240),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)

    if ready:

        elbow_angle = None
        back_angle = None
        neck_angle = None
        back_ok = False
        elbow_ok = False
        neck_ok = False

        if output.pose_landmarks:
            lm_list = output.pose_landmarks.landmark

            def xy(idx):
                lm = lm_list[idx]
                return int(lm.x * frame_w), int(lm.y * frame_h)

            nose       = xy(0)
            r_shoulder = xy(12)
            r_elbow    = xy(14)
            r_wrist    = xy(16)
            r_hip      = xy(24)
            r_knee     = xy(26)
            r_ankle    = xy(28)

            for p in [nose, r_shoulder, r_elbow, r_wrist, r_hip, r_knee, r_ankle]:
                cv2.circle(frame, p, 4, (0, 255, 0), -1)

            def seg(p1, p2):
                cv2.line(frame, p1, p2, (0, 255, 0), 2)

            seg(nose, r_shoulder)
            seg(r_shoulder, r_elbow)
            seg(r_elbow, r_wrist)
            seg(r_shoulder, r_hip)
            seg(r_hip, r_knee)
            seg(r_knee, r_ankle)

            # --------- ANGLES ---------
            # 1) BACK STRAIGHT: shoulder-hip-ankle
            back_angle = angle_3pts(r_shoulder, r_hip, r_ankle)

            # 2) ELBOW: shoulder-elbow-wrist
            elbow_angle = angle_3pts(r_shoulder, r_elbow, r_wrist)

            # 3) NECK: nose-shoulder-hip
            neck_angle = angle_3pts(nose, r_shoulder, r_hip)

            # --------- SIMPLE CHECKS (for the current frame) ---------
            if back_angle is not None:
                back_ok = abs(back_angle - 180) <= 10   # 170–190 deg

            if elbow_angle is not None:
                # this check is for "bottom" style elbow
                elbow_ok = (ELBOW_MIN <= elbow_angle <= ELBOW_MAX)

            if neck_angle is not None:
                neck_ok = abs(neck_angle - 180) <= 30   # head in line with torso

            # --------- REP LOGIC ---------
            # Only use frames where elbow_angle is valid
            if elbow_angle is not None:
                if state == "up":
                    # start going down
                    if elbow_angle < ELBOW_DOWN_THRESHOLD:
                        state = "down"
                        current_has_bottom = False
                        current_is_proper = False

                elif state == "down":
                    # detect "bottom" once per rep
                    if (not current_has_bottom and
                        ELBOW_MIN <= elbow_angle <= ELBOW_MAX):

                        # only accept this as a bottom if all angles exist
                        if back_angle is not None and neck_angle is not None:
                            current_has_bottom = True

                            # proper = all three checks true at bottom
                            if back_ok and elbow_ok and neck_ok:
                                current_is_proper = True

                    # detect going back up and finishing the rep
                    if elbow_angle > ELBOW_UP_THRESHOLD and current_has_bottom:
                        rep_count += 1
                        if current_is_proper:
                            proper_count += 1

                        # reset for next rep
                        state = "up"
                        current_has_bottom = False
                        current_is_proper = False

        # --------- DRAW TEXT ---------
        y = 30
        cv2.putText(frame, f"Reps: {rep_count}/10", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        y += 30
        cv2.putText(frame, f"Proper reps: {proper_count}", (20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        y += 30
        cv2.putText(frame,f"Time Elapsed: {elapsed}", (20,y),
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,0), 2)
        y+= 30

        if elbow_angle is not None:
            cv2.putText(frame, f"Elbow: {int(elbow_angle)} deg",
                        (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            y += 25
        if back_angle is not None:
            cv2.putText(frame, f"Back: {int(back_angle)} deg",
                        (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            y += 25
        if neck_angle is not None:
            cv2.putText(frame, f"Neck: {int(neck_angle)} deg",
                        (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Push-up Form - Counter & Analysis", frame)

        # stop either at 10 reps or when q is pressed
        if rep_count >= 10:
            break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()

    # --------- FINAL ANALYSIS ---------
print("=== PUSH-UP SESSION RESULT ===")
print(f"Total counted push-ups: {rep_count}")
print(f"Proper push-ups (all 3 checks OK at bottom): {proper_count}")
print(f"Elapsed Time: {elapsed}")
if rep_count > 0:
    percent = proper_count * 100.0 / rep_count
    print(f"Proper form percentage: {percent:.1f}%")
else:
    print("No valid push-ups were counted.")        
