import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose #Grabbing the pose estimation model from mediapipe library 


#Calculating joint angles using 3 points of reference: the joint and the bones creating the joints
def calculate_joint_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]- b[1], c[0]- b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0/ np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle                             


cap = cv2.VideoCapture(0)

def pose_estimation(cap):
    with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose: #confidence variable relates to accuracy of pose estimation (.5 is recommended)
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection of landmarks
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract body landmarks    
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates of landmarks using OpenCV pose estimation model
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                left_foot = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
                
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                right_foot = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]

                
                # Calculate joint angles bilaterally
                left_shoulder_angle = int(round(calculate_joint_angle(left_hip, left_shoulder, left_elbow), 2))
                left_elbow_angle = int(round(calculate_joint_angle(left_shoulder, left_elbow, left_wrist), 2))
                left_hip_angle = int(round(calculate_joint_angle(left_shoulder, left_hip, left_knee), 2))
                left_knee_angle = int(round(calculate_joint_angle(left_hip, left_knee, left_ankle), 2))
                left_ankle_angle = int(round(calculate_joint_angle(left_knee, left_ankle, left_foot), 2))

                right_elbow_angle = int(round(calculate_joint_angle(right_shoulder, right_elbow, right_wrist), 2))
                right_shoulder_angle = int(round(calculate_joint_angle(right_hip, right_shoulder, right_elbow), 2))
                right_hip_angle = int(round(calculate_joint_angle(right_shoulder, right_hip, right_knee), 2))
                right_knee_angle = int(round(calculate_joint_angle(right_hip, right_knee, right_ankle), 2))
                right_ankle_angle = int(round(calculate_joint_angle(right_knee, right_ankle, right_foot), 2))
            
                # Visualize left-sided joint angles on screen
                cv2.putText(image, str(left_shoulder_angle),
                            tuple(np.multiply(left_shoulder, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
                cv2.putText(image, str(left_elbow_angle),
                            tuple(np.multiply(left_elbow, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
                cv2.putText(image, str(left_hip_angle),
                            tuple(np.multiply(left_hip, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
                cv2.putText(image, str(left_knee_angle),
                            tuple(np.multiply(left_knee, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            )
                cv2.putText(image, str(left_ankle_angle),
                            tuple(np.multiply(left_ankle, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 

                
                # Visualize right-sided joint angles on screen
                cv2.putText(image, str(right_shoulder_angle),
                            tuple(np.multiply(right_shoulder, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
                cv2.putText(image, str(right_elbow_angle),
                            tuple(np.multiply(right_elbow, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
                cv2.putText(image, str(right_hip_angle),
                            tuple(np.multiply(right_hip, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
                cv2.putText(image, str(right_knee_angle),
                            tuple(np.multiply(right_knee, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
                cv2.putText(image, str(right_ankle_angle),
                            tuple(np.multiply(right_ankle, [1920, 1080]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            ) 
            except:
                pass

            # Render detections on screen 
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                            mp_drawing.DrawingSpec(color = (245, 117, 66), thickness =2, circle_radius = 2),
                            mp_drawing.DrawingSpec(color = (245, 66, 230), thickness = 2, circle_radius = 2))
            

            return image



    cap.release()
    cv2.destroyAllWindows()



