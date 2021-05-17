#!/bin/python3

import json, logging, os, sys 
import pytz
from time import sleep
from captors import captors
from camera import camera
from specimen import specimen
from preview import preview
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

    logging.info("Loaded config, saving images every {} seconds to {}".format( config["time"]["interval_seconds"], config["images"]["output_directory"]))

    # initialize objects
    capt = captors()
    prev = preview(config["preview"])
    cam = camera(config["images"])
    spec = specimen(config["text"], config["images"])
    pwd = os.getcwd()


    while True:
        
        tz_Paris = pytz.timezone('Europe/Paris')
        datetime_Paris = datetime.now(tz_Paris)
        hour = datetime_Paris.hour

        if (config["time"]["start"] < hour < config["time"]["end"]):
            logging.info("Current hour: {}. A capture is possible.")
            logging.info("New capture in progress ... ")
            # get captors data
            readings = capt.get_readings()
            logging.info(readings)

            # get new image
            cam = camera(config["images"])
            frame = cam.get_frame()

            # Save image with incrusted data from sensors
            spec.save_image("{}/image.jpg".format(pwd), frame, readings)
            logging.info("=== Image capturing : done")

            # # Archive for timelapse 
            spec.copyFile("{}/image.jpg".format(pwd), config["images"]["output_directory"])
            logging.info("=== Image archiving : done")

            # Build preview files (image )
            prev.check_preview_directory()
            spec.save_html("{}/image.jpg".format(pwd), config["preview"]["git_dir"], readings)
            logging.info("=== Preview files : done")

            # Publish the preview
            prev.publish_preview()
            logging.info("=== Preview publishing : done")
                      
        else:
            logging.info("Current hour: {} No image between {} and {}".format(hour, config["time"]["start"], config["time"]["end"]))

        logging.info("... sleep for {} seconds".format(config["time"]["interval_seconds"]))
        sleep(config["time"]["interval_seconds"])

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logging.error(type(e).__name__)
            raise e
