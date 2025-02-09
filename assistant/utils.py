import os
import cv2
import numpy as np
import torch
from PIL import Image
from transformers import pipeline, CLIPSegProcessor, CLIPSegForImageSegmentation
from ultralytics import YOLO
import os
import logging
from gtts import gTTS
from playsound import playsound

logging.getLogger("ultralytics").setLevel(logging.ERROR)
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
depth_pipe = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device=device, use_fast=True)
seg_processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
seg_model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined").to(device)
yolo_model = YOLO('yolo11n.pt')

def speak(text, lang):
    print("Will speak", text)
    tts = gTTS(text=text, lang=lang)
    path = 'say.mp3'
    if os.path.exists(path):
        os.remove(path)
    tts.save(path)
    playsound(path)
    
    # audio_fp = BytesIO()
    # tts.write_to_fp(audio_fp)
    # audio_fp.seek(0)
    # audio = AudioSegment.from_mp3(audio_fp)
    # play(audio)

    # tts.save('say.mp3')
    # wave_obj = sa.WaveObject.from_wave_file(filename)
    # play_obj = wave_obj.play()
    # play_obj.wait_done()
    # speaker = wincom.Dispatch("SAPI.SpVoice")
    # speaker.Speak(sanitized_text)

def run_object_detection(frame):
    detection_frame = frame.copy()
    yolo_results = yolo_model(detection_frame)
    for result in yolo_results[0].boxes:
        box = result.xyxy[0]
        confidence = result.conf[0]
        class_id = int(result.cls[0])
        label = yolo_model.names[class_id]

        x_top_left, y_top_left, x_bottom_right, y_bottom_right = map(int, box)
        cv2.rectangle(detection_frame, (x_top_left, y_top_left), (x_bottom_right, y_bottom_right), (0, 255, 0), 2)
        label_text = f"{label}: {confidence:.2f}"
        cv2.putText(detection_frame, label_text, (x_top_left, y_top_left - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return detection_frame

def run_depth_estimation(frame, overlay_detection=False):
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    depth = depth_pipe(pil_image)["depth"]
    depth_array = np.array(depth)
    depth_normalized = cv2.normalize(depth_array, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_MAGMA)

    if overlay_detection:
        detection_frame = run_object_detection(frame)
        for result in yolo_model(detection_frame)[0].boxes:
            box = result.xyxy[0]
            x_top_left, y_top_left, x_bottom_right, y_bottom_right = map(int, box)
            cv2.rectangle(depth_colored, (x_top_left, y_top_left), (x_bottom_right, y_bottom_right), (0, 255, 0), 2)
            label_text = f"{yolo_model.names[int(result.cls[0])]}: {result.conf[0]:.2f}"
            cv2.putText(depth_colored, label_text, (x_top_left, y_top_left - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return depth_colored

def initialize_video_writer(save_video=False, output_dir="visualization_output", fps=6, resolution=(1280, 960)):
    if save_video:
        os.makedirs(output_dir, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        return cv2.VideoWriter(f"{output_dir}/output.mp4", fourcc, fps, resolution)
    return None

def get_object_mask(frame, prompt):
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    seg_inputs = seg_processor(text=[prompt], images=[pil_image], padding="max_length", return_tensors="pt").to(device)
    with torch.no_grad():
        seg_outputs = seg_model(**seg_inputs)
    mask = torch.sigmoid(seg_outputs.logits.unsqueeze(1)[0][0]).cpu().numpy()
    binary_mask = (cv2.resize(mask, (frame.shape[1], frame.shape[0])) > 0.5).astype(np.uint8) * 255
    return binary_mask