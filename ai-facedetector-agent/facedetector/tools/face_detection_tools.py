"""
Face detection tools using MediaPipe
"""

import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from typing import Dict, List, Any, Union, Tuple
import urllib.request
import math


def download_face_detection_model() -> str:
    """Download the MediaPipe face detection model if not present."""
    model_path = "blaze_face_short_range.tflite"
    
    if not os.path.exists(model_path):
        model_url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
        urllib.request.urlretrieve(model_url, model_path)
        print(f"Downloaded face detection model to {model_path}")
    
    return model_path


def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
    """Converts normalized value pair to pixel coordinates."""
    
    def is_valid_normalized_value(value: float) -> bool:
        return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))
    
    if not (is_valid_normalized_value(normalized_x) and is_valid_normalized_value(normalized_y)):
        return None
    
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px


def detect_faces_in_image(image_path: str) -> Dict[str, Any]:
    """
    Detect faces in an image using MediaPipe face detection.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary with detection results including face count and bounding boxes
    """
    try:
        # Download model if needed
        model_path = download_face_detection_model()
        
        # Create face detector
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceDetectorOptions(base_options=base_options)
        detector = vision.FaceDetector.create_from_options(options)
        
        # Load and process image
        if not os.path.exists(image_path):
            return {"error": f"Image file not found: {image_path}"}
            
        mp_image = mp.Image.create_from_file(image_path)
        detection_result = detector.detect(mp_image)
        
        # Process results
        faces = []
        for detection in detection_result.detections:
            bbox = detection.bounding_box
            category = detection.categories[0] if detection.categories else None
            
            face_info = {
                "bounding_box": {
                    "x": bbox.origin_x,
                    "y": bbox.origin_y, 
                    "width": bbox.width,
                    "height": bbox.height
                },
                "confidence": category.score if category else 0.0,
                "keypoints": []
            }
            
            # Add keypoints if available
            for keypoint in detection.keypoints:
                face_info["keypoints"].append({
                    "x": keypoint.x,
                    "y": keypoint.y
                })
            
            faces.append(face_info)
        
        return {
            "success": True,
            "face_count": len(faces),
            "faces": faces,
            "image_path": image_path
        }
        
    except Exception as e:
        return {"error": f"Face detection failed: {str(e)}"}


def visualize_faces(image_path: str, output_path: str = None) -> Dict[str, Any]:
    """
    Visualize detected faces with bounding boxes and keypoints.
    
    Args:
        image_path: Path to the input image
        output_path: Path to save the annotated image (optional)
        
    Returns:
        Dictionary with visualization results
    """
    try:
        # First detect faces
        detection_result = detect_faces_in_image(image_path)
        
        if "error" in detection_result:
            return detection_result
            
        # Load image for visualization
        image = cv2.imread(image_path)
        if image is None:
            return {"error": f"Could not load image: {image_path}"}
            
        annotated_image = image.copy()
        height, width, _ = image.shape
        
        # Constants for visualization
        MARGIN = 10
        ROW_SIZE = 10
        FONT_SIZE = 1
        FONT_THICKNESS = 1
        TEXT_COLOR = (255, 0, 0)  # Red
        
        # Draw annotations
        for face in detection_result["faces"]:
            bbox = face["bounding_box"]
            
            # Draw bounding box
            start_point = (bbox["x"], bbox["y"])
            end_point = (bbox["x"] + bbox["width"], bbox["y"] + bbox["height"])
            cv2.rectangle(annotated_image, start_point, end_point, TEXT_COLOR, 3)
            
            # Draw keypoints
            for keypoint in face["keypoints"]:
                keypoint_px = _normalized_to_pixel_coordinates(
                    keypoint["x"], keypoint["y"], width, height
                )
                if keypoint_px:
                    cv2.circle(annotated_image, keypoint_px, 2, (0, 255, 0), 2)
            
            # Draw confidence score
            confidence = face["confidence"]
            result_text = f"Face ({confidence:.2f})"
            text_location = (MARGIN + bbox["x"], MARGIN + ROW_SIZE + bbox["y"])
            cv2.putText(annotated_image, result_text, text_location, 
                       cv2.FONT_HERSHEY_PLAIN, FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)
        
        # Save annotated image
        if output_path is None:
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_annotated.jpg"
            
        cv2.imwrite(output_path, annotated_image)
        
        return {
            "success": True,
            "annotated_image_path": output_path,
            "face_count": detection_result["face_count"],
            "message": f"Visualized {detection_result['face_count']} faces and saved to {output_path}"
        }
        
    except Exception as e:
        return {"error": f"Visualization failed: {str(e)}"}


def download_test_image(url: str = None, output_path: str = "test_image.jpg") -> Dict[str, Any]:
    """
    Download a test image for face detection.
    
    Args:
        url: URL of the image to download (uses default if None)
        output_path: Path to save the downloaded image
        
    Returns:
        Dictionary with download results
    """
    try:
        if url is None:
            # Default test image with faces
            url = "https://i.imgur.com/Vu2Nqwb.jpeg"
        
        urllib.request.urlretrieve(url, output_path)
        
        return {
            "success": True,
            "image_path": output_path,
            "message": f"Downloaded test image to {output_path}"
        }
        
    except Exception as e:
        return {"error": f"Failed to download image: {str(e)}"}