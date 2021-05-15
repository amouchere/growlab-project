import os, subprocess, logging
from subprocess import check_output
from os import mkdir, path
from os.path import isdir

class preview:
    def __init__(self, git_opts):
        self.git_opts = git_opts

    def execute(self, command):
        PIPE = subprocess.PIPE

        

        logger = logging.getLogger("growlab")
        try:
            # logger.info(check_output(command, shell=True))
            process = subprocess.Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()

            logger.info(stdoutput)
            logger.error(stderroutput)
        except subprocess.CalledProcessError as err:
            logger.error(err)

    def check_preview_directory(self):
         # Make sure the repo is cloned
        git_dir = self.git_opts["git_dir"]
        git_path = self.git_opts["git_path"]

        if not isdir(git_dir):
            mkdir(git_dir)
            command = "git clone {} {}".format(git_path, git_dir)
            self.execute(command)


    def publish_preview(self):
        git_dir = self.git_opts["git_dir"]


        command = "cd {} && git pull".format(git_dir)
        self.execute(command)

        # Commit and push
        command = "cd {} && git add . && git commit -m ':bento: Update preview' && git push -f".format(git_dir)
        self.execute(command)
