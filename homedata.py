import requests, logging, json

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
        
        
        logger.info("request: {} {}".format(self.config["url"], data))

        try:
            x = requests.post(self.config["url"], json.dumps(data))
        except Exception as e:
            logging.error("Error: {}".format(e))

        

        #print the response text (the content of the requested file):
        logger.info("response {}", x.text)


