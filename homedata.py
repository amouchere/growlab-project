import requests, logging

class homedata:
    def __init__(self, config):
        self.config = config

    def send(self, readings):
        logger = logging.getLogger("growlab")

        data = {"location":"growlab","table":[]}
        pairs = readings.items()
        for key, value in pairs:
            if key != "time":
                data["table"].append({"key" :key, "value": value})
        
        x = requests.post(self.config["url"], data)

        #print the response text (the content of the requested file):
        logger.info("request: {} {}".format(self.config["url"], data))
        logger.info("response {}", x.text)


