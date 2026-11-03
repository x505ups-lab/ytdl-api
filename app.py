from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get-link', methods=['GET'])
def get_video_link():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'format': 'best',
        'geturl': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url', None)

            if not direct_url:
                formats = info.get('formats', [{}])
                direct_url = formats[-1].get('url', '')

            return jsonify({
                "status": "success",
                "title": info.get('title', 'Video'),
                "direct_url": direct_url
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
