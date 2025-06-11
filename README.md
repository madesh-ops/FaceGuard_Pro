# IdleSecure

IdleSecure is an intelligent screen security solution that automatically locks your Windows workstation when you're away from your computer, using real-time face detection and monitoring.

## Key Features

- **Real-time Face Detection**: Utilizes MediaPipe's Face Mesh for accurate and robust face detection
- **Automated Screen Lock**: Automatically secures your workstation when no face is detected
- **Professional Dashboard**: Modern, real-time monitoring interface showing detection and lock status
- **Low Resource Usage**: Optimized performance with minimal system impact
- **Privacy-Focused**: All processing happens locally on your machine

## Technical Details

- Built with Python, OpenCV, and MediaPipe
- Modern Tkinter-based dashboard with a sleek dark theme
- Multi-threaded architecture for smooth performance
- Configurable face detection threshold

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- Windows OS (for system lock functionality)

## Getting Started

1. Clone this repository
2. Install dependencies:
   ```
   pip install opencv-python mediapipe
   ```
3. Run the application:
   ```
   python testing.py
   ```


