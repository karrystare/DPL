import cv2
import os
import uuid

path = 'images'
MAX_NUMBER_OF_IMAGES = 100
def fetch_picture(name):
        number_of_images = 0
        directory = os.path.join(path, name)

        if not os.path.exists(directory):
                os.makedirs(directory, exist_ok = 'True')
                
        cap = cv2.VideoCapture(0)
        if cap is None or not cap.isOpened():
               return None
        while number_of_images < MAX_NUMBER_OF_IMAGES:
            ret, frame = cap.read()
           
            # Cut down frame to 250x250px
            frame = frame[120:120+250,200:200+250, :]

            if cv2.waitKey(1) & 0XFF == ord('p'):
                cv2.imwrite(os.path.join(directory, '{}.jpg'.format(uuid.uuid1())), frame)
                number_of_images += 1
                
            cv2.imshow('Image Collection', frame)
            
            # Breaking gracefully
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return ''
