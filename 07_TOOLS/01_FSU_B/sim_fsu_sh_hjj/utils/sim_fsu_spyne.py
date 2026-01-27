#-*- coding:utf-8 -*-
'''pip install spyne
目前的问题是xmlData自动生成时，总是带ns, 导致与实际不太相符
'''
import spyne
from spyne import Application
from spyne import rpc
from spyne import ServiceBase
from spyne import String, Iterable, Integer, Unicode
from spyne.model import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import hashlib
import logging
from lxml import etree
from control import invoke_proxy

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='[%Y-%m-%d %H:%M:%S]',
                    #filename='sim_fsu.log',
                    )
logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
#logging.getLogger('spyne.application.server').setLevel(logging.DEBUG)


class FSUServiceService(ServiceBase):
    @rpc(Unicode,
    #_in_message_name = 'invoke',
    _operation_name = 'invoke',
    #_out_message_name = 'invokeResponse',
    _out_variable_name = 'invokeReturn',
    _returns = Unicode,

    )
    def invoke(self,xmlData):
        logging.info("xmlData: %s" % xmlData)
        et = etree.fromstring(xmlData.encode('utf-8'))
        response  = invoke_proxy(et)
        return response


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    soap_app = Application(services = [FSUServiceService],
                           tns = 'http://FSUService.chinamobile.com',
                           name = 'FSUServiceSoapBinding',
                           in_protocol = Soap11(validator='lxml'),
                           out_protocol = Soap11(),
    )
    soap_app.interface.nsmap['soapenv'] = soap_app.interface.nsmap['soap11env']     #没什么作用
    wsgi_app = WsgiApplication(soap_app)
    server = make_server('0.0.0.0', 8080, wsgi_app)
    server.serve_forever()
