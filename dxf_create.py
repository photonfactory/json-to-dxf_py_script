import json
from pprint import pprint
import sys
import ezdxf
import math

# 111.65.228.94

# set parameters
laser_spot_diameter = 0.1  # mm

if not len(sys.argv) == 2:
    print "WARNING: no json filename entered as argument"
    json_data = open('6a047043-836b-46d7-99cb-6cc5cb0f903a.json')
    file_name = '6a047043-836b-46d7-99cb-6cc5cb0f903a.json'
    print "defaulting to: " + '6a047043-836b-46d7-99cb-6cc5cb0f903a.json'
else:
    json_data = open(str(sys.argv[1]))
    file_name = str(sys.argv[1])

data = json.load(json_data)
pprint(data)
print len(data)

dwg = ezdxf.readfile("template.dxf")
modelspace = dwg.modelspace()

for entity in data:
    if entity['type'] == "line":
        print "found a line, so drawing one into the dxf file"
        modelspace.add_line([entity['p1']['x'], entity['p1']['y']], [entity['p2']['x'], entity['p2']['y']])
    if entity['type'] == "well":
        print "found a well, so drawing one into the dxf file"
        for i in range(0, int(math.floor(entity['r']/laser_spot_diameter)-1)):
             modelspace.add_circle([entity['p1']['x'], entity['p1']['y']], entity['r']-laser_spot_diameter*(i+1))
    if entity['type'] == "circle":
        print "found a cicle, so drawing one into dxf file"
        modelspace.add_circle([entity['p1']['x'], entity['p1']['y']], entity['r'])
    if entity['type'] == "rect":
        print "found a rectangle, so drawing one into dxf file"
        modelspace.add_line([entity['p1']['x'], entity['p1']['y']], [entity['p2']['x'], entity['p2']['y']])
        modelspace.add_line([entity['p2']['x'], entity['p2']['y']], [entity['p4']['x'], entity['p4']['y']])
        modelspace.add_line([entity['p4']['x'], entity['p4']['y']], [entity['p3']['x'], entity['p3']['y']])
        modelspace.add_line([entity['p3']['x'], entity['p3']['y']], [entity['p1']['x'], entity['p1']['y']])

#for e in modelspace:
#    print e.dxftype()

json_data.close()

dwg.saveas(file_name + ".dxf")