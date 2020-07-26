import logging
import sys
from datetime import datetime, timedelta
from app.model.getInfoSongs import *
from app.model.sparQLib import *

LOG_FILE = datetime.now().strftime("%Y%m%d") + "logfile.log"


class Main:

    def __init__(self,song1,artist1,song2,artist2):
        self.logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler(sys.stdout)
        fh = logging.FileHandler(LOG_FILE)
        self.logger.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

        self.sparq = sparQLSession()
        self.op = getInfoSongs(self.logger,self.sparq)

        self.song1 = song1
        self.artist1 = artist1
        self.song2 = song2
        self.artist2 = artist2

        self.relations = self.op.process(self.song1,self.artist1,self.song2,self.artist2)

 


    def setLogging(self):
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        sh = logging.StreamHandler(sys.stdout)
        fh = logging.FileHandler(LOG_FILE)

        logger.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(sh)
        logger.addHandler(fh)

        return logger

