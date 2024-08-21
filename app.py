from flask import Flask, render_template, request, jsonify
from pytube import Search, YouTube

app = Flask(__name__)

def fetch_latest_videos():
    try:
        search = Search("latest videos")
        videos = []
        for video in search.results[:5]:
            yt = YouTube(video.watch_url)
            duration = yt.length
            videos.append({'title': video.title, 'url': video.watch_url, 'duration': f'{duration//60}:{duration%60:02d}'})
        return videos
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []

@app.route('/')
def index():
    latest_videos = fetch_latest_videos()
    return render_template('index.html', latest_videos=latest_videos)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    search = Search(query)
    results = []
    for video in search.results[:5]:
        try:
            yt = YouTube(video.watch_url)
            duration = yt.length
            results.append({'title': video.title, 'url': video.watch_url, 'duration': f'{duration//60}:{duration%60:02d}'})
        except Exception as e:
            print(f"Error fetching video duration: {e}")
            results.append({'title': video.title, 'url': video.watch_url, 'duration': '-:-:-'})
    return jsonify(results)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')
    try:
        video = YouTube(video_url)
        stream = video.streams.get_highest_resolution()
        stream.download()
        return jsonify({"message": f"Downloaded: {video.title}"})
    except Exception as e:
        return jsonify({"message": f"Failed to download: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
