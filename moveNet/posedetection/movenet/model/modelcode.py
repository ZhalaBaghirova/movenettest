import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2
import pandas as pd

def pose_estimation_function():
    # load model
    interpreter = tf.lite.Interpreter(model_path='C:/Users/jlmub/Desktop/moveNet/posedetection/movenet/model/lite-model_movenet_singlepose_lightning_3.tflite')
    interpreter.allocate_tensors()

    # Draw keypoints
    def draw_keypoints(frame, keypoints,confidence):
        y,x,c=frame.shape
        shaped=np.squeeze(np.multiply(keypoints,[y,x,1]))
        
        for kp in shaped:
            ky,kx,kp_conf=kp
            if kp_conf>confidence:
                cv2.circle(frame,(int(kx), int(ky)), 4, (0,255,0),-1)
                
    #  Draw edges
    EDGES = {
        (0, 1): 'm', 
        (0, 2): 'c',
        (1, 3): 'm',
        (2, 4): 'c',
        (5, 7): 'm',
        (7, 9): 'm',
        (6, 8): 'c',
        (8, 10): 'c',
        (5, 6): 'y',
        (5, 11): 'm',
        (6, 12): 'c',
        (11, 12): 'y',
        (11, 13): 'm',
        (13, 15): 'm',
        (12, 14): 'c',
        (14, 16): 'c'
    }

    def draw_edges(frame,keypoints,edges, confidence):
        y,x,c=frame.shape
        shaped=np.squeeze(np.multiply(keypoints,[y,x,1]))
        
        for edge,color in edges.items():
            p1, p2=edge
            print(p1,p2)
            y1,x1,c1=shaped[p1]
            y2,x2,c2=shaped[p2]
            
            if (c1>confidence) & (c2>confidence):
                cv2.line(frame,(int(x1),int(y1)),(int(x2),int(y2)),(255,0,0),2)
                
    # make detections
    cap = cv2.VideoCapture(0) #can pass video name instead of 0
    while cap.isOpened():
        ret, frame = cap.read()
        
    # reshape image to 192x192x3
        img= frame.copy()
        img=tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192,192)
        input_image = tf.cast(img, dtype=tf.float32)
        
    # setup input and output
        input_details=interpreter.get_input_details()
        output_details=interpreter.get_output_details()
        
        
    # make prediction
        interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        interpreter.invoke()
        keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
        print(keypoints_with_scores)
        
    #     rendering
        draw_edges(frame,keypoints_with_scores,EDGES, 0.6)
        draw_keypoints(frame, keypoints_with_scores,0.6)
        
        cv2.imshow('MoveNet Lightning', frame)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()