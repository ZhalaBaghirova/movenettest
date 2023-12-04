# app/views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse
import threading
from .model.modelcode import pose_estimation_function

# Flag to indicate whether to continue video streaming
streaming_active = True
def home(request):
    return render(request, 'pose_estimation.html')

def video_stream():
    while streaming_active:
        frame = pose_estimation_function()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def pose_estimation(request):
    return render(request, 'pose_estimation.html')

def video_feed(request):
    return StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')
