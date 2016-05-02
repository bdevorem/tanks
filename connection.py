from main import GameSpace
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall

class ServerConnFactory(Factory):
	def __init__(self, gs):
		self.gs = gs

	def buildProtocol(self, addr):
		self.addr = addr
		self.conn = ServerConnection(addr, self.gs)
		return self.conn

class ServerConnection(Protocol):
	def __init__(self, addr, gs):
		self.addr = addr
		self.gs = gs

	def connectionMade(self):
		print "connection made"
		self.gs.start()
		lc = LoopingCall(self.gs.tick)
		lc.start(1/60)

	def dataReceived(self, data):
		self.gs.addData(data)

	def send(self, data):
		self.transport.write(data)

	def connectionLost(self, reason):
		print "lost connection"

class ClientConnFactory(ClientFactory):
	def __init__(self, gs):
		self.gs = gs

	def buildProtocol(self, addr):
		self.addr = addr
		self.conn = ClientConnection(addr, self.gs)
		return self.conn

class ClientConnection(Protocol):
	def __init__(self, addr, gs):
		self.addr = addr
		self.gs = gs

	def connectionMade(self):
		print "connection made"
		self.gs.start()
		lc = LoopingCall(self.gs.tick)
		lc.start(1/60)

	def dataReceived(self, data):
		self.gs.addData(data)

	def send(self, data):
		self.transport.write(data)

	def connectionLost(self, reason):
		print "lost connection"


