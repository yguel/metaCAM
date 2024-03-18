# Python 3 server example
from io import BytesIO
from flask import Flask, jsonify, request, send_from_directory,send_file,abort
from time import sleep
from PIL import Image,ImageDraw
from matplotlib import pyplot as plt
from ultralytics import YOLO
from threading import Thread
import cv2
import queue
import base64
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from datetime import datetime
import camera_database
import ip_detect
import os


# SETUP GLOBAL VARIABLES
########################
# Path to the model
PATH_TO_MODEL = None
PATH_TO_MODEL0 = "src/yolov8/model/11/best.pt"
PATH_TO_MODEL1 = "../yolov8/model/11/best.pt"
# Path to the frame
FRAME_PATH = None
FRAME_PATH0 = "src/multistream_yolo/frame.jpg"
FRAME_PATH_FLASK = "frame.jpg"          #Flask and prog are not in the same path ??
# Path to the found image
FOUND_PATH0 = "src/multistream_yolo/found.jpg"
FOUND_PATH_FLASK = "found.jpg"
# Path to the camera file
file_camera = None
file_camera0="src/multistream_yolo/cameras.txt"
file_camera1="cameras.txt"

if os.path.isfile(PATH_TO_MODEL0):
    PATH_TO_MODEL = PATH_TO_MODEL0
    FRAME_PATH = FRAME_PATH0
    FOUND_PATH = FOUND_PATH0
    file_camera = file_camera0
else:
    PATH_TO_MODEL = PATH_TO_MODEL1
    FRAME_PATH = FRAME_PATH_FLASK
    FOUND_PATH = FOUND_PATH_FLASK
    file_camera = file_camera1

# END SETUP GLOBAL VARIABLES
############################




app = Flask(__name__)
CORS(app)  
api = Api(app, version='1.0', title='API for glasses detection', description='A simple API to take the last detection of glasses and add cameras',)


os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"



url_camera_hardcode = "http://10.42.0.115:4747/video"




class VideoCapture:

    def __init__(self, ip):
        print("Ici")
        self.cap = cv2.VideoCapture(ip)
        print("Ici2")
        self.q = queue.Queue()
        t = Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            if not self.cap.isOpened():
                self.q.put(None)
                sleep(1)
                continue
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        if self.q.empty():
            return None
        return self.q.get()

    def release(self):
        print("Ici3")
        # self.cap.release()


class Camera:
    def __init__(self, name,place,url):
        self.name = name
        self.place= place
        print("La")
        self.cap = VideoCapture(url)
        print("La2")
        
    def read(self):
        return self.cap.read()
    
    def release(self):
        print("Release camera")
        self.cap.release()
        
def load_cameras(file_camera):
    
    for (a,b,c) in camera_database.get_active_camera():
        print("rtsp://tprli2023:tprli2023@"+a+"/stream1");
        yield Camera(c,b,"rtsp://tprli2023:tprli2023@"+a+"/stream1")
    
    

# Your existing variables and initialization
cameras = []
try:
    model = YOLO(PATH_TO_MODEL)
except Exception as e:
    print("Error loading model")
    print("Wrong path to model ({}) or model not found")
    exit(1)
queue_found = queue.Queue(1)

for cam in load_cameras(file_camera):
    cameras.append(cam)



def analyze_stream_video(model, frame):

    
    # Save the frame as a temporary image file
    cv2.imwrite(FRAME_PATH, frame)
    # Infer on the frame using the provided model
    predictions = model.predict(source=frame, conf=0.65)

    # Create a drawing context

    for result in predictions:
        
        # image = Image.fromarray(result.orig_img).convert("RGB")
        image = Image.open(FRAME_PATH)
        draw = ImageDraw.Draw(image)
        if result.boxes.xyxy.numel() == 0:
            return image,False
        
        for box in result.boxes.xyxy:
            x, y, xmax, ymax = box.tolist()
            width = xmax - x
            height = ymax - y

            # Create a rectangle using Pillow
            draw.rectangle([x, y, xmax, ymax], outline=(255, 0, 0), width=2)

            return image,True        
                    

last_found = None


def loop_detect(queue_found):
    global cameras
    nb_loop = 0
    global last_found
    while True:
        for cam in cameras:
            frame = cam.read()
            if frame is None:
                print("Error cam")
                cameras.remove(cam)
                cam.release()
                sleep(1)
                continue
            img,detected = analyze_stream_video(model, frame)
            if detected :
                last_found = (FOUND_PATH,cam.name,cam.place,datetime.now())
                img.save(FOUND_PATH)
        nb_loop+=1
        if nb_loop % 100 == 0:          #Update the camera (if ip or name change)
            print("Update Camera")
            cameras=[]
            for cam in load_cameras(file_camera):
                cameras.append(cam)    
            sleep(3)            #to avoid to much cpu usage when there is no camera

loop = Thread(target=loop_detect,args=[queue_found])
loop.start()   




model_ask_detection = api.model('AskDetection', {
    'name': fields.String(description='The name of the camera'),
    'path': fields.String(description='The api path to request the image'),
    'place': fields.String(description='The place of the camera'),
    'time': fields.String(description='The amount of time since the detection'),
})

model_new_camera = api.model('NewCamera', {
    'name': fields.String(description='Name of the camera', required=True),
    'place': fields.String(description='Location of the camera', required=True),
    'mac_addr': fields.String(description='Mac address of the camera', required=True),
    'ip_addr': fields.String(description='ip address of the camera', required=True),
})

model_list_camera = api.model('ListCamera', {
    'name': fields.String(description='Name of the camera', required=True),
    'place': fields.String(description='Location of the camera', required=True),
    'ip_addr': fields.String(description='ip address of the camera', required=True),
})


class AskDetection(Resource):
    # New API route to parse and send current detection
    @api.marshal_with(model_ask_detection)
    def get(self):
        """
        Get the last valid detection if exists else return empty response
        """

        # global queue_found
        # Check if there is a valid detection
        global last_found

        valid_detection = {
            'name': '',
            'path': '',
            'place': '',
            'time' : '',
        }
        if last_found is None:
            return valid_detection
        
        cur = datetime.now()
        diff= cur - last_found[3]
        valid_detection = {
            'name': str(last_found[1]),
            'path': '/img_found',  # Include the base64-encoded image         ,
            'place': str(last_found[2]),
            'time' : str(diff),
        }
        return valid_detection
# Add the resource to the API
api.add_resource(AskDetection, '/found')



def add_camera(camera_name, camera_place, camera_mac,camera_ip,file_camera):
    """
    Add a new camera to the list of cameras file.
    """
    global cameras
    camera_database.add_a_camera((camera_mac,camera_ip,camera_place,camera_name,1))


        
            
class NewCamera(Resource):
    @api.expect(model_new_camera)
    def post(self):
        """
        Add a new camera.
        """
        data = api.payload
        camera_name = data.get('name')
        camera_place = data.get('place')
        camera_mac = data.get('mac_addr')
        camera_ip = data.get('ip_addr')

        add_camera(camera_name, camera_place, camera_mac,camera_ip,file_camera)
        
        cameras=[]
        for cam in load_cameras(file_camera):
            cameras.append(cam)
        
        return 
        

# Add the new resource to the API
api.add_resource(NewCamera, '/new_camera')


class ListCamara(Resource):
    def get(self):
        """
        Get the list of cameras.
        """
        ret_cams = []
        for cam in camera_database.get_active_camera():
            ret_cams.append({
                "ip_addr": cam[0],
                "name": cam[2],
                "place": cam[1],
            })
        return ret_cams  
api.add_resource(ListCamara, '/list_camera')


class GetLastFound(Resource):
    def get(self):
        """
        Get the last image where there are glasses.
        """
        try:
            return send_file(FOUND_PATH_FLASK,mimetype='image/jpeg')
        except FileNotFoundError:
            # Si le fichier est pas trouver  renvoyer une erreur 404
            abort(404, description='Image not found')
        except Exception as e:
            # Gerer d autres exceptions ici si necessaire
            abort(500, description='Internal Server Error')

api.add_resource(GetLastFound, '/img_found')

class GetLastFrame(Resource):
    def get(self):
        """
        Get the last frame. Usefull for debug
        """
        try:
            return send_file(FRAME_PATH_FLASK,mimetype='image/jpeg')
        except FileNotFoundError:
            # Si le fichier n est pas trouver, renvoyer une erreur 404
            abort(404, description='Image not found')
        except Exception as e:
            # Gerer d'autres exceptions ici si necessaire
            abort(500, description='Internal Server Error')

        
api.add_resource(GetLastFrame,'/img_frame')

if __name__ == "__main__":
    #get ip of the jetson on the ethernet network
    ip_eth0 = ip_detect.get_eth0_ip()
    app.run(host=ip_eth0,debug=False,threaded=True)

    # Wait for the Flask thread to finish (optional)
