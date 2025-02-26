import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import subprocess
import time

# تابع استخراج صدا از ویدیو با استفاده از ffmpeg
def extract_audio(video_path, output_audio):
    subprocess.run([
        "ffmpeg", "-y",  # <- اینجا -y اضافه شد
        "-i", video_path,
        "-q:a", "0",
        "-map", "a",
        output_audio
    ])

# تابع تبدیل صدا به متن
def speech_to_text(audio_file, language="en"):
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file)
    return result

# تبدیل زمان به فرمت SRT
def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# تولید فایل SRT با ترجمه به فارسی یا انگلیسی
def generate_srt_from_segments(segments, output_srt_path, translate_to_farsi=False):
    with open(output_srt_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(segments, start=1):
            start_time = seconds_to_srt_time(segment["start"])
            end_time = seconds_to_srt_time(segment["end"])
            text = segment["text"].strip()

            if translate_to_farsi:
                translated_text = GoogleTranslator(source='en', target='fa').translate(text)
                text = translated_text
            
            srt_file.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

# افزودن زیرنویس به ویدیو با استفاده از ffmpeg
def add_subtitles_to_video(video_path, srt_file, output_video_path):
    subprocess.run([
        "ffmpeg", "-y",  # بازنویسی فایل خروجی
        "-i", video_path,
        "-vf", f"subtitles={srt_file}:force_style='FontSize=10,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0'",
        "-c:a", "copy",
        output_video_path
    ])

# رابط استریم‌لیت
st.title("Video Audio Extractor and Subtitle Generator")

# آپلود فایل ویدیو
video_file = st.file_uploader("Upload a Video", type=["mp4"])

# ذخیره وضعیت فایل و دکمه‌ها با استفاده از session_state
if "srt_output" not in st.session_state:
    st.session_state.srt_output = None
if "output_video" not in st.session_state:
    st.session_state.output_video = None
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False
if "translate_to_farsi" not in st.session_state:
    st.session_state.translate_to_farsi = False
if "video_file" not in st.session_state:
    st.session_state.video_file = None

# اگر ویدیو جدید آپلود شده باشد، وضعیت را بازنشانی می‌کنیم
if video_file is not None:
    # اگر ویدیوی جدید آپلود شود، پردازش مجدد انجام می‌شود
    if video_file != st.session_state.video_file:
        st.session_state.processing_done = False  # پردازش را دوباره شروع می‌کنیم
        st.session_state.srt_output = None
        st.session_state.output_video = None
        st.session_state.video_file = video_file

# انتخاب زبان برای زیرنویس (English یا Persian)
language_option = st.radio("Select subtitle language:", ("English", "Persian"))

# ذخیره زبان انتخاب شده در session_state
st.session_state.translate_to_farsi = language_option == "Persian"

# دکمه برای پردازش فایل
if video_file is not None and not st.session_state.processing_done:
    # نمایش دکمه "Generate Subtitles" تنها زمانی که ویدیو آپلود شده باشد
    if st.button("Generate Subtitles"):
        # ذخیره فایل ویدیو به صورت موقت
        with open("temp_video.mp4", "wb") as f:
            f.write(st.session_state.video_file.getbuffer())
        
        # نشان دادن لودینگ
        with st.spinner("Processing video... Please wait."):
            # استخراج صدا از ویدیو
            audio_output = "final.mp3"
            extract_audio("temp_video.mp4", audio_output)
            
            # تبدیل صدا به متن
            st.write("Transcribing audio...")
            result = speech_to_text(audio_output, language="en")
            
            # تولید فایل SRT با توجه به انتخاب کاربر
            srt_output = "subtitle.srt"
            generate_srt_from_segments(result["segments"], srt_output, st.session_state.translate_to_farsi)
            st.session_state.srt_output = srt_output  # ذخیره فایل SRT
            st.success("Subtitle file generated successfully! Now embedding subtitles...")

            # اضافه کردن زیرنویس به ویدیو
            output_video = "video_with_subtitles.mp4"
            add_subtitles_to_video("temp_video.mp4", srt_output, output_video)
            st.session_state.output_video = output_video  # ذخیره ویدیو خروجی
            st.session_state.processing_done = True  # وضعیت پردازش تکمیل شد
            st.success("Video with subtitles generated successfully! Download it below.")

# نمایش دکمه‌های دانلود فقط زمانی که پردازش کامل شده باشد
if st.session_state.processing_done:
    # دکمه‌های دانلود را تنها زمانی که پردازش انجام شده باشد نمایش می‌دهیم
    if st.session_state.output_video:
        with open(st.session_state.output_video, "rb") as file:
            st.download_button("Download Video with Subtitles", file, file_name="video_with_subtitles.mp4", mime="video/mp4")
    
    if st.session_state.srt_output:
        with open(st.session_state.srt_output, "rb") as srt_file:
            st.download_button("Download Subtitle File", srt_file, file_name="subtitle.srt", mime="text/plain")

