from tornado.tcpclient import TCPClient
from tornado import ioloop, gen, iostream
from tornado.ioloop  import IOLoop
import struct

class TestTcpclient(object):
    """docstring for TestTcpClient"""
    def __init__(self, host,port):
        self.host = host
        self.port = port
 
 
    @gen.coroutine
    def start(self):
        self.stream = yield TCPClient().connect(self.host, self.port)
        #self.login_req()
        self.set_dyn_access_mode_req()

    @gen.coroutine
    def login_req(self):
        SerialsNo = 100001
        username = 'admin'.ljust(20).encode('utf-8')
        password = 'admin'.ljust(20).encode('utf-8')
        for li in range(1,3):
            login_req = struct.pack('<llll20s20sH', 0x7e7c6b5a, 58, SerialsNo, 101, username, password, 0x00)
            self.stream.write(login_req)
            rec=yield self.stream.read_bytes(19)
            print('recive from the server[login_ack]:',rec)
            SerialsNo = SerialsNo + 1

    @gen.coroutine
    def set_dyn_access_mode_req(self):
        SerialsNo = 401001
        length = 18+8+1+8+8*5       #假设5个Cnt, 18个包含pk_type（16+2），剩下的是info的
        TerminalID = 1
        GroupID = 1
        Mode = 2
        PollingTime = 10        #定时方式时的发送间隔秒数
        device_id_list = [528384,]
        Cnt = 1                 #假设取5个设备
        set_req = struct.pack('<lllllllll'+str(Cnt)+'lH', 0x7e7c6b5a, length, SerialsNo, 401, 
                                TerminalID,GroupID,Mode,PollingTime,Cnt,device_id_list[0],0x00)
        self.stream.write(set_req)

        resp_header = yield self.stream.read_bytes(16,partial=True)
        (self.Header, self.Length, self.SerialsNo, self.PK_Type) = struct.unpack('<llll', resp_header)
        print('[unpack header]\n\tHeader:%s\n\tLength:%s\n\tSerialsNo:%s\n\tPK_Type:%s' % (hex(self.Header), self.Length, self.SerialsNo, self.PK_Type))
        self.PK_Body = yield self.stream.read_bytes(self.Length - 16,partial=True)
        print('[DYN_ACCESS_MODE_ACK][body]:', self.PK_Body)
 
def test_main():
    tcp_client = TestTcpclient('127.0.0.1', '8099')
    tcp_client.start()
    IOLoop.instance().start()


if __name__=="__main__":
    test_main()