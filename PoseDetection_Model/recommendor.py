import cv2
import mediapipe as mp
import time
import math

# Get weight input first, before initializing other components
try:
    weight = float(input("Enter your weight in kilograms: "))
except ValueError:
    print("Invalid weight input. Please enter a numeric value.")
    exit()
4
# Proceed with the rest of the imports and initialization
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Define reference points for each pose
pose_references = {
    "Tadasana (Mountain Pose)": [
        (0.5, 0.9),  # Hip
        (0.5, 0.7),  # Shoulder
        (0.5, 0.5),  # Knee
        (0.5, 0.3),  # Ankle
    ],
    "Baddha Konasana (Bound Angle Pose)": [
        (0.5, 0.7),  # Hip
        (0.5, 0.6),  # Shoulder
        (0.5, 0.5),  # Knee
        (0.5, 0.4),  # Ankle
    ],
    "Marjaryasana-Bitilasana (Cat-Cow Pose)": [
        (0.5, 0.6),  # Hip
        (0.5, 0.5),  # Shoulder
        (0.5, 0.4),  # Knee
        (0.5, 0.3),  # Ankle
    ],
    "Balasana (Child’s Pose)": [
        (0.5, 0.9),  # Hip
        (0.6, 0.7),  # Shoulder
        (0.5, 0.6),  # Knee
        (0.5, 0.4),  # Ankle
    ],
    "Setu Bandhasana (Bridge Pose)": [
        (0.5, 0.8),  # Hip
        (0.6, 0.5),  # Shoulder
        (0.5, 0.4),  # Knee
        (0.6, 0.3),  # Ankle
    ],
    "Vrksasana (Tree Pose)": [
        (0.5, 0.9),  # Standing Hip
        (0.5, 0.7),  # Standing Shoulder
        (0.6, 0.5),  # Bent Knee
        (0.5, 0.3),  # Standing Ankle
        (0.5, 0.2)  # Top of the head
    ],
    "Virabhadrasana I (Warrior I Pose)": [
        (0.5, 0.9),  # Front Hip
        (0.6, 0.7),  # Front Shoulder
        (0.6, 0.5),  # Front Knee
        (0.6, 0.3),  # Front Ankle
        (0.5, 0.2)  # Top of the head
    ],
    "Adho Mukha Svanasana (Downward-Facing Dog)": [
        (0.5, 0.7),  # Hip
        (0.5, 0.5),  # Shoulder
        (0.5, 0.4),  # Knee
        (0.5, 0.3),  # Ankle
        (0.5, 0.2)  # Top of the head
    ],
    "Sukhasana (Easy Pose)": [
        (0.5, 0.8),  # Hip
        (0.5, 0.6),  # Shoulder
        (0.5, 0.5),  # Knee
        (0.5, 0.4),  # Ankle
        (0.5, 0.2)  # Top of the head
    ]
}

def get_yoga_recommendations(weight_category):
    recommendations = {
        'lightweight': [
            "Tadasana (Mountain Pose)",
            "Baddha Konasana (Bound Angle Pose)",
            "Marjaryasana-Bitilasana (Cat-Cow Pose)"
        ],
        'medium_weight': [
            "Balasana (Child’s Pose)",
            "Setu Bandhasana (Bridge Pose)",
            "Tadasana (Mountain Pose)"
        ],
        'overweight': [
            "Balasana (Child’s Pose)",
            "Baddha Konasana (Bound Angle Pose)",
            "Setu Bandhasana (Bridge Pose)"
        ]
    }
    return recommendations.get(weight_category, [])

def classify_weight_category(weight):
    if weight < 60:
        return 'lightweight'
    elif 60 <= weight < 80:
        return 'medium_weight'
    else:
        return 'overweight'

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def is_pose_correct(landmarks, pose_name):
    if pose_name not in pose_references:
        return False

    pose_reference = pose_references[pose_name]
    landmark_coords = [(landmarks[i].x, landmarks[i].y) for i in range(len(landmarks))]

    pose_landmarks = {
        'Hip': mp_pose.PoseLandmark.LEFT_HIP.value,
        'Shoulder': mp_pose.PoseLandmark.LEFT_SHOULDER.value,
        'Knee': mp_pose.PoseLandmark.LEFT_KNEE.value,
        'Ankle': mp_pose.PoseLandmark.LEFT_ANKLE.value,
    }

    pose_landmark_positions = [landmark_coords[pose_landmarks[name]] for name in pose_landmarks]

    for ref_pos, actual_pos in zip(pose_reference, pose_landmark_positions):
        distance = calculate_distance(ref_pos, actual_pos)
        if not (0.8 <= distance <= 1.2):  # Allowable range
            return False

    return True

def show_pose(cap, pose_name):
    start_time = time.time()
    duration = 30  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if is_pose_correct(results.pose_landmarks.landmark, pose_name):
                cv2.putText(frame, "Correct Pose!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Display pose instructions and timer countdown
            elapsed_time = time.time() - start_time
            remaining_time = max(0, duration - int(elapsed_time))
            cv2.putText(frame, f"Perform {pose_name} - Time Left: {remaining_time}s", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2, cv2.LINE_AA)

            if remaining_time == 0:
                break

        cv2.imshow('Yoga Pose Recommendation', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

def main(weight):
    # Use the ESP32-CAM stream URL instead of the laptop camera
    cap = cv2.VideoCapture('http://172.20.10.14:81/stream')  # Replace with your ESP32-CAM IP address
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    weight_category = classify_weight_category(weight)
    yoga_recommendations = get_yoga_recommendations(weight_category)

    if not yoga_recommendations:
        print("No yoga recommendations available. Exiting...")
        cap.release()
        cv2.destroyAllWindows()
        return

    print(f"Recommended Yoga Poses for {weight_category} category:")
    for idx, pose in enumerate(yoga_recommendations, 1):
        print(f"{idx}. {pose}")

    for pose in yoga_recommendations:
        print(f"\nPerforming pose: {pose}")
        show_pose(cap, pose)

    cap.release()
    cv2.destroyAllWindows()

# Call main function
main(weight)
