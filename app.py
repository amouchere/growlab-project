#!/bin/python3

import json, logging, os, sys 
import pytz
from time import sleep
from sensors import sensors
from camera import camera
from specimen import specimen
from preview import preview
from homedata import homedata
from datetime import datetime

def main():
    # Create logger
    logging.basicConfig(filename='/home/pi/growlab.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.getLogger("growlab")

    print("-----------")
    logging.info("================")
    logging.info("Starting growlab")
    logging.info("================")

    logging.info(os.getcwd())

    # Parse config file
    config = {}
    try:
        with open("./config.json") as f:
            config = json.loads(f.read())
    except Exception as e:
        logging.error("Error: {}".format(e))
        sys.exit(1)

    logging.info("Loaded config, saving images every {} seconds to {}".format( config["timelapse"]["interval_seconds"], config["images"]["output_directory"]))

    # initialize objects
    capt = sensors()
    prev = preview(config["preview"])
    hmdata = homedata(config["homedata"])
    cam = camera(config["images"])
    spec = specimen(config["text"], config["images"])
    pwd = os.getcwd()


    while True:
        
        tz_Paris = pytz.timezone('Europe/Paris')
        datetime_Paris = datetime.now(tz_Paris)
        hour = datetime_Paris.hour

        if (config["timelapse"]["start"] <= hour <= config["timelapse"]["end"]):
            logging.info("Current hour: {}. A capture is possible.".formmat(hour))
            logging.info("New capture in progress ... ")
            # get sensors data
            readings = capt.get_readings()
            logging.info(readings)

            # Send sensors data to homedata application
            hmdata.send(readings)
            
            # get new image
            cam = camera(config["images"])
            frame = cam.get_frame()

            # Save image with incrusted data from sensors
            spec.save_image("{}/image.jpg".format(pwd), frame, readings)
            logging.info("=== Image capturing : done")
            
            # Archive for timelapse 
            if (config["timelapse"]["active"]=="true"):
                spec.copyFile("{}/image.jpg".format(pwd), config["images"]["output_directory"])
                logging.info("=== Image archiving : done")
            else:
                logging.info("=== Image archiving : disabled")

            # Build preview files (image )
            prev.check_preview_directory()
            spec.save_html("{}/image.jpg".format(pwd), config["preview"]["git_dir"], readings)
            logging.info("=== Preview files : done")

            # Publish the preview
            prev.publish_preview()
            logging.info("=== Preview publishing : done")
                      
        else:
            logging.info("Current hour: {} No image between {} and {}".format(hour, config["timelapse"]["start"], config["timelapse"]["end"]))

        logging.info("... sleep for {} seconds".format(config["timelapse"]["interval_seconds"]))
        sleep(config["timelapse"]["interval_seconds"])

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logging.error(type(e).__name__)
            raise e
