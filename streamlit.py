import streamlit as st
from pydub import AudioSegment
import whisper
from deep_translator import GoogleTranslator
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

# استخراج صدا از ویدیو
def extract_audio(video_path, output_audio):
    audio = AudioSegment.from_file(video_path)
    audio.export(output_audio, format='mp3')

# تبدیل صدا به متن
def speech_to_text(audio_file, language="en"):
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file)
    return result

# تبدیل زمان به SRT
def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

# ساخت SRT با ترجمه
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

# خواندن SRT
def read_srt(srt_file):
    subtitles = []
    with open(srt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    index = 0
    while index < len(lines):
        if lines[index].strip().isdigit():
            start, end = lines[index + 1].strip().split(' --> ')
            text = lines[index + 2].strip()
            start = convert_time_to_seconds(start)
            end = convert_time_to_seconds(end)
            subtitles.append({'start': start, 'end': end, 'text': text})
        index += 4
    return subtitles

# تبدیل زمان SRT به ثانیه
def convert_time_to_seconds(time_str):
    h, m, s = time_str.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

# تقسیم متن به خطوط
def split_text_to_lines(text, font, max_width):
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = font.getbbox(test_line)  # استفاده از getbbox به جای getsize
        width, _ = bbox[2], bbox[3]  # محاسبه عرض متن

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
            
    if current_line:
        lines.append(current_line)
    
    return lines


# اضافه کردن زیرنویس به ویدیو
def add_subtitles_with_opencv(video_path, srt_file, output_path, font_path='arial.ttf', font_size=20, is_farsi=False):
    subtitles = read_srt(srt_file)
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    font = ImageFont.truetype(font_path, font_size)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        for subtitle in subtitles:
            if subtitle['start'] <= current_time <= subtitle['end']:
                text = subtitle['text']
                if is_farsi:
                    reshaped_text = arabic_reshaper.reshape(text)
                    text = get_display(reshaped_text)

                frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(frame_pil)

                # محاسبه عرض و ارتفاع متن و تقسیم متن به خطوط
                max_width = width - 40  # فاصله از دو طرف
                lines = split_text_to_lines(text, font, max_width)
                
                y = height - 50  # شروع از پایین ویدیو

                for line in lines:
                    # محاسبه موقعیت متن
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    # تنظیم موقعیت متن
                    x = (width - text_width) // 2
                    draw.rectangle([x - 10, y - 10, x + text_width + 10, y + text_height + 10], fill=(0, 0, 0, 180))  # پس‌زمینه نیمه‌شفاف
                    draw.text((x, y), line, font=font, fill=(255, 255, 255))  # رنگ سفید برای متن
                    y += text_height + 10  # تنظیم فاصله برای خط بعدی

                frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

        out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# رابط Streamlit
st.title("Video Subtitle Generator")
video_file = st.file_uploader("Upload a Video", type=["mp4"])
if video_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.getbuffer())

    st.write("Extracting audio and processing video... Please wait!")

    # استفاده از spinner برای نمایش حالت لودینگ
    with st.spinner('Processing...'):
        audio_output = "final.mp3"
        extract_audio("temp_video.mp4", audio_output)
        result = speech_to_text(audio_output, language="en")
        translate_to_farsi = st.radio("Subtitles Language:", ("English", "Persian")) == "Persian"
        srt_output = "subtitle.srt"
        generate_srt_from_segments(result["segments"], srt_output, translate_to_farsi)
        st.success("Subtitle generated successfully!")

        with open(srt_output, "rb") as file:
            st.download_button("Download SRT", file, file_name="subtitle.srt", mime="text/plain")

        output_video = "output_video.mp4"
        add_subtitles_with_opencv("temp_video.mp4", srt_output, output_video, font_path='/Library/Fonts/Arial.ttf', is_farsi=translate_to_farsi)

        with open(output_video, "rb") as video:
            st.download_button("Download Video with Subtitles", video, file_name="output_video.mp4", mime="video/mp4")
