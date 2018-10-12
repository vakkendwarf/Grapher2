import Graph as g
import Sql as s
import sys

version     = "0.1"
argdatev    = sys.argv[1]
argamt      = sys.argv[2]

print("PYTHON INTERFACE (v"+str(version)+") IS NOW CONNECTED")
print("INTERFACE HAS RECIEVED THE FOLLOWING DATE: " + str(argdatev) + " AND AMOUNT: " + str(argamt))

s.insert_into_db(argdatev, argamt)
g.streamit(argdatev, argamt)
