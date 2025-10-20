"""
File handling tools for the face detector agent
"""

import cv2
import numpy as np
import urllib.request
from typing import Dict, Any


def save_image(image_data: np.ndarray, output_path: str) -> Dict[str, Any]:
    """
    Save an image array to file.
    
    Args:
        image_data: Image data as numpy array
        output_path: Path to save the image
        
    Returns:
        Dictionary with save results
    """
    try:
        cv2.imwrite(output_path, image_data)
        return {
            "success": True,
            "output_path": output_path,
            "message": f"Image saved to {output_path}"
        }
    except Exception as e:
        return {"error": f"Failed to save image: {str(e)}"}


def load_image_from_url(url: str, output_path: str = None) -> Dict[str, Any]:
    """
    Download and load an image from a URL.
    
    Args:
        url: URL of the image to download
        output_path: Local path to save the image (optional)
        
    Returns:
        Dictionary with load results and image path
    """
    try:
        if output_path is None:
            # Generate filename from URL
            filename = url.split("/")[-1]
            if not filename or "." not in filename:
                filename = "downloaded_image.jpg"
            output_path = filename
        
        # Download the image
        urllib.request.urlretrieve(url, output_path)
        
        # Verify the image can be loaded
        image = cv2.imread(output_path)
        if image is None:
            return {"error": f"Downloaded file is not a valid image: {output_path}"}
        
        return {
            "success": True,
            "image_path": output_path,
            "image_shape": image.shape,
            "message": f"Successfully downloaded and loaded image from {url}"
        }
        
    except Exception as e:
        return {"error": f"Failed to load image from URL: {str(e)}"}


def list_supported_formats() -> Dict[str, Any]:
    """
    List supported image formats for face detection.
    
    Returns:
        Dictionary with supported formats
    """
    return {
        "supported_formats": [
            ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"
        ],
        "recommended_format": ".jpg",
        "message": "Face detection works best with clear, well-lit images containing visible faces"
    }