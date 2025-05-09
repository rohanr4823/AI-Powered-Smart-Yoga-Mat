import cv2
import mediapipe as mp
from pose_utilis import classifyPose

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def detectPose(image, pose):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return image, results.pose_landmarks

def main():
    url = 'http://172.20.10.14:81/stream'  # Ensure the URL is correct
    cap = cv2.VideoCapture(url)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Detect pose
        output_frame, landmarks = detectPose(frame, pose)

        if landmarks:
            output_frame, label = classifyPose(landmarks, output_frame, display=False)
            cv2.putText(output_frame, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Pose Detection', output_frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
