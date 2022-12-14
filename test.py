import json
import os
import sys
import argparse
import subprocess
import string

import threading
import numpy as np
import cv2
import time
from threading import Thread, Lock
from queue import Queue
import random
from datetime import datetime

from modules.logger.logger import Logger
from modules.json_reader.json_reader import JsonReader
from modules.firebase_api.firebase_api import Firebase_API
from modules.command.command import LocalCommand
from modules.MongoDB_API.MongoDB_API import mongo_dbs
from modules.file.file import File

g_script_dir = ""
g_script_base_name = os.path.basename(__file__)
script_dir_name = os.path.dirname(__file__)
script_full_name = os.path.join(script_dir_name, g_script_base_name)
if os.path.islink(script_full_name):
  g_script_dir = os.path.dirname(os.path.realpath(script_full_name))
else:
  g_script_dir = os.path.dirname(os.path.abspath(script_full_name))
g_test_config_dir = os.path.join(g_script_dir, "test_config")

g_description = \
"""
jetsonxavier Application
"""

g_version = """App v1.0.0
Author: Le Tu Ngoc Minh
Email: ..."""

g_log_file = os.path.join(script_dir_name, "log/testing.log")
g_log_level_guide = """specify wanted log level.
Supported log levels: debug, info, warn, error, critical
"""
g_log_level = "INFO"
g_quiet = False

def exit_program(exit_msg="Exit program!", exit_code=0):
  print(exit_msg)
  sys.exit(exit_code)

def show_version():
  print(g_version)

FILENAME_LENGTH = 6
def generate_random_string(string_length):
    return ''.join(random.choices(string.ascii_letters, k=string_length))

class Argument:
    def __init__(self, images_capture_dir, root_workspace, file_module, command_module, fb, mongodb_api):
        self.images_capture_dir = images_capture_dir
        self. root_workspace = root_workspace
        self.file_module = file_module
        self.command_module = command_module
        self.fb = fb
        self.mongodb_api = mongodb_api


#init camera

FIRST_CAM = 0
SECOND_CAM = 2



QRcam = cv2.VideoCapture(FIRST_CAM)
Facecam = cv2.VideoCapture(SECOND_CAM)


def QRThread(q, argm):
    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()
    while True:
        _, img = QRcam.read()
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if data:
            a = data
            print(a)
            pass
        cv2.imshow("QRCODEscanner", img)   
        if cv2.waitKey(1) == ord("q"):
            break


def IRThread(q, argm):

    while True:
        # Capture the video frame
        # by frame
        ret, frame = Facecam.read()
    
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

       

if __name__ =="__main__":
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=g_description)
    arg_parser.add_argument("-v", "--version", dest="version", action="store_true", help="show version of this framework")
    arg_parser.add_argument("-lf", "--log-file", dest="log_file",
                          nargs=1, type=str, required=False, default=None,
                          help="specify the path for log file")
    arg_parser.add_argument("-lv", "--log-level", dest="log_level",
                          nargs=1, type=str, required=False, default=None,
                          help=g_log_level_guide)
    arg_parser.add_argument("-q", "--quiet", dest="quiet",
                          action="store_true", default=False,
                          help="don't print console log")
    args = arg_parser.parse_args()

    if len(sys.argv) == 1:
        script_name = os.path.basename(__file__)
        print('No option was provided, start running with all default settings')

    if args.version:
        show_version()
        exit_program()

    if args.log_file:
        g_log_file = args.log_file[0]

    if args.log_level:
        if args.log_level[0] in ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]:
            g_log_level = args.log_level[0].upper()

    if args.quiet:
        g_quiet = True


    local_command = LocalCommand()
    test_config = os.path.join(g_test_config_dir, "test_config.json")
    if os.path.isfile(test_config):
        os.environ['ROOT_WORKSPACE'] = g_script_dir
        jsonreader = JsonReader()
        jsonreader.read_json_file(test_config)
        #init firebase
        dir_environment = jsonreader.get_value_by_key('DirEnvironment')
        fb_config  = jsonreader.get_value_by_key('FireBaseConfig')

        firebase_storage = Firebase_API(
            Accountkey= fb_config['ServiceAccountKey'],
            storagebucket= fb_config['storagebucket']
        )
        #init mongodb
        mongodb_config = jsonreader.get_value_by_key('MongoDBConfig')
        connection_string = mongodb_config['connection_string']
        mongodb_password = mongodb_config['password']
        mongodb_connection_string = connection_string.replace(r'<password>', mongodb_password)
        db_name = mongodb_config['dbname']

        mgdbs = mongo_dbs(mongodb_connection_string, db_name)

        #init file
      
        file_module = File.Local()
        #init Argument
        argm = Argument(dir_environment['images_capture'], os.environ['ROOT_WORKSPACE'], file_module, local_command, firebase_storage, mgdbs )

        q = Queue()
        t1 = threading.Thread(target=QRThread, args =(q, argm))
        t2 = threading.Thread(target=IRThread, args =(q, argm))    
        # starting threads
        t2.start()
        t1.start()
        # wait until all threads finish
        t1.join()
        t2.join()    


        QRcam.release()
        Facecam.release()
        cv2.destroyAllWindows()
    else:
        exit_program("Missing test configuration file!", 1)

    # local_command.exec('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')
