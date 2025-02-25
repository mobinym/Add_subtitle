# 🎬 Video Subtitle Adder with Audio Sync  
Easily add Persian and English subtitles to your videos with precise timing and audio synchronization.

---

## 🌟 Key Features  
- **Persian (RTL) Subtitle Support** – Proper alignment and display.  
- **SRT File Parsing** – Accurate timing and text extraction.  
- **Automatic Line Breaking** – For optimal subtitle display.  
- **Audio Merging** – Combines video with external audio file.  
- **High-Quality Output** – MP4 format with preserved resolution and FPS.  

---

## ⚙️ Installation  
Ensure you have the required libraries installed:  
```
pip install opencv-python-headless numpy pillow arabic_reshaper bidi pydub
```

### ⚠️ FFmpeg Requirement  
This project requires **FFmpeg** for audio processing:  
- **macOS/Linux:**  
    ```
    brew install ffmpeg
    ```
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org) and add to the system PATH.

---

## 🚀 Quick Start  
1. **Prepare Your Files:**  
   - Video: `short-clip.mp4`  
   - Subtitles: `subtitle.srt` (UTF-8 encoded)  
   - Audio: `final.mp3`  

2. **Add Subtitles:**  
```
add_subtitles_with_opencv("short-clip.mp4", "subtitle.srt", "output_video.mp4", font_path='/Library/Fonts/Arial.ttf')
```

3. **Merge Audio:**  
```
add_audio_to_video("output_video.mp4", "final.mp3", "final_output.mp4")
```

Your final video with synchronized subtitles and audio will be saved as `final_output.mp4`.

---

## 🎨 Customization Options  
- **Font Style:** Change the `font_path` to use different fonts.  
- **Font Size:** Adjust `font_size` as per your preference.  
- **Positioning:** Modify `x` and `y` values for precise subtitle placement.  

---

## 📝 Supported SRT Format  
```
1  
00:00:01,000 --> 00:00:04,000  
This is the first subtitle line.  

2  
00:00:05,000 --> 00:00:07,000  
Here is another line of text.  
```

---

## 🛠 Troubleshooting  
- **Subtitles Not Displaying?**  
    - Check the font path and make sure it supports Persian characters.  
    - Confirm your SRT file is UTF-8 encoded.  
- **Audio Sync Issues?**  
    - Ensure the FPS of the original video and audio match.  
- **FFmpeg Not Found?**  
    - Ensure FFmpeg is correctly installed and added to the system PATH.

---

## ❤️ Support  
Found this project useful? Give it a ⭐ to show your support!  

---
