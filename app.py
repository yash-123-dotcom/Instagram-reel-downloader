import streamlit as st
import instaloader
import os
import re
from datetime import datetime

def extract_shortcode_from_url(url):
    """Extract the shortcode from Instagram URL"""
    pattern = r'(?:https?:\/\/)?(?:www\.)?instagram\.com(?:\/reels?\/|\/p\/|\/reel\/)([A-Za-z0-9_-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def download_reel(url):
    try:
        # Extract shortcode from URL
        shortcode = extract_shortcode_from_url(url)
        if not shortcode:
            return False, "Invalid Instagram URL"

        # Initialize instaloader with custom download path
        L = instaloader.Instaloader(
            dirname_pattern="downloads",  # सभी फाइल्स downloads फोल्डर में सेव होंगी
            filename_pattern="{date}_reel"  # फाइल का नाम पैटर्न
        )
        
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        # Create downloads directory if it doesn't exist
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
            
        # Download the post
        L.download_post(post, target="downloads")
        
        # Find the downloaded video file
        video_file = None
        for file in os.listdir("downloads"):
            if file.endswith(".mp4"):
                video_file = os.path.join("downloads", file)
                break
                
        if video_file:
            return True, video_file
        
        return False, "Video file not found after download"
        
    except Exception as e:
        return False, str(e)

# Streamlit UI
st.set_page_config(page_title="Instagram Reel Downloader", page_icon="📥")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
    }
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📥 Instagram Reel Downloader")

# URL input
url = st.text_input("Paste Instagram Reel URL here")

# Download button
if st.button("Download Reel", type="primary"):
    if url:
        with st.spinner('Downloading...'):
            success, result = download_reel(url)
            if success:
                try:
                    # Create download button for saved video
                    with open(result, "rb") as f:
                        video_bytes = f.read()
                    
                    st.download_button(
                        label="Click to Download",
                        data=video_bytes,
                        file_name="instagram_reel.mp4",
                        mime="video/mp4"
                    )
                    st.success("Download completed! ✅")
                    
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
                finally:
                    # Clean up - delete downloads directory
                    try:
                        import shutil
                        shutil.rmtree("downloads", ignore_errors=True)
                    except:
                        pass
            else:
                st.error(f"Failed to download: {result}")
    else:
        st.warning("Please enter a valid Instagram Reel URL")

# Features section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='text-align: center; background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;'>
            ⚡<br>Fast Download
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='text-align: center; background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;'>
            ♾️<br>Unlimited Downloads
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='text-align: center; background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px;'>
            🛡️<br>Safe & Secure
        </div>
    """, unsafe_allow_html=True) 