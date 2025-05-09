import cv2
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calculateAngle(a, b, c):
    """
    Calculate the angle between three points.
    """
    a = np.array(a)  # First
    b = np.array(b)  # Middle
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def classifyPose(landmarks, output_image, display=False):
    '''
    Classifies yoga poses depending on the angles of various body joints.
    Args:
        landmarks: Detected landmarks of the person.
        output_image: Image with the detected pose landmarks drawn.
        display: If True, displays the resultant image with the pose label written on it.
    Returns:
        output_image: Image with the detected pose landmarks drawn and pose label written.
        label: Classified pose label.
    '''

    label = 'Unknown Pose'
    color = (0, 0, 255)  # Color to draw the label

    lm = landmarks.landmark

    # Calculate angles for pose classification
    angles = {
        'left_elbow': calculateAngle(
            (lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y),
            (lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y),
            (lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        ),
        'right_elbow': calculateAngle(
            (lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y),
            (lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y),
            (lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        ),
        'left_shoulder': calculateAngle(
            (lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y),
            (lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y),
            (lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y)
        ),
        'right_shoulder': calculateAngle(
            (lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x, lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y),
            (lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y),
            (lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        ),
        'left_knee': calculateAngle(
            (lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y),
            (lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y),
            (lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
        ),
        'right_knee': calculateAngle(
            (lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x, lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y),
            (lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].y),
            (lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)
        )
    }

    # Pose classification logic
    # Example logic for 10 poses - replicate and adjust for 50 poses

    if 165 < angles['left_elbow'] < 195 and 165 < angles['right_elbow'] < 195:
        if 80 < angles['left_shoulder'] < 110 and 80 < angles['right_shoulder'] < 110:
            if 165 < angles['left_knee'] < 195 or 165 < angles['right_knee'] < 195:
                if 90 < angles['left_knee'] < 120 or 90 < angles['right_knee'] < 120:
                    label = 'Warrior II Pose'
                else:
                    label = 'T Pose'
            else:
                label = 'T Pose'
        else:
            label = 'Unknown Pose'
    elif 165 < angles['left_knee'] < 195 or 165 < angles['right_knee'] < 195:
        if 315 < angles['left_knee'] < 335 or 25 < angles['right_knee'] < 45:
            label = 'Tree Pose'
        else:
            label = 'Unknown Pose'
    elif 170 < angles['left_elbow'] < 190 and 170 < angles['right_elbow'] < 190:
        if 75 < angles['left_shoulder'] < 105 and 75 < angles['right_shoulder'] < 105:
            if 90 < angles['left_knee'] < 130 or 90 < angles['right_knee'] < 130:
                label = 'Downward Dog'
            else:
                label = 'Unknown Pose'
    elif 160 < angles['left_shoulder'] < 200 and 160 < angles['right_shoulder'] < 200:
        if 70 < angles['left_elbow'] < 110 and 70 < angles['right_elbow'] < 110:
            label = 'Plank Pose'
        else:
            label = 'Unknown Pose'
    elif 150 < angles['left_knee'] < 190 and 150 < angles['right_knee'] < 190:
        if 70 < angles['left_shoulder'] < 110 and 70 < angles['right_shoulder'] < 110:
            label = 'Chair Pose'
        else:
            label = 'Unknown Pose'
    elif 140 < angles['left_shoulder'] < 180 and 140 < angles['right_shoulder'] < 180:
        if 110 < angles['left_elbow'] < 150 and 110 < angles['right_elbow'] < 150:
            label = 'Cobra Pose'
        else:
            label = 'Unknown Pose'
    elif 160 < angles['left_knee'] < 200 and 160 < angles['right_knee'] < 200:
        if 60 < angles['left_shoulder'] < 100 and 60 < angles['right_shoulder'] < 100:
            label = 'Bridge Pose'
        else:
            label = 'Unknown Pose'
    elif 150 < angles['left_knee'] < 190 and 150 < angles['right_knee'] < 190:
        if 100 < angles['left_shoulder'] < 140 and 100 < angles['right_shoulder'] < 140:
            label = 'Boat Pose'
        else:
            label = 'Unknown Pose'
    elif 160 < angles['left_elbow'] < 200 and 160 < angles['right_elbow'] < 200:
        if 100 < angles['left_shoulder'] < 140 and 100 < angles['right_shoulder'] < 140:
            label = 'Side Plank Pose'
        else:
            label = 'Unknown Pose'
    elif 150 < angles['left_knee'] < 190 and 150 < angles['right_knee'] < 190:
        if 90 < angles['left_shoulder'] < 130 and 90 < angles['right_shoulder'] < 130:
            label = 'Eagle Pose'
        else:
            label = 'Unknown Pose'
    # Add logic for other poses
    # ...

    # Draw label on the image
    cv2.putText(output_image, label, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 5)

    if display:
        import matplotlib.pyplot as plt
        plt.figure(figsize=[10, 10])
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')
        plt.show()
    else:
        return output_image, label

# Example usage with video capture
