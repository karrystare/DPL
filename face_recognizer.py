import cv2
import os
import numpy as np
import tensorflow as tf
import facenet

FR_model = facenet.facenet()
FR_model.load_weights('nn4.small2.v1.h5')

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

threshold = 0.1

face_database = {}
attendance = {}

def img_path_to_encoding(image_path, model):
  img1 = cv2.imread(image_path, 1)
  return img_to_encoding(img1, model)
  
def img_to_encoding(image_path, model):
  image = cv2.resize(image_path, (96, 96))
  img = np.around(np.array(image) / 255.0, decimals=12)
  x_train = np.expand_dims(img, axis=0)
  embedding = model.predict_on_batch(x_train)
  return embedding / np.linalg.norm(embedding, ord=2)

for name in os.listdir('images'):
  face_database[name] = []
  for image in os.listdir(os.path.join('images',name)):
    face_database[name].append(img_path_to_encoding(os.path.join('images',name,image), FR_model))
    attendance[name] = False

video_capture = cv2.VideoCapture(0)
while True:
  ret, frame = video_capture.read()
  frame = cv2.flip(frame, 1)

  faces = face_cascade.detectMultiScale(frame, 1.3, 5)
  for(x,y,w,h) in faces:
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
    roi = frame[y:y+h, x:x+w]
    encoding = img_to_encoding(roi, FR_model)
    min_dist = 100
    identity = None

    for(name, encoded_image_list) in face_database.items():
      for encoded_image_name in encoded_image_list:
        dist = np.linalg.norm(encoding - encoded_image_name)
        if(dist < min_dist):
          min_dist = dist
          identity = name

    if min_dist < threshold:
      attendance[name] = True
      cv2.putText(frame, "Face : " + identity, (x, y - 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
      cv2.putText(frame, "Dist : " + str(min_dist), (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
    else:
      cv2.putText(frame, 'No matching faces', (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

  cv2.imshow('Face Recognition System', frame)
  if(cv2.waitKey(1) & 0xFF == ord('q')):
    break

video_capture.release()
cv2.destroyAllWindows()

