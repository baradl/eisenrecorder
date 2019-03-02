import os
import shutil


directory = "C:/Users/basti/OneDrive/Dokumente/TrainingLogDB/scripts/__pycache__"


if os.path.exists(directory):
    shutil.rmtree(directory)
    
