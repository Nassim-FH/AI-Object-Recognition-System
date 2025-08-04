#!/usr/bin/env python3
"""
AI Object Recognition System - Main Entry Point
===============================================

Run this script to analyze all images in the images folder.

Usage:
    python main.py

Author: Nassim FH
Date: August 2025
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from object_recognition import main

if __name__ == "__main__":
    main()
