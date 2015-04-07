import ssl
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):

        self.poolmanager = PoolManager(num_pools = connections,
                                       maxsize = maxsize,
                                       block = block,
                                       ssl_version = ssl.PROTOCOL_TLSv1)

def get_session():

    session = requests.session()

    session.mount("https://", SSLAdapter())

    return session
