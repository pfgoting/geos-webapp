from tornado import websocket, web, ioloop
import os

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
)

class MainHandler(web.RequestHandler):
    def get(self):
        self.render('main.html')

def make_app():
    return web.Application([
        (r"/", MainHandler),
        (r'/(test\.html)', web.StaticFileHandler, dict(path=settings['static_path']))
    ],**settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8008)
    ioloop.IOLoop.current().start()