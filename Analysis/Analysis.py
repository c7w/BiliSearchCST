import os
import json
import pandas
import numpy as np

# - -1. global variables
videos = 0
tags = 0
ups = 0

# - 0. Write Crawlled Result to Dataframe
# --|  videos
# --|  authors
# --|  tags
def GetDataframe():
    global videos, tags, ups
    videos = pandas.read_sql_table('Web_video', "sqlite:///Database/db.sqlite3")
    tags = pandas.read_sql_table('Web_tag', "sqlite:///Database/db.sqlite3")
    ups = pandas.read_sql_table('Web_up', "sqlite:///Database/db.sqlite3")

# - 1. Calculate growth speed of video amount
def Conclusion1():
    idList = np.array(videos['id']) 
    idRepresent = idList // 1000000
    
    # Calc frequencies
    idUnique = np.unique(idRepresent)
    
    
    

if __name__ == "__main__":
    GetDataframe()
    Conclusion1()
