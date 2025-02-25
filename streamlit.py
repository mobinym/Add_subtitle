import streamlit as st
import moviepy as mp
import whisper
from deep_translator import GoogleTranslator

# تابع استخراج صدا از ویدیو
def extract_audio(video_path, output_audio):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio)
    video.close()

# تابع تبدیل صدا به متن
def speech_to_text(audio_file, language="en"):
    model = whisper.load_model("tiny")  # می‌تونیم "tiny" یا "large" هم استفاده کنیم بسته به نیاز
    result = model.transcribe(audio_file)  # تشخیص خودکار زبان
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
                # ترجمه به فارسی
                translated_text = GoogleTranslator(source='en', target='fa').translate(text)
                text = translated_text
            
            srt_file.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

# رابط استریم‌لیت
st.title("Video Audio Extractor and Subtitle Generator")

# آپلود فایل ویدیو
video_file = st.file_uploader("Upload a Video", type=["mp4"])

# دکمه برای پردازش فایل
if video_file is not None:
    # ذخیره فایل ویدیو به صورت موقت
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    
    st.write("Processing video...")

    # استخراج صدا از ویدیو
    audio_output = "final.mp3"
    extract_audio("temp_video.mp4", audio_output)
    
    # تبدیل صدا به متن
    st.write("Transcribing audio...")
    result = speech_to_text(audio_output, language="en")
    
    # انتخاب زبان برای زیرنویس
    translate_to_farsi = st.radio("Do you want subtitles in Persian?", ("No", "Yes")) == "Yes"
    
    # تولید فایل SRT با توجه به انتخاب کاربر
    if st.button("Generate Subtitles"):
        generate_srt_from_segments(result["segments"], "subtitle.srt", translate_to_farsi)
        st.success("Subtitle file generated successfully! Download it below.")

        # دکمه دانلود برای فایل SRT
        with open("subtitle.srt", "rb") as file:
            st.download_button("Download SRT", file, file_name="subtitle.srt", mime="text/plain")
