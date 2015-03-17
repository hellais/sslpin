from .schema import fingerprint_to_base32, base32_to_fingerprint

from OpenSSL import SSL
from twisted.internet import ssl

class DetectClientContextFactory(ssl.ClientContextFactory):
    def __init__(self, d):
        self.d = d
        self.certs = {}

    def getContext(self):
        def verify_callback(connection, x509, errnum, depth, ok):
            self.certs[depth] = x509
            if int(depth) == 0:
                self.d.callback(self.certs)
            return True

        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.set_verify(SSL.VERIFY_PEER, verify_callback)
        return ctx

class VerifiedClientContextFactory(ssl.ClientContextFactory):
    def getContext(self, host, port, fingerprint):
        depth, base32_fingerprint = fingerprint.split('=')
        depth = int(depth)
        fingerprint = base32_to_fingerprint(base32_fingerprint)
        def verify_callback(connection, x509, errnum, errdepth, ok):
            if errdepth == depth and fingerprint != x509.digest('sha1'):
                raise SSL.Error("Invalid fingerprint for %s: %s" % (host, x509.digest('sha1')))
            else:
                return True

        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.set_verify(SSL.VERIFY_PEER, verify_callback)
        return ctx
