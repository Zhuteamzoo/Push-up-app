# Push-Up Alarm App — Requirements (RQ)

## 1. Purpose

The Push-Up Alarm App is designed to prevent passive alarm dismissal by requiring the user to complete a short physical activity (push-ups) before the alarm can be turned off. The system prioritizes **reliability and correctness** to ensure the alarm cannot be dismissed unintentionally.

---

## 2. Functional Requirements

### FR-1 Alarm Lock
- The alarm **must not be dismissible** until the required number of valid push-ups is completed.
- The user may optionally snooze the alarm **only after completing a partial requirement**.

### FR-2 Pose Detection
- The system must use **MediaPipe Pose** to detect body landmarks in real time.
- At minimum, the following landmarks must be tracked:
  - Shoulder
  - Elbow
  - Wrist
  - Hip
  - Ankle
  - Head/neck reference points

### FR-3 Skeleton Construction
- The system must construct a simplified posture model by connecting detected landmarks into line segments.
- These segments will be used for posture and motion analysis.

### FR-4 Push-Up Motion Detection
- A push-up must be detected using the **elbow angle (shoulder–elbow–wrist)**.
- A valid push-up must follow a complete motion cycle:
  - Extended (up position)
  - Bent (down position)
  - Extended (return to up position)

### FR-5 Depth Requirement
- The elbow angle must pass a predefined **minimum bend threshold** to prevent partial or shallow movements from being counted.

### FR-6 Form Validation
A push-up is considered valid **only if all conditions below are met**:
1. Complete motion cycle is detected  
2. Back remains approximately straight (torso alignment within threshold)  
3. Neck remains aligned (no significant tilt or collapse)

### FR-7 Rep Counting
- Push-ups must be counted using a **state-based system** to prevent double counting.
- A push-up is counted only after a full valid cycle is completed.

### FR-8 Quality Scoring
- The system must track:
  - Total push-ups attempted
  - Number of valid (“good”) push-ups
- Only valid push-ups contribute toward unlocking the alarm.

---

## 3. Non-Functional Requirements

### NFR-1 Reliability
- The system should prioritize **false negatives over false positives**.
- It is acceptable to miss a rep; it is not acceptable to unlock incorrectly.

### NFR-2 Robustness
- If pose landmarks are not reliably detected, push-up counting must pause.
- Sudden loss of body visibility should invalidate the current rep.

### NFR-3 Performance
- Pose detection and analysis must operate in real time with minimal latency.
- The system must respond quickly enough to track continuous motion.

### NFR-4 Usability
- The interface should clearly display:
  - Number of valid push-ups completed
  - Remaining push-ups required
- Feedback should be simple and non-distracting during alarm operation.

---

## 4. Constraints

- The system must rely on **camera-based pose estimation only** (no external sensors).
- The app must function under varying lighting conditions within reasonable limits.
- The project is implemented incrementally and may not initially support user accounts.

---

## 5. Assumptions

- The users full body is visible
- The camera is facing the left side of the user

---

## 6. Future Extensions (Out of Scope)

- User accounts and authentication
- Personalized difficulty calibration
- Support for additional exercises
- Cloud-based data storage
