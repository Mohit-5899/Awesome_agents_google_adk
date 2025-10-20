"""
Face Detector Agent - Main entry point
Run face detection analysis using Google ADK and MediaPipe
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from google import genai
from google.genai import types
from facedetector.agent import face_detector_agent

load_dotenv()


def run_face_detection(query: str):
    """
    Run face detection analysis using the ADK agent
    
    Args:
        query: User query for face detection task
    """
    print(f"\n{'='*80}")
    print(f"AI Face Detector Agent - Google ADK + MediaPipe")
    print(f"{'='*80}")
    print(f"Query: {query}")
    print(f"{'='*80}\n")
    
    # Initialize client
    client = genai.Client(
        vertexai=False,
        api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    )
    
    print("Processing your face detection request...")
    print(f"Query: {query}\n")
    
    # Generate response using the face detector agent
    response = client.agentic.generate_content(
        model=face_detector_agent.model,
        contents=query,
        config=types.GenerateContentConfig(
            agent=face_detector_agent,
            temperature=0.3,
        )
    )
    
    print("\n" + "="*80)
    print("FACE DETECTION ANALYSIS COMPLETE")
    print("="*80 + "\n")
    
    # Print the response
    for part in response.candidates[0].content.parts:
        print(part.text)
    
    return response


def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI Face Detector Agent - Google ADK + MediaPipe"
    )
    parser.add_argument(
        "query",
        type=str,
        nargs="*",
        default=["Download a test image and detect faces in it"],
        help="Face detection query (e.g., 'detect faces in image.jpg', 'download test image and analyze')"
    )
    
    args = parser.parse_args()
    
    # Join query parts if multiple arguments
    query = " ".join(args.query) if args.query else "Download a test image and detect faces in it"
    
    # Check for required API key
    if not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
        print("Error: Please set GOOGLE_API_KEY or GEMINI_API_KEY environment variable")
        print("You can get an API key from: https://aistudio.google.com/app/apikey")
        print("Then add it to a .env file or export as environment variable")
        sys.exit(1)
    
    run_face_detection(query)


if __name__ == "__main__":
    main()