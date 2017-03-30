#! -*- coding: utf-8 -*-
# from ttypes import *
from thrift.Thrift import TProcessor, TApplicationException, TType, TMessageType
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None


class InterFace(object):
    """
        remote call base class
    """
    def standard(self, predicate, pendings):
        """
        Parameters:
        - predicate
        - pendings
        """
        pass


class Client(InterFace):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def stand(self, predicate, pendings, func_str, result_cls, args_cls):
        """
        Parameters:
         - predicate
         - pendings
         - func_str :  called function name str
         - result_cls : class for result  base
         - args_cls : class for args base
        """
        self.stand_send(predicate, pendings, func_str, args_cls)
        return self.stand_recv(func_str, result_cls)

    def stand_send(self, predicate, pendings, func_str='', args_cls=None):
        self._oprot.writeMessageBegin(func_str, TMessageType.CALL, self._seqid)
        args = args_cls()
        args.predicate = predicate
        args.pendings = pendings
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def stand_recv(self, func_str='', result_cls=None):
        (fname, mtype, rseqid) = self._iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(self._iprot)
            self._iprot.readMessageEnd()
            raise x
        result = result_cls()
        result.read(self._iprot)
        self._iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationException.MISSING_RESULT, "recv %s failed: unknown result" % func_str)


class Processor(InterFace, TProcessor):

    def __init__(self, handler, call_map={}):
        """
           - call_map: {"call_name_str": "func str"}
        """
        self._handler = handler
        self._processMap = dict()
        for call_name in call_map.keys():
            self._processMap[call_name] = Processor.process_get_task            # need change w

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name, ))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_get_task(self, seqid, iprot, oprot, func_str='', args_cls=None, result_cls=None):
        args = args_cls()                # need rewrite for args cls
        args.read(iprot)
        iprot.readMessageEnd()
        result = result_cls()
        func_call = getattr(self._handler, func_str, None)
        if func_call:
            result.success = func_call(args.predicate, args.pendings)
        oprot.writeMessageBegin(func_str, TMessageType.REPLY, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


class BaseGetDeal(object):

    thrift_spec = ()

    def __init__(self, success=None, predicate=None, pendings=None, func_str='', cls_str='', thrift_spec=()):
        self.success = success
        self.func_str = func_str
        self.cls_str = cls_str
        self.predicate = predicate
        self.pendings = pendings
        self.thrift_spec = thrift_spec

    def __repr__(self):
        lst = ['%s=%r' % (key, value) for key, value in self.__dict__.iteritems()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(lst))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated \
                and self.thrift_spec is not None \
                and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('%s_result', self.func_str)
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.LIST, 0)
            oprot.writeListBegin(TType.STRUCT, len(self.success))
            for iter6 in self.success:
                iter6.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated \
                and isinstance(iprot.trans, TTransport.CReadableTransport) \
                and self.thrift_spec is not None \
                and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.LIST:
                    self.success = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in xrange(_size0):
                        self.read(iprot)
                        self.success.append(self)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()


