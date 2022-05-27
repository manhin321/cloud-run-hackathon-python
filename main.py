
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request


#### User defined variable
def premove(dimension, direction, location):
    move = "R"
    need_turn = False
    xx, yy =  dimension
    x, y = location
    if(x == xx-1 or y == yy-1 or x == 0 or y == 0):  # no need move, just turn
        if(x == 0 and direction != "E"):
            need_turn = True
        elif(x == xx-1 and direction != "W"):
            need_turn = True
        elif(y == 0 and direction != "S"):
            need_turn = True
        elif(y == yy-1 and direction != "N"):
            need_turn = True
    else:
        need_turn = True
        move = "F"
    return move, need_turn

####

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    request.get_data()
    #logger.info(request.json)
    data = request.json
    myself = "https://cloud-run-hackathon-python-7qbsdooeja-uc.a.run.app"
    dimension = data['arena']['dims']

    mydir = data['arena']['state'][myself]['direction']
    mypos = (data['arena']['state'][myself]['x'],  data['arena']['state'][myself]['y'])

    move, need_turn = premove(dimension, mydir, mypos)
    
    logger.info("dim: (%d %d)"%(dimension[0], dimension[1]))
    logger.info("mydir: %s, mypos: (%d %d)"%(mydir, mypos[0], mypos[1]))
    logger.info("move: ", move)
    logger.info(need_turn)

    if(need_turn):
        return move
    else:
        return moves[1]
    #return moves[random.randrange(len(moves))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
