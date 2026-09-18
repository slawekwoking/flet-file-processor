#!/bin/bash
# Quick build script for Flet Android APK
# Usage: ./build_apk.sh [debug|release]

set -e

BUILD_TYPE=${1:-debug}
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Flet Android APK Builder"
echo "=========================================="
echo "Project: $PROJECT_DIR"
echo "Build type: $BUILD_TYPE"
echo ""

# Check for flet
if ! command -v flet &> /dev/null; then
    echo "ERROR: 'flet' command not found"
    echo "Install with: pip install flet[build]"
    exit 1
fi

# Check for Android SDK
if [ -z "$ANDROID_HOME" ] || [ ! -d "$ANDROID_HOME" ]; then
    echo "ERROR: ANDROID_HOME not set or invalid"
    echo "Please set up Android SDK first (see BUILD_INSTRUCTIONS.md)"
    exit 1
fi

echo "Android SDK: $ANDROID_HOME"
echo ""

cd "$PROJECT_DIR"

# Build command
BUILD_CMD="flet build apk \
    --project-name \"FileProcessor\" \
    --org \"com.example.fileprocessor\" \
    --description \"Cross-platform file processing application built with Flet\" \
    --version \"1.0.0\" \
    --build-number 1 \
    --permissions INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO \
    main.py"

if [ "$BUILD_TYPE" = "release" ]; then
    BUILD_CMD="$BUILD_CMD --release"
fi

echo "Running build command..."
echo "$BUILD_CMD"
echo ""

eval $BUILD_CMD

echo ""
echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="

if [ "$BUILD_TYPE" = "release" ]; then
    APK_PATH="build/apk/app-release.apk"
else
    APK_PATH="build/apk/app-debug.apk"
fi

if [ -f "$APK_PATH" ]; then
    echo "APK location: $PROJECT_DIR/$APK_PATH"
    echo "Size: $(du -h "$APK_PATH" | cut -f1)"
    echo ""
    echo "To install on device:"
    echo "  adb install $APK_PATH"
    echo ""
    echo "Or copy to device and install via file manager:"
    echo "  cp $APK_PATH /sdcard/Download/"
else
    echo "WARNING: APK not found at expected location"
    echo "Check build output above for actual location"
fi