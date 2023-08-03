def main(face_photo,name_photo,name_video):
    # Load a sample picture and learn how to recognize it.
    object_image = face_photo
    object_face_encoding = face_recognition.face_encodings(object_image)[0]
    
    # Create arrays of known face encodings and their names
    object_name = name_photo
    object_video = name_video
    known_face_encodings = [
         object_face_encoding
        # nikita_face_encoding
    ]
    known_face_names = [
        f'{object_name}'
        # "Nikita"
    ]
    print('Найдено лиц', len(known_face_encodings), 'в изображении.')
    
    def save_frame(frame, cnt):
        number_count = cnt
        saveframe_name = os.path.join(foldername, f'frame-{number_count}.jpg')
        cv2.imwrite(saveframe_name, frame)
        
    # Make the folder to save matched screenshots
    foldername, _ = os.path.splitext(object_video)
    now_day = datetime.datetime.now().strftime('%d')
    now_month = datetime.datetime.now().strftime('%m')
    now_year = datetime.datetime.now().strftime('%Y')
    now_time = datetime.datetime.now().strftime('%X').replace(':','.')
    foldername += f'-{now_day}{now_month}{now_year}_{now_time}'
    if not os.path.isdir(foldername):
        os.mkdir(foldername)
    
    # Open the input movie file
    input_movie = cv2.VideoCapture(f'{object_video}')
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create an output movie file
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_movie = cv2.VideoWriter(f'out_{now_day}{now_month}{now_year}_{now_time}_{object_video}', fourcc, 15, (640, 480))
    face_encodings = []
    face_locations = []
    frame_number = 0
    
    beg_time = time.perf_counter()
    count_compares = 0
    
    while True:
        # Grab a single frame of video
        ret, frame = input_movie.read()
        frame_number += 1
    
        # Quit when the input video file ends
        if not ret:
            break
        
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]
       
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
       
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
        # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
           if len(face_locations) != 0:
                
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            
                name = ' '
                if matches[0]:
                    name = known_face_names[0] 
                    count_compares +=1
                    save_frame(frame,frame_number)
                    print('Совпадение обнаруженo ✓')
            
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            
                # Label the results
                for top, right, bottom, left in face_locations:
                    if not name:
                        # continue
                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 72), 2)
                    else:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 72), 2)
                        # Draw a label with a name below the face
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
            
            # Write the resulting frame to the output video file
        print('Кадр {}/{}'.format(frame_number, length))
        output_movie.write(frame)
        
    end_time = time.perf_counter()
    print(f'\nЗатрачено, с: {end_time - beg_time} \nСравнений: {count_compares}')


if __name__ == '__main__':
    import sys
    try:
        import face_recognition
        import numpy as np
        import cv2
        import time
        import os
        import datetime
        print('Добро пожаловать в программу для распознавания лиц. ver.2\n')
        input_photo = input('Введите имя изображения с указанием формата. Например: test_face.jpg\n') 
        face_photo = face_recognition.load_image_file(input_photo)
        name_photo = input_photo.split('.')[0]
        name_video = input("Введите название видео с указанием формата. Например: test_video.avi\n")
        main(face_photo,name_photo,name_video)
    except Exception:
        import traceback
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback_exception = traceback.TracebackException(exc_type, exc_value, exc_tb)
        print('Сообщение об ошибке', traceback_exception)
    input('Нажмите Enter для выхода')

        