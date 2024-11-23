from flask import Flask, render_template, request, send_file
import instaloader
import os
from datetime import datetime

app = Flask(__name__)

# डाउनलोड्स फोल्डर बनाने के लिए
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        try:
            # पहले डाउनलोड्स फोल्डर को साफ करें
            for file in os.listdir(DOWNLOAD_FOLDER):
                file_path = os.path.join(DOWNLOAD_FOLDER, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

            # Instagram URL से पोस्ट ID निकालें
            post_id = url.split('/')[-2]
            
            # Instaloader इंस्टेंस बनाएं
            L = instaloader.Instaloader(dirname_pattern=DOWNLOAD_FOLDER)
            
            # रील डाउनलोड करें
            post = instaloader.Post.from_shortcode(L.context, post_id)
            L.download_post(post, target=DOWNLOAD_FOLDER)
            
            # डाउनलोड की गई फ़ाइल को ढूंढें
            for file in os.listdir(DOWNLOAD_FOLDER):
                if file.endswith('.mp4'):
                    video_path = os.path.join(DOWNLOAD_FOLDER, file)
                    return send_file(video_path, as_attachment=True)
            
            return "Video file not found in downloads"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 