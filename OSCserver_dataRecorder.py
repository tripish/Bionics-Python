# Program to record motion data from OSC
# Listens on port 9050 (normally the Processing port)
# Stores all data in files in tests/data/

from liblo import *
from OSC import *

from time import *

import json
from datetime import datetime, timedelta

from DataIOClasses import DataWriter, DataReader

startTime = []

timestr = strftime("%Y%m%d-%H%M%S")
filename = 'tests/data/' + timestr + '.txt'
datawriter = DataWriter(filename)
startTime = datetime.now()


# Threaded server code from "serverThread.py" in pyliblo
class MyServer(ServerThread):
    def __init__(self):
        ServerThread.__init__(self, 9050)

    @make_method('/foo', 'ifs')
    def foo_callback(self, path, args):
        i, f, s = args
        print "received message '%s' with arguments: %d, %f, %s" % (path, i, f, s)

    @make_method(None, None)
    def fallback(self, path, args):
        print "received unknown message '%s', '%s'" % (path, args)
        print path
        print args

        msgJSON = {}
        msgJSON['path'] = path
        msgJSON['data'] = args
        msgJSON['time'] = datetime.now()-startTime
        datawriter.addEntry(msgJSON)



try:
    server = MyServer()
except ServerError, err:
    print str(err)
    sys.exit()

server.start()
startTime = datetime.now()


while True:
    try:
        print "loop!"
        sleep(5)
    except KeyboardInterrupt:
        break



server.stop()
datawriter.close()