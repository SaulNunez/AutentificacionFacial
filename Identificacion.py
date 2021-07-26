import face_recognition

import cv2

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# Get a reference to webcam
video_capture = cv2.VideoCapture(0)

# Load authorized user picture, and encode the image so the face recognition can recognize it
auth_image = face_recognition.load_image_file("saul.jpg")
auth_face_encoding = face_recognition.face_encodings(auth_image)[0]

auth_image_2 = face_recognition.load_image_file("brenda.jpg")
auth_face_encoding_2 = face_recognition.face_encodings(auth_image_2)[0]

auth_image_3 = face_recognition.load_image_file("fernando.jpg")
auth_face_encoding_3 = face_recognition.face_encodings(auth_image_3)[0]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
found_authorized_user = False

while True:
    # Grab a frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([auth_face_encoding, auth_face_encoding_2, auth_face_encoding_3], face_encoding)
            name = "Unknown";
            if match[0]:
                name = "Saul"
                found_authorized_user = True
            if match[1]:
                name = "Brenda"
                found_authorized_user = True
            if match[2]:
                name = "Fernando"
                found_authorized_user = True
            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if (cv2.waitKey(1) & 0xFF == ord('q')) or found_authorized_user:
        break

print(found_authorized_user)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
