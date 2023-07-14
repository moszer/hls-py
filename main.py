from flask import Flask, request, send_from_directory, make_response
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hls_link = request.form['hls_link']
        download_path = os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4')
        download_hls(hls_link, download_path)
        return '''
        <h1>HLS Downloader</h1>
        <p>Video downloaded successfully! Click the button below to download.</p>
        <a href="/download" class="btn">Download Video</a>
        '''
    return '''
    <h1>HLS Downloader</h1>
    <form method="post" action="/">
        <input type="text" name="hls_link" placeholder="Paste HLS link" required>
        <input type="submit" value="Download">
    </form>
    '''

def download_hls(hls_link, download_path):
    ffmpeg_cmd = ['ffmpeg', '-i', hls_link, '-c', 'copy', download_path]
    subprocess.run(ffmpeg_cmd)

@app.route('/download')
def download():
    filename = 'video.mp4'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    response = make_response(send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True))
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response

if __name__ == '__main__':
    app.run(debug=True)
