import cv2
import os
import numpy as np
import tensorflow as tf
import facenet
import image_generator as gen
from datetime import datetime

FR_model = facenet.facenet()
FR_model.load_weights('nn4.small2.v1.h5')

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

threshold = 0.1
logs_directory = "logs/"

def create_logdir(slot):
    if not os.path.exists(logs_directory):
      os.makedirs(logs_directory, exist_ok = 'True')
    logs = []
    logs.append(datetime.today().strftime('%H:%M:%S') + ' ' + slot)
    logs.append('\n')
    return logs

def write_logs(logs):
    date = datetime.today().strftime('%Y-%m-%d')
    logs_filename = logs_directory + date + '.txt'
    with open(logs_filename, 'a+') as f:
        for line in logs:
          f.write(line)
          f.write('\n')

def write_attendance(line):
    with open('attendance.txt', 'a+') as f:
        f.write(line)
        f.write('\n')  

def img_path_to_encoding(image_path, model):
  img1 = cv2.imread(image_path, 1)
  return img_to_encoding(img1, model)
  
def img_to_encoding(image_path, model):
  image = cv2.resize(image_path, (96, 96))
  img = np.around(np.array(image) / 255.0, decimals=12)
  x_train = np.expand_dims(img, axis=0)
  embedding = model.predict_on_batch(x_train)
  return embedding / np.linalg.norm(embedding, ord=2)

def fill_database():
    database = {}
    for name in os.listdir('images'):
      database[name] = []
      for image in os.listdir(os.path.join('images',name)):
        database[name].append(img_path_to_encoding(os.path.join('images',name,image), FR_model))
    return database

def add_database(database, new_name):
    if new_name not in os.listdir('images'):
        gen.fetch_picture(new_name)
    if new_name not in database:
        for image in os.listdir(os.path.join('images',new_name)):
            database[new_name].append(img_path_to_encoding(os.path.join('images',new_name,image), FR_model))
    return database

def remove_database(database, name):
    if name in database:
        database.pop(name)
        return database
    return None

def save_database(database, filename):
    np.save(filename+'.npy', database) 

def load_database(filename):
    if os.path.isfile(filename+'.npy'):
        database = np.load(filename+'.npy',allow_pickle='TRUE').item()
        return database
    print('No file to load')

def verify_face(database, slot):
    logs = create_logdir(slot)
    latest_entry = ''
    attendance = set()
    write_attendance(datetime.today().strftime('%H:%M:%S') + ' ' + slot)
    
    video_capture = cv2.VideoCapture(0)
    if video_capture is None or not video_capture.isOpened():
       print('Warning: unable to open video source: ', source)
       return None
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

        for(name, encoded_image_list) in database.items():
          for encoded_image_name in encoded_image_list:
            dist = np.linalg.norm(encoding - encoded_image_name)
            if(dist < min_dist):
              min_dist = dist
              identity = name

        if min_dist < threshold and latest_entry != identity:
          latest_entry = identity
          attendance.add(identity)
          logs.append(datetime.today().strftime('%H:%M:%S') + "   -   " + identity)
          cv2.putText(frame, "Face : " + identity + " Verified", (x, y - 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
          cv2.putText(frame, "Dist : " + str(min_dist), (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
        elif latest_entry == identity:
          cv2.putText(frame, "Face : " + identity + " Already Verified", (x, y - 50), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
        else:
          cv2.putText(frame, 'No matching faces', (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

      cv2.imshow('Face Recognition System', frame)
      if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

    video_capture.release()
    cv2.destroyAllWindows()
    write_logs(logs)
    write_attendance(', '.join(attendance))
    return attendance
