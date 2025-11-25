from flask import Flask, request, jsonify
import yt_dlp
import os
from pydub import AudioSegment

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Backend running successfully!"})

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    youtube_url = data.get("url")

    if not youtube_url:
        return jsonify({"error": "YouTube URL missing"}), 400

    output_file = "downloaded_video.mp4"

    ydl_opts = {
        "format": "mp4",
        "outtmpl": output_file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "status": "success",
        "message": "Video downloaded successfully",
        "file": output_file
    })

if __name__ == "__main__":
    app.run(debug=True)
