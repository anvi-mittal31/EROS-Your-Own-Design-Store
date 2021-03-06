from flask.templating import render_template
from tensorflow.keras.models import model_from_json
import numpy as np
import cv2
import os
import random


class FacialExpressionModel(object):
    EMOTIONS_LIST = ["ANGRY", "DISGUST", "FEAR", "HAPPY", "SAD", "SURPRISE", "NEUTRAL"]; ## dont change the order
    def __init__(self, model_json_file, model_weights_file):
        # load model from JSON file
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)
        print("Model loaded from disk")
        self.loaded_model.summary()

    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        self.preds[4:6] += 0.1
        self.preds[1:3] += 0.2
        lbl = np.argmax(self.preds)
        return FacialExpressionModel.EMOTIONS_LIST[lbl], lbl


'''rgb = cv2.VideoCapture(0)
emo_happy = cv2.imread('happy.png',1)
emo_sad = cv2.imread('sad.png',1)
emo_fear = cv2.imread('fear.png',1)
emo_disgust = cv2.imread('disgust.png',1)
emo_surprise = cv2.imread('surprise.png',1)
emo_angry = cv2.imread('angry.png',1)
emo_neutral = cv2.imread('neutral.png',1)
emoji = [emo_angry,emo_disgust,emo_fear,emo_happy,emo_sad,emo_surprise,emo_neutral] #fix order'''

'''def __get_data__(rgb):
    
    _, fr = rgb.read()
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = facec.detectMultiScale(gray, 1.25, 5)
    return faces, fr, gray'''


def start_app(frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    facec = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    cnn = FacialExpressionModel("model1.json", "chkPt1.hdf5")
    #while True:
    #faces, fr, gray_fr = __get_data__(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facec.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        fc = gray[y:y+h, x:x+w]
        fc = cv2.normalize(fc,None,0,255,cv2.NORM_MINMAX)
#             fc = cv2.addWeighted(fc,1.5,blur,-0.5,0)
        roi = cv2.resize(fc, (48, 48))
        pred, lbl = cnn.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
        #print(pred)
        #list.append(pred)
        cv2.putText(frame, pred, (x, y), font, 1, (255, 255, 0), 2)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        x1 = x + w//2
        y1 = y + h//2
        #emo = emoji[lbl]
        return frame,pred



# def wallpaperHandler():
#     if (FINAL_PRED == 'happy'):
#         return render_template()



        '''try:
            emo = cv2.resize(emo,(h,w))
            frame[y:y+h,x:x+w] = cv2.addWeighted(frame[y:y+h,x:x+w],0.5,emo,0.5,0)
        except Exception as e:
            print(str(e))'''
    '''if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        #break
#         cv2.imshow("img",emo)
    cv2.imshow('Filter', frame)'''


'''def detect():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (1366, 800))
            start_app(frame)
            return frame
            cv2.imshow('Filter',frame)
            cv2.waitKey(1)
        else:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    #start_app()'''
