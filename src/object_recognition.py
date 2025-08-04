"""
AI Object Recognition System
============================

An intelligent object recognition system using MobileNetV2 deep learning model
to classify and identify objects in images with high accuracy.

Author: Nassim
Date: August 2025
License: MIT
"""

import keras
import numpy as np
import cv2
import os
import glob
from pathlib import Path


class ObjectRecognizer:
    """AI Object Recognition System using MobileNetV2."""
    
    def __init__(self):
        """Initialize the object recognizer with pre-trained model."""
        print("🤖 Initializing AI Object Recognition System...")
        print("📦 Loading MobileNetV2 model...")
        self.model = keras.applications.MobileNetV2(weights='imagenet', include_top=True)
        print("✅ Model loaded successfully!")
        
    def find_images(self, folder_path="../images"):
        """
        Find all image files in the specified folder.
        
        Args:
            folder_path (str): Path to the images folder
            
        Returns:
            list: List of image file paths
        """
        # Get the directory of the current script
        current_dir = Path(__file__).parent
        images_dir = current_dir / folder_path
        
        # Supported image extensions
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.bmp', '*.tiff', '*.tif']
        available_images = []
        
        for extension in image_extensions:
            available_images.extend(images_dir.glob(extension))
            available_images.extend(images_dir.glob(extension.upper()))
        
        # Convert to strings, remove duplicates, and sort
        available_images = list(set([str(img) for img in available_images]))
        available_images.sort()
        
        return available_images
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for model prediction.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            numpy.ndarray: Preprocessed image array
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Preprocess image
        image = cv2.resize(image, (224, 224))
        image = keras.utils.img_to_array(image)
        image = keras.applications.mobilenet_v2.preprocess_input(image)
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        
        return image
    
    def predict_image(self, image_array, top_k=5):
        """
        Make prediction on preprocessed image.
        
        Args:
            image_array (numpy.ndarray): Preprocessed image array
            top_k (int): Number of top predictions to return
            
        Returns:
            list: Top predictions with labels and confidence scores
        """
        predictions = self.model.predict(image_array, verbose=0)
        decoded_predictions = keras.applications.mobilenet_v2.decode_predictions(
            predictions, top=top_k
        )
        return decoded_predictions[0]
    
    def analyze_single_image(self, image_path, top_k=5):
        """
        Analyze a single image and return predictions.
        
        Args:
            image_path (str): Path to the image file
            top_k (int): Number of top predictions to return
            
        Returns:
            tuple: (image_name, predictions) or (image_name, None) if error
        """
        image_name = Path(image_path).name
        
        try:
            # Preprocess image
            image_array = self.preprocess_image(image_path)
            
            # Make prediction
            predictions = self.predict_image(image_array, top_k)
            
            return image_name, predictions
            
        except Exception as e:
            print(f"❌ Error processing {image_name}: {str(e)}")
            return image_name, None
    
    def analyze_all_images(self, images_folder="../images", top_k=5):
        """
        Analyze all images in the specified folder.
        
        Args:
            images_folder (str): Path to the images folder
            top_k (int): Number of top predictions to return
        """
        # Find all images
        available_images = self.find_images(images_folder)
        
        if not available_images:
            print("❌ No images found in the folder!")
            return
        
        print(f"🗂️  Found {len(available_images)} image(s)")
        print("=" * 80)
        
        # Process each image
        for image_index, image_path in enumerate(available_images, 1):
            image_name, predictions = self.analyze_single_image(image_path, top_k)
            
            print(f"\n📸 Image {image_index}/{len(available_images)}: {image_name}")
            print("-" * 80)
            
            if predictions is None:
                continue
            
            print("⏳ Analysis complete!")
            print("📊 Top predictions:")
            
            for i, (class_id, label, score) in enumerate(predictions, 1):
                confidence = score * 100
                # Add emoji based on confidence level
                if confidence > 70:
                    emoji = "🎯"
                elif confidence > 50:
                    emoji = "✅"
                elif confidence > 30:
                    emoji = "⚠️"
                else:
                    emoji = "❓"
                
                print(f"   {emoji} {i}. {label.replace('_', ' ').title()}: {score:.4f} ({confidence:.2f}%)")
        
        print("\n" + "=" * 80)
        print(f"🎉 Analysis complete! Processed {len(available_images)} image(s) successfully!")


def main():
    """Main function to run the object recognition system."""
    print("🚀 Starting AI Object Recognition System")
    print("=" * 80)
    
    try:
        # Initialize the recognizer
        recognizer = ObjectRecognizer()
        
        # Analyze all images
        recognizer.analyze_all_images()
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
    finally:
        print("\n🔚 Thank you for using AI Object Recognition System!")


if __name__ == "__main__":
    main()
