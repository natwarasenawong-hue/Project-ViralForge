import streamlit as st
from moviepy.editor import *
import requests # เพื่อจำลองการดาวน์โหลดไฟล์

# --- ส่วนจำลอง AI Modules (ปกติส่วนนี้จะเป็น API Call) ---
def analyze_trends():
    st.info("Trend Spotter AI: พบว่าเพลง 'Upbeat Folk' กำลังเป็นกระแส")
    # URL to a royalty-free music file
    music_url = "https://cdn.pixabay.com/download/audio/2022/08/04/audio_2dde641a22.mp3"
    r = requests.get(music_url)
    with open("trending_music.mp3", "wb") as f:
        f.write(r.content)
    return "trending_music.mp3"

def generate_script(topic):
    st.info(f"Scriptwriter AI: กำลังเขียนสคริปต์สำหรับหัวข้อ '{topic}'...")
    return [
        {"text": "บ่ายทีไร หนังตาก็หนักทุกที", "duration": 3, "keyword": "sleepy office"},
        {"text": "1. ลุกขึ้นเดินยืดเส้นยืดสาย", "duration": 4, "keyword": "office stretching"},
        {"text": "2. ดื่มน้ำเปล่าเย็นๆ แทนกาแฟ", "duration": 4, "keyword": "drinking water"},
        {"text": "3. ฟังเพลงสนุกๆ ที่ชอบ", "duration": 3, "keyword": "listening music headphones"},
    ]

def find_visuals(script):
    st.info("Visual Scout AI: กำลังค้นหาฟุตเทจที่ตรงกับสคริปต์...")
    video_urls = {
        "sleepy office": "https://cdn.pixabay.com/video/2020/09/11/50693-458999993.mp4",
        "office stretching": "https://cdn.pixabay.com/video/2022/06/13/118712-723689163.mp4",
        "drinking water": "https://cdn.pixabay.com/video/2019/11/04/28128-372505556.mp4",
        "listening music headphones": "https://cdn.pixabay.com/video/2023/06/21/167732-839070904.mp4",
    }
    clips = []
    for scene in script:
        url = video_urls[scene["keyword"]]
        r = requests.get(url, stream=True)
        filename = f"{scene['keyword'].replace(' ', '_')}.mp4"
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        clips.append(VideoFileClip(filename).set_duration(scene["duration"]))
    return clips

def assemble_video(script, clips, music_file):
    st.info("Editor AI: เริ่มกระบวนการตัดต่อวิดีโอ...")
    final_clips = []
    for i, scene in enumerate(script):
        txt_clip = TextClip(scene["text"], fontsize=70, color='white', font='Arial-Bold',
                            stroke_color='black', stroke_width=2)
        txt_clip = txt_clip.set_pos('center').set_duration(scene["duration"])
        
        video_clip = clips[i].resize(height=1920).crop(x1=0, y1=0, width=1080, height=1920) # Resize to 9:16
        final_clips.append(CompositeVideoClip([video_clip, txt_clip]))

    final_video = concatenate_videoclips(final_clips)
    
    # Add music
    audioclip = AudioFileClip(music_file).set_duration(final_video.duration)
    final_video.audio = audioclip
    
    output_filename = "tiktok_final_video.mp4"
    final_video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    return output_filename

# --- หน้าเว็บ UI ---
st.set_page_config(layout="wide")
st.title("🎬 ระบบจำลอง AI Content Creator for TikTok (Project ViralForge)")

topic = st.text_input("ป้อนหัวข้อวิดีโอที่คุณต้องการสร้าง:", "3 วิธีแก้ง่วงตอนบ่าย")

if st.button("🚀 สร้างวิดีโอ TikTok ด้วย AI"):
    with st.spinner("AI กำลังทำงาน... โปรดรอสักครู่ กระบวนการนี้อาจใช้เวลา 2-3 นาที"):
        # 1. Analyze Trends
        music_file = analyze_trends()
        # 2. Generate Script
        script = generate_script(topic)
        # 3. Find Visuals
        video_clips = find_visuals(script)
        # 4. Assemble Video (The core of the simulation)
        final_video_file = assemble_video(script, video_clips, music_file)
        
        st.success("🎉 AI สร้างวิดีโอของคุณสำเร็จแล้ว!")
        
        video_file = open(final_video_file, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        
        with open(final_video_file, "rb") as file:
            st.download_button(
                label="📥 ดาวน์โหลดวิดีโอ (MP4)",
                data=file,
                file_name=final_video_file,
                mime="video/mp4"
            )
