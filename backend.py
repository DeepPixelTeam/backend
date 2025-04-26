from flask import Flask, request, send_file
from flask_cors import CORS
import BackendModelExecutor
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = "outputs"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/upload-and-run-model', methods=['POST'])
def upload_files():
    video = request.files.get('video')
    model_file = request.files.get('model')
    model_name = request.form.get('model_name')

    video_filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    output_path = os.path.join(OUTPUT_FOLDER, video_filename)

    # Save video
    video.save(video_path)
    
    if model_file:
        model_filename = secure_filename(model_file.filename)
        model_path = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)
        model_file.save(model_path)
    elif model_name:
        model_path = model_name

    modelExecutor = BackendModelExecutor.ModelExecutor(model_path, video_path, output_path)
    print("Executing Model")
    modelExecutor.executeModel()

    return send_file(output_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
