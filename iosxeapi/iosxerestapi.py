import requests
import urllib3
import logging.config

config = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'short': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'short',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'plugins': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    },
}

logging.config.dictConfig(config)

class iosxerestapi(object):
    def __init__(self, host=None, username=None, password=None, port=443):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.logger = logging.getLogger('iosxerestapi')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.host)

    def _execute_call(self, url, method='get'):
        try:
            self.logger.info('Calling {}'.format(url))
            requests.packages.urllib3.disable_warnings()
            url_base = 'https://{0}:{1}/restconf/data/'.format(self.host, self.port)
            headers = {
            'Accept': 'application/yang-data+json',
            'content-type': 'application/yang-data+json'
            }
            if method == 'get':
                response = requests.get(url_base+url, auth=(self.username, self.password), headers=headers, verify=False)

            return response.json()
                #response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
        except Exception as e:
            self.logger.error(e)

    def get_bgp(self):
        return self._execute_call('Cisco-IOS-XE-bgp-oper:bgp-state-data')

    def get_interfaces_oper(self):
        return self._execute_call('Cisco-IOS-XE-interfaces-oper:interfaces')
