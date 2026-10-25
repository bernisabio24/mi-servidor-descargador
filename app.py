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

@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'GET':
        url = request.args.get('url')
        is_audio = request.args.get('isAudio', 'true').lower() == 'true'
    else:
        data = request.json or {}
        url = data.get('url')
        is_audio = data.get('isAudio', True)

    if not url:
        return jsonify({'status': 'error', 'message': 'URL requerida'}), 400

    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'geo_bypass': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return jsonify({'status': 'error', 'message': 'No se pudo obtener informacion'}), 404

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
                return jsonify({'status': 'error', 'message': 'No se encontró flujo de audio/video'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
