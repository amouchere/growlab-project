from PIL import Image, ImageFont, ImageDraw
from jinja2 import Template
import time
import shutil
import logging
from time import gmtime, strftime
import os

class specimen:
    def __init__(self, text_config, image_config):
        self.text_config = text_config
        self.image_config = image_config

    def save_image(self, filename, image, readings):
        logger = logging.getLogger("growlab")
        with open(filename, 'wb') as file:
            file.write(image.getvalue())

        msg = self.format(readings)

        img = Image.open(filename, "r").convert("RGBA")
        img_draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('roboto/Roboto-Regular.ttf', self.text_config["size"])
        colour = (self.text_config["colour"]["red"] ,self.text_config["colour"]["green"], self.text_config["colour"]["blue"])

        text_size = img_draw.textsize(msg, font)

        pos = (10, 20)
        bg_size = (text_size[0]+30, text_size[1]+50)
        bg_img = Image.new('RGBA', img.size, (0, 0, 0, 0))

        bg_draw = ImageDraw.Draw(bg_img)
        overlay_transparency = 100
        bg_draw.rectangle((pos[0], pos[1], bg_size[0], bg_size[1]), fill=(0, 0, 0, overlay_transparency), outline=(255, 255, 255))
        bg_draw.text(xy=(pos[0]+10, pos[1]+10), text=msg, fill=colour, font=font)

        out = Image.alpha_composite(img, bg_img)
        logger.info("Saving {}..".format(filename))
        r = out.convert('RGB')
        r.save(filename, "JPEG")
        logger.info("Saved {}..OK".format(filename))

    def format(self, readings):
        degree_symbol=u"\u00b0"
        return "#growlab - {}\nTemperature: {:05.2f}{}C \nHumidity: {:05.2f}%".format(readings["time"], readings["temperature"], degree_symbol, readings["humidity"])

    def save_html(self, input_filename, output_path, readings):
        logger = logging.getLogger("growlab")
        img = Image.open(input_filename, "r")

        img = img.resize((int(self.image_config["width"]/2), int(self.image_config["height"]/2)), Image.ANTIALIAS)
        img.save(output_path+"/preview.jpg", "JPEG")

        template_text = ""
        with open("index.jinja", 'r') as file:
            template_text = file.read()

        template = Template(template_text)
        degree_symbol=u"\u00b0"
        vals = {}
        vals["time"] = readings["time"]
        vals["temperature"] = "{:05.2f}{}C".format(readings["temperature"], degree_symbol)
        vals["humidity"] = "{:05.2f}%".format(readings["humidity"])
        vals["uid"] = "{}".format(time.time())

        html = template.render(vals)
        with open(output_path+"/index.html", "w") as html_file:
            html_file.write(html)
            logger.info("Wrote {}..OK".format(output_path+"/index.html"))

    def copyFile(self, old_path, new_directory):
        logger = logging.getLogger("growlab")
        # check if the directory already exists
        if not os.path.exists(new_directory):
            os.mkdir(new_directory)
            logger.info("Directory {} Created.".format(new_directory))
        else:    
            logger.info("Directory {} already exists..".format(new_directory))

        # create new path from new_directory, the filename and the timestamp
        new_path = new_directory + strftime("%Y-%m-%d_%H-%M-%S_", gmtime()) + "timelapse.jpg"

        # copy the file to the new path
        try:
            shutil.copy(old_path, new_path)
        # eg. src and dest are the same file
        except shutil.Error as e:
            print(f"Error: {e}")
        # eg. source or destination doesn't exist
        except IOError as e:
            print(f"Error: {e.strerror}")