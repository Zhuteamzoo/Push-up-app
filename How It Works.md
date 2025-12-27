## Push-Up Detection Logic (Computer Vision)

The app uses **MediaPipe Pose** to detect body landmarks in real time (e.g., shoulder, elbow, wrist, hip, ankle, and key head/neck points). Using these landmarks, the program constructs a simplified “skeleton” by connecting relevant joints.

### 1) Build a posture model
From the detected landmarks, the app forms line segments (e.g., shoulder→elbow→wrist, shoulder→hip, hip→ankle). These lines are used to analyze posture and movement over time.

### 2) Evaluate form using joint angles
The program calculates angles between connected segments to check push-up quality, including:
- **Elbow angle (shoulder–elbow–wrist):** used to detect the push-up motion
- **Back alignment:** checks that the torso remains relatively straight
- **Neck alignment:** checks that the head/neck is not significantly tilted or “crooked”

### 3) Count a push-up only when form + motion are valid
A push-up is counted only if all three conditions are met:

1. **Complete movement cycle:** the elbow angle moves from a “resting/extended” state → to a “bent” state → back to extended  
2. **Back stays straight:** torso alignment remains within an acceptable range  
3. **Neck stays aligned:** the head/neck does not significantly deviate from neutral alignment  

### 4) Score push-up quality
The app tracks:
- **Total push-ups attempted**
- **Number of “good” push-ups** (meeting all conditions)

It then computes the user’s **good push-up rate** (good / total), which can be used to determine whether the alarm can be dismissed.
