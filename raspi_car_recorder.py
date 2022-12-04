# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from datetime import datetime
import os
import gps
import cv2

import threading


datadir = 'data/'


class DataRecorder:
    def __init__(self, max_dur=20):
        self.is_started = False
        self.max_duration = max_dur  # maximum number of seconds to collect data
        
        # time metadata and save folder
        self.start_datetime = datetime.now()
        self.script_start_datetime = self.start_datetime.strftime("%m-%d-%Y_%H:%M:%S")
        self.start_timestamp = datetime.timestamp(self.start_datetime)

        # save folder and filenames
        self.script_start_datedir = os.path.join(datadir, self.start_datetime.strftime("%m-%d-%Y"))
        os.makedirs(self.script_start_datedir, exist_ok=True)
        self.gps_filepath = os.path.join(self.script_start_datedir, f'GPS_{self.script_start_datetime}.csv')
        self.video_filepath = os.path.join(self.script_start_datedir, f'camera_{self.script_start_datetime}.mp4')
        
        # sensor params -- TODO put in config file
        self.fps = 20
        self.camera_resolution = (640, 480)  # change when better camera
        # self.camera_resolution = (1920, 1080)  # change when better camera

        threading.Thread(self.initialize_gps())
        threading.Thread(self.initialize_camera(self.fps, self.camera_resolution))




    def initialize_gps(self):
        # TODO update to gps3
        # Listen on port 2947 (gpsd) of localhost
        self.gps_session = gps.gps("localhost", "2947")
        self.gps_session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        self.gps_writer = open(self.gps_filepath, 'w')
        self.gps_writer.write('latitude,longitude,gps_timestamp\n')
        self.lats = []
        self.longs = []
        print("Started GPS")
        while True:
            self.record_gps()


    def initialize_camera(self, fps=20, resolution=(1920, 1080)):
        self.camera_writer = cv2.VideoWriter(self.video_filepath, cv2.VideoWriter_fourcc(*'mp4v'), fps, resolution, True)
        self.camera_stream = cv2.VideoCapture(0)  # defaults to first input stream

        codec = cv2.VideoWriter_fourcc(	'M', 'J', 'P', 'G'	)
        self.camera_stream.set(6, codec)
        self.camera_stream.set(5, fps)
        self.camera_stream.set(3, resolution[0])
        self.camera_stream.set(4, resolution[1])
        self.num_camera_frames = 0
        print("Started camera")

    def record_gps(self):
        try:
            report = self.gps_session.next()
            # Wait for a 'TPV' report and display the current time
            while report['class'] != 'TPV' or report['mode'] <= 1:
                report = self.gps_session.next()

            local_timestamp = datetime.timestamp(datetime.now())
            lat = report['lat']
            lon = report['lon']
            self.lats.append(lat)
            self.longs.append(lon)

            # store data in csv file
            self.gps_writer.write(f'{lat},{lon},{local_timestamp}\n')

            if local_timestamp - self.start_timestamp > self.max_duration:
                print(f"{self.max_duration} seconds elapsed")

        except Exception as e:
            print("Error with gps recording")
            print(e)
            print("GPSD has terminated")
        
    def record_camera(self):
        ret, frame = self.camera_stream.read()
        if ret:
            self.camera_writer.write(frame)
            self.num_camera_frames += 1
            # cv2.imshow('Video', frame)  # debugging, remove later
        else:
            print("No camera found")
            # ret, frame = self.camera_stream.read()
            # if cv2.waitKey(1) & 0xFF==ord("q"):
            #     break
            # if not self.is_started:
            #     break
        print(f"{self.num_camera_frames} frames recorded")

    def shutdown_gps(self):
        self.gps_session = None
        self.gps_writer.close()
        print("GPS has terminated")

    def shutdown_camera(self):
        self.camera_stream.release()
        self.camera_writer.release()
        cv2.destroyAllWindows() # remove later
        print("Camera has terminated")
                    




# add a callback to external on/off button
# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
# GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

recorder = DataRecorder()

for i in range(5000):
    recorder.record_gps()
    recorder.record_camera()

recorder.shutdown_gps()
recorder.shutdown_camera()

recorder.write_gps_route_to_image()