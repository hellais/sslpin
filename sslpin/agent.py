from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.web.error import SchemeNotSupported

from twisted.web.client import Agent, _URI

class _WebToNormalContextFactory(object):
    def __init__(self, webContext, hostname, port, fingerprint):
        self._webContext = webContext
        self._hostname = hostname
        self._port = port
        self._fingerprint = fingerprint

    def getContext(self):
        return self._webContext.getContext(self._hostname, self._port,
                                           self._fingerprint)

class VerifiedAgent(Agent):
    """
    A HTTPS agent that supports httpv or HTTP Verified URLs.
    """
    def _wrapContextFactory(self, host, port, fingerprint):
        return _WebToNormalContextFactory(self._contextFactory, host, port,
                                          fingerprint)

    def request(self, method, uri, headers=None, bodyProducer=None):
        parsedURI = _URI.fromBytes(uri, 443)
        fingerprint, parsedURI.host = parsedURI.host.split(';')
        try:
            endpoint = self._getEndpoint(parsedURI.scheme, parsedURI.host,
                                         parsedURI.port, fingerprint)
        except SchemeNotSupported:
            return defer.fail(Failure())
        parsedURI.scheme = 'https'
        key = (parsedURI.scheme, parsedURI.host, parsedURI.port)
        return self._requestWithEndpoint(key, endpoint, method, parsedURI,
                                         headers, bodyProducer,
                                         parsedURI.originForm)

    def _getEndpoint(self, scheme, host, port, fingerprint):
        kwargs = {}
        if self._connectTimeout is not None:
            kwargs['timeout'] = self._connectTimeout
        kwargs['bindAddress'] = self._bindAddress
        if scheme == 'httpsv':
            return SSL4ClientEndpoint(self._reactor, host, port,
                                      self._wrapContextFactory(host, port,
                                                               fingerprint),
                                      **kwargs)
        else:
            raise SchemeNotSupported("Unsupported scheme: %r" % (scheme,))
