import face_recognition
import cv2
import os
import time
#Time Set before suspending or shutting the PC
def countdown(p,q):
    i=p
    j=q
    k=0
    while True:
        if(j==-1):
            j=59
            i -=1
        if(j > 9):  
            print(str(k)+str(i)+":"+str(j), end="\r")
        else:
            print(str(k)+str(i)+":"+str(k)+str(j), end="\r")
        time.sleep(1)
        j -= 1
        if(i==0 and j==-1):
            break
    if(i==0 and j==-1):
        os.system("systemctl suspend")
        time.sleep(1)

video_capture = cv2.VideoCapture(0)

img1_image = face_recognition.load_image_file("/root/Desktop/Project/Face-locking/faces/mihir.jpg")
img1_face_encoding = face_recognition.face_encodings(img1_image)[0]

known_face_encodings = [
    img1_face_encoding
]
known_face_names = [
    "yash"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (1, 1), fx=1, fy=1)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if name == "Unknown":
            os.system("zenity --notification --text='BEWARE OF THE SPY NEAR YOU'")   #To show notification
            video_capture.release()
            cv2.destroyAllWindows()
            countdown(0,15) #Call of timer
		
    
    cv2.imshow('Video', frame)
