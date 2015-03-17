class SimpleProtocol(Protocol):
    def connectionMade(self):
        print "Connection made"
        print self.transport.getPeerCertificate()

    def dataReceived(self, data):
        print "Got data.."
        print data


class TLSProtocol(TLSMemoryBIOProtocol):
    def dataReceived(self, data):
        TLSMemoryBIOProtocol.dataReceived(self, data)
        cert = self.getPeerCertificate()
        if cert:
            self.d.callback(cert)
            self.loseConnection()

class TLSFactory(TLSMemoryBIOFactory):
    protocol = TLSProtocol

    def __init__(self, d, *args):
        self.d = d
        TLSMemoryBIOFactory.__init__(self, *args)

    def buildProtocol(self, addr):
        self.protocol.d = self.d
        return TLSMemoryBIOFactory.buildProtocol(self, addr)
