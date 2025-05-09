# Yoga Pose Detection & Recommendation System 🧘‍♀️🤖

## Introduction 🌟

Welcome to the Yoga Pose Detection & Recommendation System! This AI-powered project helps users improve their yoga practice by:

Detecting and tracking body poses in real-time with MediaPipe Pose.

Offering feedback on pose accuracy.

Suggesting personalized yoga poses based on weight categories (light, medium, and overweight) for better practice and posture.

Designed for yoga enthusiasts at any level, this system ensures safe and efficient yoga sessions, promoting healthier living!


## Key Features 🚀

1. Pose Classification
   
   Detects human poses using MediaPipe Pose.

   Calculates joint angles to classify various yoga poses.

   Displays detected poses on the input image or video feed.

2. Personalized Yoga Recommendations
   
   Takes the user's weight as input.

   Recommends a set of yoga poses based on the user’s weight category (e.g., lightweight, medium, heavyweight).

   ![project8](https://github.com/user-attachments/assets/6c961c99-08d9-4a67-a7c0-7ef6c24a8d5f)


## How It Works 🔧

1. Pose Detection
   
   The system uses MediaPipe Pose to detect human poses in real-time. This is achieved by analyzing each frame from the webcam (or any video input). MediaPipe 
   provides key body landmarks such as shoulders, elbows, knees, and wrists, which are used to identify the body’s pose.

   Joint Angles Calculation: The system calculates angles between joints (e.g., shoulder-elbow, elbow-wrist, hip-knee) to classify various poses.

    Pose Classification: The system classifies poses based on predefined thresholds for joint angles. For example, the Tree Pose is classified if the angle between 
    the hip, knee, and ankle fits the threshold for that pose.

2. Yoga Pose Recommendation
    The user is asked to input their weight in kilograms.

    Based on the weight input, the system categorizes the user into one of three weight categories: lightweight, medium, or heavyweight.

    For each weight category, a set of yoga poses is recommended:

    Lightweight: Generally more flexible poses like Tadasana, Baddha Konasana.

    Medium Weight: Poses that require moderate flexibility like Vrksasana, Sukhasana.

   Heavyweight: Poses that are easier to hold and focus on stability like Adho Mukha Svanasana, Setu Bandhasana.
   
# System Requirements 💻

1. Python 3.x

2. OpenCV: pip install opencv-python

3. MediaPipe: pip install mediapipe

4. NumPy: pip install numpy

5. ESP32-CAM: A camera module to capture and stream live video.
   

### Contributing 🤝

We welcome contributions from the community! Here are some ways you can help:

Add more poses or improve pose recognition.

Enhance feedback for incorrect poses with improvement tips.

Track progress over time and suggest improvements for your yoga journey.


### Future Enhancements 

Pose Correction Tips: When a pose is incorrect, offer suggestions on how to correct it.

Expanded Pose Categories: Include flexibility, experience level, and other factors to further personalize recommendations.

Yoga Progress Tracking: Track the user’s improvement over time and suggest modifications.


