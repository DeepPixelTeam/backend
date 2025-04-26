from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import BackendModelExecutor
import os
from werkzeug.utils import secure_filename

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = "outputs"
app.state.UPLOAD_FOLDER = UPLOAD_FOLDER
app.state.OUTPUT_FOLDER = OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.post('/upload-and-run-model')
async def upload_files(video: UploadFile = File(...), model: UploadFile = File(None), model_name: str = Form(None)):
    video_filename = secure_filename(video.filename)
    
    #print(" = " + str())
    video_path = os.path.join(app.state.UPLOAD_FOLDER, video_filename)
    output_path = os.path.join(app.state.OUTPUT_FOLDER, video_filename)
    print("video_filename = " + str(video_filename))
    print("video_path = " + str(video_path))
    print("output_path = " + str(output_path))
    # Save video
    with open(video_path, "wb") as f:
        f.write(await video.read())

    model_path = None
    if model:
        model_filename = secure_filename(model.filename)
        model_path = os.path.join(app.state.UPLOAD_FOLDER, model_filename)
        with open(model_path, "wb") as f:
            f.write(await model.read())
    elif model_name:
        # Handle case where model_name is provided directly
        model_path = os.path.join(app.state.OUTPUT_FOLDER, model_name)  # Assuming the model is already in the correct directory

    # Execute the model
    modelExecutor = BackendModelExecutor.ModelExecutor(model_path, video_path, output_path)
    print("Executing Model")
    modelExecutor.executeModel()

    return FileResponse(output_path, headers={"Content-Disposition": f"attachment; filename={video_filename}"})

# To run the FastAPI app, you can use Uvicorn
