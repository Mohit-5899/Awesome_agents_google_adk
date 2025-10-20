# AI Face Detector Agent - Google ADK + MediaPipe

A sophisticated face detection agent built with Google ADK (Agent Development Kit) and MediaPipe, providing intelligent face detection and analysis capabilities through natural language interaction.

## Features

- **Advanced Face Detection**: Uses MediaPipe's state-of-the-art BlazeFace model
- **Intelligent Agent**: Google ADK-powered conversational interface
- **Visual Analysis**: Automatic face detection with bounding boxes and keypoints
- **Multiple Input Methods**: Support for local files, URLs, and test images
- **Comprehensive Output**: Detailed analysis with confidence scores and face count
- **Interactive Visualization**: Annotated images showing detection results

## Installation

1. **Clone and Setup**:
```bash
cd /Users/mohitmandawat/Coding/Quanta_AI_Labs\ -\ AI\ Agents/google-adk-agents/ai-facedetector-agent
pip install -r requirements.txt
```

2. **Configure API Key**:
```bash
# Copy the example environment file
cp .env.example .env

# Add your Google API key to .env file
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

## Quick Start

### Basic Usage

```bash
# Detect faces in a local image
python main.py "detect faces in my_image.jpg"

# Download test image and analyze
python main.py "download a test image and detect faces"

# Load image from URL and visualize
python main.py "load image from https://example.com/image.jpg and create visualization"

# Get supported formats
python main.py "what image formats do you support?"
```

### Interactive Examples

```bash
# Default demo (downloads test image and analyzes)
python main.py

# Complex analysis request
python main.py "Download a test image, detect all faces, and create an annotated visualization with confidence scores"

# Multiple step process
python main.py "First check supported formats, then download test image, detect faces and explain the results"
```

## Agent Capabilities

### Core Tools

1. **`detect_faces_in_image`**: Detect faces with MediaPipe
2. **`visualize_faces`**: Create annotated images with bounding boxes
3. **`download_test_image`**: Get sample images for testing
4. **`load_image_from_url`**: Process images from web URLs
5. **`list_supported_formats`**: Show supported image types

### Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Architecture

```
ai-facedetector-agent/
├── facedetector/
│   ├── __init__.py
│   ├── agent.py              # Main ADK agent definition
│   └── tools/
│       ├── __init__.py
│       ├── face_detection_tools.py  # MediaPipe face detection
│       └── file_tools.py           # Image handling utilities
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md              # This file
```

## Technical Details

### Face Detection Model
- **Model**: MediaPipe BlazeFace (short range)
- **Framework**: MediaPipe Tasks for Python
- **Precision**: Float16 optimized
- **Features**: Bounding boxes, keypoints, confidence scores

### ADK Integration
- **Agent Type**: Google ADK Agent with tools
- **Model**: Gemini 2.0 Flash Experimental
- **Tools**: Function calling for face detection operations
- **Interface**: Natural language conversation

## Example Interactions

### 1. Basic Face Detection
```
User: "Detect faces in family_photo.jpg"
Agent: "I'll analyze family_photo.jpg for faces using MediaPipe face detection..."
[Provides detailed analysis with face count and confidence scores]
```

### 2. Complete Analysis Workflow  
```
User: "Download test image and create full analysis"
Agent: "I'll download a test image and perform comprehensive face detection analysis..."
[Downloads image, detects faces, creates visualization, provides detailed report]
```

### 3. URL Processing
```
User: "Load this image URL and tell me how many faces are detected"
Agent: "I'll download the image from the URL and analyze it for faces..."
[Downloads, processes, and provides face count with analysis]
```

## Advanced Usage

### Programmatic Integration

```python
from facedetector import face_detector_agent
from google import genai
from google.genai import types

client = genai.Client(api_key="your_api_key")

response = client.agentic.generate_content(
    model=face_detector_agent.model,
    contents="Detect faces in my_image.jpg and create visualization",
    config=types.GenerateContentConfig(
        agent=face_detector_agent,
        temperature=0.3,
    )
)
```

### Custom Tool Usage

```python
from facedetector.tools import detect_faces_in_image, visualize_faces

# Direct tool usage
result = detect_faces_in_image("my_image.jpg")
print(f"Found {result['face_count']} faces")

# Create visualization
viz_result = visualize_faces("my_image.jpg", "output_annotated.jpg")
```

## Requirements

- Python 3.8+
- Google API Key (AI Studio or Vertex AI)
- Dependencies from requirements.txt:
  - google-adk
  - google-generativeai
  - mediapipe
  - opencv-python
  - numpy
  - pillow
  - python-dotenv

## Troubleshooting

### Common Issues

1. **Missing API Key**:
   ```
   Error: Please set GOOGLE_API_KEY environment variable
   ```
   Solution: Add your API key to .env file or export as environment variable

2. **MediaPipe Model Download**:
   - First run automatically downloads the BlazeFace model
   - Requires internet connection for initial setup

3. **Image Format Issues**:
   - Use supported formats: JPEG, PNG, BMP, TIFF
   - Ensure images are readable and not corrupted

4. **Import Errors**:
   ```bash
   pip install --upgrade google-adk mediapipe opencv-python
   ```

## Contributing

This face detector agent demonstrates:
- Google ADK agent architecture
- MediaPipe integration for computer vision
- Natural language interface for AI tools
- Modular tool design for extensibility

Feel free to extend with additional computer vision capabilities or integrate with other MediaPipe solutions!

## License

Built with Google ADK and MediaPipe. See respective licenses for usage terms.