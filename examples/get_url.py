from twisted.internet import reactor

from sslpin.contexts import VerifiedClientContextFactory
from sslpin.agent import VerifiedAgent

def display(response):
    print "Received response"
    print response
    reactor.stop()

def error(failure):
    print failure.value[0][0].value

invalid_url = "httpsv://1=FOHJK3CO4R7Z2XA6AWXI5V7ZLVD4EH4A;twitter.com"
valid_url = "httpsv://1=FOWJK3CO4R7Z2XA6AWXI5V7ZLVD4EH4A;twitter.com"

contextFactory = VerifiedClientContextFactory()
agent = VerifiedAgent(reactor, contextFactory)
d = agent.request("GET", invalid_url)
d.addCallbacks(display, error)
d.addCallback(lambda ignored: reactor.stop())

reactor.run()
