import asyncore
import socket
from controller import get_blobs

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        print "First"
        data = self.recv(8192)
        if data:
            while True:
                self.send("HERE\n")
                b = get_blobs()
                if b:
                    self.send(str(b))

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        print "handle_accept"
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

s = EchoServer('192.168.0.107', 8080)
asyncore.loop()
