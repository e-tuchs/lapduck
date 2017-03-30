#! -*- coding: utf-8 -*-
from rpccore.gen import Links
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from multiprocessing.synchronize import Lock

_lock = Lock()


class LinksHandler(Links.InterFace):

    DEFAULT_PORT = 9990

    def getStand(self, predicate, pendings):
        try:
            _lock.acquire()
            print "do something"
            return
        finally:
            _lock.release()


handler = LinksHandler()
processor = Links.Processor(handler)
transport = TSocket.TServerSocket(port=LinksHandler.DEFAULT_PORT)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print "Starting server..."
server.serve()
