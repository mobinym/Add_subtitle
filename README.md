```markdown
# 🎥 **Video Subtitle Adder with Audio Sync**  
This project allows you to accurately add Persian and English subtitles to videos and seamlessly merge the original audio back into the final output!

---

## 🔥 **Features**  
- **Supports Persian and Right-to-Left (RTL) Subtitles** using `arabic_reshaper` and `bidi`.
- **Automatic Line Breaking** for better subtitle display.
- **SRT Compatibility** for reading subtitle timing and text.
- **Audio Merging** with OpenCV and Pydub.
- **High-Quality Video Output** in MP4 format.

---

## 📂 **Prerequisites**  
First, install the required libraries:
```bash
pip install opencv-python-headless numpy pillow arabic_reshaper bidi pydub
```

**Note:**  
- Pydub requires **FFmpeg** to be installed.
- On macOS or Linux, use Homebrew:
    ```bash
    brew install ffmpeg
    ```
- On Windows, download **FFmpeg** from the [official website](https://ffmpeg.org) and add it to the system PATH.

---

## 🚀 **How to Use**  

1. **Place Video and Subtitle Files:**  
   - Put the original video named `short-clip.mp4` in the project folder.
   - Place the subtitle file as `subtitle.srt` in the same directory.
   - Include the separate audio file named `final.mp3` in the project folder.

2. **Run the Script:**  
   ```python
   add_subtitles_with_opencv("short-clip.mp4", "subtitle.srt", "output_video.mp4", font_path='/Library/Fonts/Arial.ttf')
   add_audio_to_video("output_video.mp4", "final.mp3", "final_output.mp4")
   ```
   - Subtitles are added to the video and saved as `output_video.mp4`.
   - The original audio is merged, and the final output is saved as `final_output.mp4`.

---

## 🎨 **Customization**  
- **Change Subtitle Font:**  
  Modify the `font_path` parameter to use a different font. It defaults to `Arial.ttf`.
- **Adjust Font Size:**  
  Change the `font_size` value to resize the subtitles.
- **Subtitle Position:**  
  Subtitles appear at the bottom by default. Adjust `x` and `y` values in the drawing section to reposition.

---

## 📜 **Supported SRT Format**  
This project supports SRT files with the following structure:  
```
1
00:00:01,000 --> 00:00:04,000
This is the first subtitle line

2
00:00:05,000 --> 00:00:07,000
Here is another line
```

---

## ⚙️ **How It Works**  
1. **Read SRT File:**  
   Extracts subtitle text along with start and end times using `read_srt()`.
2. **Automatic Line Breaking:**  
   Long lines are split into shorter ones for better display.
3. **Right-to-Left Text Support:**  
   Utilizes `arabic_reshaper` and `bidi` to correctly display RTL text.
4. **Adding Subtitles:**  
   Uses OpenCV and PIL to overlay subtitles on each video frame.
5. **Merging Audio:**  
   Combines the separate audio file with the video using Pydub and FFmpeg.

---

## 🔧 **Troubleshooting**  
- **Audio Sync Issues?**  
  Ensure the frame rate (FPS) of both the video and audio are identical.
- **Subtitles Not Showing?**  
  Verify the correct font path and ensure the font supports Persian characters.
- **FFmpeg Error on Windows?**  
  Confirm FFmpeg is added to the system PATH.

---

## 🎨 **Suggestions for Improvement**  
- **Add customization for subtitle color and font style.**
- **Support for other subtitle formats like VTT.**
- **Include a Graphical User Interface (GUI) for easier usage.**

---

## 📜 **License**  
This project is released under the **MIT License**.  
Feel free to copy, modify, and distribute it.

---

## 🌟 **Support This Project!**  
If you found this project useful, please give it a star (⭐) and share it with your friends!
```
