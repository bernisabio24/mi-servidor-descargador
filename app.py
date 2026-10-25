from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Music Downloader Backend Engine (yt-dlp)"
    })

@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    url = data.get('url')
    is_audio = data.get('isAudio', True)

    if not url:
        return jsonify({'status': 'error', 'message': 'URL requerida'}), 400

    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Cancion_Descarga')

            url_stream = info.get('url')
            if not url_stream and 'formats' in info:
                for fmt in info['formats']:
                    if is_audio and fmt.get('acodec') != 'none':
                        url_stream = fmt.get('url')
                    elif not is_audio and fmt.get('vcodec') != 'none':
                        url_stream = fmt.get('url')

            if url_stream:
                return jsonify({
                    'status': 'success',
                    'title': title,
                    'downloadUrl': url_stream
                })
            else:
                return jsonify({'status': 'error', 'message': 'No se encontró flujo de audio'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
