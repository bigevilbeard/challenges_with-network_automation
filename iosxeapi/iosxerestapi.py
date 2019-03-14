import requests
import urllib3
import logging.config
import json

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

class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val

class iosxerestapi(object):
    def __init__(self, host=None, username=None, password=None, port=443):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.logger = logging.getLogger('iosxerestapi')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.host)

    def _execute_call(self, url, method='get', data=None):
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
            if method == 'patch':
                response = requests.patch(url_base+url, auth=(self.username, self.password), headers=headers, verify=False, data=data)
            if method == 'delete':
                response = requests.delete(url_base+url, auth=(self.username, self.password), headers=headers, verify=False, data=data)

            return response.json()
                #response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
        except Exception as e:
            self.logger.error(e)

    def get_bgp(self):
        """Function to get BGP information on IOS XE"""
        neighbors_list = dict()
        neighbors_list['Cisco-IOS-XE-bgp-oper:bgp-state-data'] = {'neighbors':[]}
        neighbors = DictQuery(self._execute_call('Cisco-IOS-XE-bgp-oper:bgp-state-data')).get('Cisco-IOS-XE-bgp-oper:bgp-state-data/neighbors/neighbor')
        # return neighbors
        # return self._execute_call('Cisco-IOS-XE-bgp-oper:bgp-state-data')
        for neighbor in neighbors:
            dict_temp = {}
            dict_temp['neighbor-id'] = neighbor.get('neighbor-id',None)
            dict_temp['link'] = neighbor.get('link',None)
            dict_temp['up-time'] = neighbor.get('up-time',None)
            dict_temp['state'] = DictQuery(neighbor.get('connection')).get('state')
            dict_temp['total-prefixes'] = DictQuery(neighbor.get('prefix-activity')).get('received/total-prefixes')
            neighbors_list['Cisco-IOS-XE-bgp-oper:bgp-state-data']['neighbors'].append(dict_temp)

        return json.dumps(neighbors_list, sort_keys=False, indent=4)


    def get_interfaces_oper(self):
        """Function to get interface information on IOS XE"""
        # return self._execute_call('Cisco-IOS-XE-interfaces-oper:interfaces')
        interfaces_list = dict()
        interfaces_list['Cisco-IOS-XE-interfaces-oper:interfaces'] = {'interface':[]}
        interfaces = DictQuery(self._execute_call('Cisco-IOS-XE-interfaces-oper:interfaces')).get('Cisco-IOS-XE-interfaces-oper:interfaces/interface')

        for interface in interfaces:
            dict_temp = {}
            dict_temp['name'] = interface.get('name')
            dict_temp['description'] = interface.get('description')
            dict_temp['ipv4'] = interface.get('ipv4')
            dict_temp['vrf'] = interface.get('vrf')
            dict_temp['admin-status'] = interface.get('admin-status')
            dict_temp['input-security-acl'] = interface.get('input-security-acl')
            dict_temp['output-security-acl'] = interface.get('output-security-acl')
            dict_temp['in-discards'] = interface.get('in-discards')
            dict_temp['in-errors'] = interface.get('in-errors')
            dict_temp['out-discards'] = interface.get('out-discards')
            dict_temp['out-errors'] = interface.get('out-errors')
            dict_temp['in-pkts'] = interface.get('in-pkts')
            dict_temp['out-pkts'] = interface.get('out-pkts')

            interfaces_list['Cisco-IOS-XE-interfaces-oper:interfaces']['interface'].append(dict_temp)

        return json.dumps(interfaces_list, sort_keys=False, indent=4)

    def add_access_group(self):
        """Function to create a IP accessgroup on IOS XE"""
        # url = self._execute_call('Cisco-IOS-XE-native:native').patch('Cisco-IOS-XE-native:native/interface/GigabitEthernet=3')
        url = 'https://{0}:{1}/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=3'.format(self.host, self.port)
        headers = {
        'Accept': 'application/yang-data+json',
        'content-type': 'application/yang-data+json'
        }

        data = {
        "Cisco-IOS-XE-native:GigabitEthernet":[
              {
                 "name":"3",
                 "ip":{
                    "access-group":{
                       "in":{
                          "acl":{
                             "acl-name":"DROP",
                             "in":[None]
                          }
                       }
                    }
                 }
              }
           ]
        }
        response = self._execute_call('Cisco-IOS-XE-native:native/interface/GigabitEthernet=3', method='patch', data=json.dumps(data))
        return response

    def delete_access_group(self):
        """Function to delete a IP accessgroup on IOS XE"""
        url = 'https://{0}:{1}/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=3/ip/access-group/in/acl'.format(self.host, self.port)
        headers = {
        'Accept': 'application/yang-data+json',
        'content-type': 'application/yang-data+json'
        }

        data = {}
        response = self._execute_call('Cisco-IOS-XE-native:native/interface/GigabitEthernet=3/ip/access-group/in/acl', method='delete', data=json.dumps(data))
        return response
