import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import os, time
# from watcher import main
from threading import Thread
from mapmaker import make_map
 
settingz = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path="templates",
    debug=True
)

wss = []
init = 1
class Monkey(object):
    def __init__(self):
        self._cached_stamp = 0
        self.filename = r'templates\test.html'
        self.ini = init

    def ook(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            print init
            if self.ini == 1:
                self.ini = 0
            else:
                wsSend("An event has been recorded.")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def func(self):
        print "ws connected! ez"

    def open(self):
        print "ws connected! ez"
        # self.func()
        if self not in wss:
            wss.append(self)
        # pub = Monkey()
        # while True:
        #     try:
        #         pub.ook()
        #         time.sleep(2)
        #     except KeyboardInterrupt:
        #         print "Done"
        #         break

 
    def on_message(self, message):
        self.write_message(message)
        print message
 
    def on_close(self):
        if self in wss:
            wss.remove(self)

 
 
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


def wsSend(message):
    for ws in wss:
        if not ws.ws_connection.stream.socket:
            print "Web socket does not exist anymore!!!"
            wss.remove(ws)
        else:
            ws.write_message(message)

 
 
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/(test\.html)', tornado.web.StaticFileHandler, dict(path='templates')),
            (r'/websocket', WebSocketHandler)
        ]

        settings = settingz
        # settings = {
        #     'template_path': 'templates',
        #     'debug': True
        # }
        tornado.web.Application.__init__(self, handlers, **settings)

def start_app():
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

def monkey():
    pub = Monkey()
    print "MONKAAAS"
    while True:
        try:
            pub.ook()
            time.sleep(2)
        except KeyboardInterrupt:
            print "Done"
            break

 
 
if __name__ == '__main__':


    t2 = Thread(target=start_app)
    t2.daemon = True
    t2.start()

    t1 = Thread(target=monkey)
    t1.daemon = True
    t1.start()

    while True:
        time.sleep(1)

    # start_app()
    # try:
    #     ws_app = Application()
    #     server = tornado.httpserver.HTTPServer(ws_app)
    #     server.listen(8080)
    #     tornado.ioloop.IOLoop.instance().start()
    # except KeyboardInterrupt:  
    #     my_ioloop = tornado.ioloop.IOLoop.current()
    #     my_ioloop.close(all_fds=True)





