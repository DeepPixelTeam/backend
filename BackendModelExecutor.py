import cv2
from ultralytics import YOLO

class ModelExecutor:
    model_path = None
    input_path = None
    frame_buffer = None
    output_path = None

    model = None
    device = None 
    

    def __init__(self, model_path, input_path, output_path):
        self.model_path = model_path
        self.input_path = input_path
        self.frame_buffer = []
        self.output_path = output_path
        self.model = YOLO(model_path)

    def executeModel(self):
        cap = cv2.VideoCapture(self.input_path)
        
        if not cap.isOpened():
            print("Video failed to load")
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = self.process_frame(frame)

            self.frame_buffer.append(processed_frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        self.save_video(fps, width, height)

    def process_frame(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.model(img_rgb)
        result_frame = results[0].plot()
        result_bgr = cv2.cvtColor(result_frame, cv2.COLOR_RGB2BGR)

        return result_bgr
    
    def save_video(self, fps, width, height):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height), isColor=True)

        for frame in self.frame_buffer:
            out.write(frame)

        out.release()
        print("Video saved successfully.")