import socket
import tornado.httpserver
import tornado.websocket
import torando.ioloop
import tornado.web

class MessageHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'User connected'

    def on_messsage(self, message):
        print 'Message: %s'
        #echo
        self.write_message(message[::-1])

    def on_close(self):
        return True

    #def check_origin(self):
     #   return True


app = tornado.web.Application([r'/', MessageHandler])

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8087)
    host = socket.gethostbyname(socket.gethostname())
    print 'Echo server IP: %s' % host
    tornado.ioloop.IOLoop.instance.start()
