# Flet Android APK Build Instructions

This guide provides complete step-by-step instructions for building a Flet Python application into an Android APK (.apk) file using command-line tools.

## Prerequisites

- **Termux** (Android) or **Parrot OS / Kali Linux** (Desktop Linux)
- Internet connection for downloading dependencies
- Minimum 2GB free storage space
- Python 3.8+ installed

---

## Option 1: Building in Termux (On Android Device)

### Step 1: Install Termux and Setup

```bash
# Install Termux from F-Droid (recommended) or GitHub releases
# Do NOT use Google Play version (outdated)

# Open Termux and run:
pkg update && pkg upgrade -y

# Install required packages
pkg install -y python git wget curl unzip openjdk-17 gradle

# Verify installations
python --version  # Should be 3.10+
java --version    # Should be 17+
gradle --version  # Should be 7.5+
```

### Step 2: Install Android SDK (Required for APK building)

```bash
# Create Android SDK directory
mkdir -p $HOME/android-sdk
cd $HOME/android-sdk

# Download command line tools
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
unzip commandlinetools-linux-11076708_latest.zip -d cmdline-tools
mv cmdline-tools/cmdline-tools cmdline-tools/latest
rm commandlinetools-linux-11076708_latest.zip

# Set environment variables (add to ~/.bashrc or ~/.zshrc)
cat >> ~/.bashrc << 'EOF'
export ANDROID_HOME=$HOME/android-sdk
export ANDROID_SDK_ROOT=$HOME/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
EOF

source ~/.bashrc

# Accept licenses and install required components
yes | sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0" "ndk;26.1.10909125"
```

### Step 3: Install Flet and Build Dependencies

```bash
# Install Flet with build support
pip install --upgrade pip
pip install flet[build]

# Verify flet build command is available
flet --version
```

### Step 4: Prepare Your Project

```bash
# Navigate to your project directory
cd /data/data/com.termux/files/home/flet_app

# Install project dependencies
pip install -r requirements.txt

# Test run on desktop (optional)
flet run main.py
```

### Step 5: Build the APK

```bash
# Build APK (this will take 5-15 minutes on first run)
flet build apk \
    --project-name "FileProcessor" \
    --org "com.example" \
    --description "File processing application built with Flet" \
    --version "1.0.0" \
    --build-number 1 \
    --icon assets/icon.png \
    --splash assets/splash.png \
    --permissions INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE \
    main.py
```

**Output location:** `build/apk/app-release.apk`

### Step 6: Install and Test

```bash
# Install on device (requires USB debugging or file transfer)
adb install build/apk/app-release.apk

# Or copy to shared storage and install via file manager
cp build/apk/app-release.apk /sdcard/Download/
```

---

## Option 2: Building on Desktop Linux (Parrot OS / Kali Linux)

### Step 1: System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y \
    python3 python3-pip python3-venv \
    git wget curl unzip \
    openjdk-17-jdk \
    gradle \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-glx \
    libgtk-3-0 libwebkit2gtk-4.0-37

# Verify installations
python3 --version
java --version
gradle --version
```

### Step 2: Install Android SDK

```bash
# Create Android SDK directory
mkdir -p $HOME/android-sdk
cd $HOME/android-sdk

# Download command line tools
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
unzip commandlinetools-linux-11076708_latest.zip -d cmdline-tools
mv cmdline-tools/cmdline-tools cmdline-tools/latest
rm commandlinetools-linux-11076708_latest.zip

# Set environment variables
cat >> ~/.bashrc << 'EOF'
export ANDROID_HOME=$HOME/android-sdk
export ANDROID_SDK_ROOT=$HOME/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
EOF

source ~/.bashrc

# Install SDK components
yes | sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0" "ndk;26.1.10909125"
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create and activate virtual environment
python3 -m venv flet-env
source flet-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Flet with build support
pip install flet[build]
```

### Step 4: Build the APK

```bash
# Navigate to project
cd /path/to/flet_app

# Install dependencies
pip install -r requirements.txt

# Build APK
flet build apk \
    --project-name "FileProcessor" \
    --org "com.example.fileprocessor" \
    --description "Cross-platform file processing application" \
    --version "1.0.0" \
    --build-number 1 \
    --permissions INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO \
    main.py
```

### Step 5: Test on Desktop (Linux)

```bash
# Run natively on Linux desktop
flet run main.py

# Or run as packaged app
flet pack main.py --name FileProcessor --icon assets/icon.png
```

---

## Option 3: Using Buildozer Directly (Advanced)

If you need more control over the build process:

### Step 1: Install Buildozer Dependencies

```bash
# Ubuntu/Debian/Parrot/Kali
sudo apt install -y \
    git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    build-essential ccache

# Termux
pkg install -y git zip unzip openjdk-17 python autoconf libtool pkg-config \
    zlib-dev ncurses-dev cmake libffi-dev openssl-dev build-essential ccache
```

### Step 2: Install Buildozer

```bash
pip install --upgrade buildozer
```

### Step 3: Initialize Buildozer Config

```bash
cd /data/data/com.termux/files/home/flet_app
buildozer init
```

### Step 4: Configure buildozer.spec

Edit `buildozer.spec` with these key settings:

```ini
[app]
title = File Processor
package.name = fileprocessor
package.domain = com.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md
version = 1.0.0
requirements = python3,flet
orientation = portrait
osx.sdk_path = 
osx.arch = 
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO
android.api = 34
android.minapi = 24
android.ndk = 26b
android.gradle_dependencies = 
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
```

### Step 5: Build with Buildozer

```bash
# Debug build
buildozer -v android debug

# Release build (requires keystore)
buildozer -v android release
```

---

## Android Sandbox Compliance & Permissions

### How Flet Handles Android Sandbox

Flet applications run within the **standard Android application sandbox** - no root access required:

1. **Process Isolation**: Each app runs in its own Linux process with unique UID
2. **File System Access**: 
   - Internal storage: `/data/user/0/com.example.fileprocessor/` (private, no permissions needed)
   - External storage: Requires `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE` (legacy) or MediaStore API (Android 10+)
   - Scoped Storage: Android 11+ enforces scoped storage - apps see only their own files

3. **Flet's Permission Handling**:
   ```python
   # In your Python code, use Flet's FilePicker which handles permissions automatically
   file_picker = ft.FilePicker(on_result=on_file_picked)
   page.overlay.append(file_picker)
   
   # Request file access - Flet handles runtime permissions
   file_picker.pick_files(allowed_extensions=["txt", "json"])
   ```

4. **No `su` Required**: Flet uses standard Android APIs:
   - `ActivityResultContracts` for file picking
   - `MediaStore` for media access
   - `StorageManager` for storage volumes
   - All handled by Flutter engine (Flet's backend)

### Required Permissions Explained

| Permission | Purpose | Android Version |
|------------|---------|-----------------|
| `INTERNET` | Network access (if needed) | All |
| `READ_EXTERNAL_STORAGE` | Read files from shared storage | ≤ Android 12 |
| `WRITE_EXTERNAL_STORAGE` | Write files to shared storage | ≤ Android 12 |
| `READ_MEDIA_IMAGES` | Read images (scoped storage) | Android 13+ |
| `READ_MEDIA_VIDEO` | Read videos (scoped storage) | Android 13+ |
| `READ_MEDIA_AUDIO` | Read audio (scoped storage) | Android 13+ |

### Best Practices for Sandbox Compliance

1. **Use FilePicker**: Always use `ft.FilePicker()` - it uses system document picker
2. **Internal Storage First**: Save app data to `page.client_storage` or app-specific directory
3. **No Direct Path Access**: Don't hardcode `/sdcard/` paths
4. **Handle Permission Denial**: Gracefully handle when user denies permission

```python
# Example: Proper file handling in Flet
def save_file(self, content: str):
    # Use client storage for app data (no permissions needed)
    self.page.client_storage.set("last_content", content)
    
    # For user-visible files, use FilePicker save dialog
    self.file_picker.save_file(
        dialog_title="Save processed file",
        file_name="processed_output.txt",
        allowed_extensions=["txt"]
    )
```

---

## Troubleshooting

### Common Issues

**1. "NDK not found"**
```bash
# Install NDK
sdkmanager "ndk;26.1.10909125"
# Or set path manually
export ANDROID_NDK_HOME=$ANDROID_HOME/ndk/26.1.10909125
```

**2. "Gradle build failed"**
```bash
# Clean and retry
cd build/android
./gradlew clean
cd ../..
flet build apk ...
```

**3. "Java version mismatch"**
```bash
# Ensure Java 17
sudo update-alternatives --config java
# Select Java 17
```

**4. "Out of memory" during build**
```bash
# Increase Gradle memory
export GRADLE_OPTS="-Xmx4g -XX:MaxMetaspaceSize=1g"
```

**5. Termux: "Permission denied" on APK install**
```bash
# Enable "Install unknown apps" for Termux in Android settings
# Or use adb
adb install build/apk/app-release.apk
```

---

## Quick Reference Card

### Termux One-Liner Setup
```bash
pkg update && pkg install -y python git wget unzip openjdk-17 gradle && \
mkdir -p $HOME/android-sdk && cd $HOME/android-sdk && \
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && \
unzip commandlinetools-linux-11076708_latest.zip -d cmdline-tools && \
mv cmdline-tools/cmdline-tools cmdline-tools/latest && \
echo 'export ANDROID_HOME=$HOME/android-sdk' >> ~/.bashrc && \
echo 'export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools' >> ~/.bashrc && \
source ~/.bashrc && \
yes | sdkmanager --licenses && \
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0" "ndk;26.1.10909125" && \
pip install flet[build]
```

### Build Command Template
```bash
flet build apk \
    --project-name "YourAppName" \
    --org "com.yourdomain" \
    --version "1.0.0" \
    --build-number 1 \
    --permissions INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE \
    main.py
```

### Output Locations
- **Debug APK**: `build/apk/app-debug.apk`
- **Release APK**: `build/apk/app-release.apk`
- **AAB (Play Store)**: `build/app/build/outputs/bundle/release/app-release.aab`

---

## Additional Resources

- [Flet Documentation](https://flet.dev/docs/)
- [Flet Build Commands](https://flet.dev/docs/publish/android/)
- [Android Storage Guide](https://developer.android.com/training/data-storage)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)

---

## File Structure Summary

```
flet_app/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── assets/
│   ├── icon.png         # App icon (512x512 recommended)
│   └── splash.png       # Splash screen (optional)
└── BUILD_INSTRUCTIONS.md # This file
```

Create `assets/icon.png` (512x512 PNG) for a proper app icon. The build will use a default icon if not provided.