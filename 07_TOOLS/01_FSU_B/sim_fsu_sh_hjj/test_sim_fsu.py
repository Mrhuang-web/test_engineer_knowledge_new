#-*- coding:utf-8 -*-
from suds.client import Client
import requests
url = 'http://10.1.24.7:8080/?wsdl'
client = Client(url)

soap_env = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:fsus="http://FSUService.chinamobile.com">
   <soapenv:Header/>
   <soapenv:Body>
      <fsus:invoke>
         <fsus:xmlData><![CDATA[%s]]>
</fsus:xmlData>
      </fsus:invoke>
   </soapenv:Body>
</soapenv:Envelope>
'''

somestr = '''<?xml version="1.0" encoding="UTF-8"?>
<Request>
	<PK_Type>
		<Name>LOGIN</Name>
	</PK_Type>
	<Info>
		<UserName/>
		<PassWord/>
		<FSUID/>
		<FSUIP/>
        <FSUMAC/>
		<FSUVER/>
	</Info>
</Request>
'''

def suds_test():
    result = client.service.invoke(somestr)
    print(result)

def str_test():
    result2 = requests.post(url,soap_env % somestr)
    print(result2.content)

if __name__=='__main__':
    suds_test()
    str_test()