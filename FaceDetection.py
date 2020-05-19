from PIL import Image
import face_recognition

def detect(filename):
    image = face_recognition.load_image_file(filename)

    # Find all the faces in the image using the default HOG-based model.
    # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
    face_locations = face_recognition.face_locations(image)

    #print("I found {} face(s) in this photograph.".format(len(face_locations)))
    return(image,face_locations,len(face_locations))
