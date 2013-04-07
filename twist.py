from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from controller import get_blobs
 
class IphoneChat(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print "clients are ", self.factory.clients
        while True:
            b = get_blobs()
            print b
            if b:
                s = str(b[0]) + "," + str(b[1])
                print s
                self.message(s)
    def dataReceived(self, data):
        print "received data"
        a = data.split(':')
        print a
        if len(a) > 1:
            command = a[0]
            content = a[1]
 
            msg = ""
            if command == "iam":
                self.name = content
                msg = self.name + " has joined"
 
            elif command == "msg":
                msg = self.name + ": " + content
                print msg
 
            for c in self.factory.clients:
                c.message(msg)

    def message(self, message):
        self.transport.write(message + '\r\n')
 
    def connectionLost(self, reason):
        self.factory.clients.remove(self)
 
factory = Factory()
factory.protocol = IphoneChat
factory.clients = []
reactor.listenTCP(8080, factory)
print "Iphone Chat server started"
reactor.run()
