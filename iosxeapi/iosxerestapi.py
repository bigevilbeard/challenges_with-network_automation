import requests
import urllib3
import logging.config
import json
import re

HTTP_SUCCESS_CODES = {
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'Accepted but with no JSON body',
}

HTTP_ERROR_CODES = {
    400: 'Bad Request',
    401: 'Unauthorized',
    404: 'Not Found',
    405: 'Method not Allowed',
}

HTTP_SERVER_ERRORS = {
    500: 'Internal Server Error',
    503: 'Service Unavailable',
}

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
            'level': 'ERROR',
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

class Result(object):
    def __init__(self,
                 ok=False, response=None, status_code=None,
                 error=None, message=None, json=None):
        self.ok = ok
        self.response = response
        self.status_code = status_code
        self.error = error
        self.message = message
        self.json = json

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
            elif method == 'patch':
                response = requests.patch(url_base+url, auth=(self.username, self.password), headers=headers, verify=False, data=json.dumps(data, ensure_ascii=False))
            elif method == 'delete':
                response = requests.delete(url_base+url, auth=(self.username, self.password), headers=headers, verify=False, data=json.dumps(data, ensure_ascii=False))

            result = Result(response=response)
            result.status_code = response.status_code

            if response.status_code in HTTP_ERROR_CODES:
                result.ok = False
                result.error = HTTP_ERROR_CODES[response.status_code]

            elif response.status_code in HTTP_SERVER_ERRORS:
                result.ok = False
                result.error = HTTP_SERVER_ERRORS[response.status_code]

            elif response.status_code in HTTP_SUCCESS_CODES:
                result.ok = True
                result.message = HTTP_SUCCESS_CODES[response.status_code]

            if not response.status_code == 204:
                result.json = response.json()

            return result

                #response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
        except Exception as e:
            self.logger.error(e)

    def get_bgp(self):
        """Function to get BGP information on IOS XE"""
        neighbors_list = dict()
        neighbors_list['Cisco-IOS-XE-bgp-oper:bgp-state-data'] = {'neighbors':[]}
        api_data = self._execute_call('Cisco-IOS-XE-bgp-oper:bgp-state-data')
        neighbors = DictQuery(api_data.json).get(
            'Cisco-IOS-XE-bgp-oper:bgp-state-data/neighbors/neighbor')

        for neighbor in neighbors:
            dict_temp = {}
            dict_temp['neighbor-id'] = neighbor.get('neighbor-id',None)
            dict_temp['link'] = neighbor.get('link',None)
            dict_temp['up-time'] = neighbor.get('up-time',None)
            dict_temp['state'] = DictQuery(neighbor.get('connection')).get('state')
            dict_temp['total-prefixes'] = DictQuery(neighbor.get('prefix-activity')).get('received/total-prefixes')
            neighbors_list['Cisco-IOS-XE-bgp-oper:bgp-state-data']['neighbors'].append(dict_temp)

        return json.dumps(neighbors_list, sort_keys=False, indent=4)

    def get_device(self):
        """Function to get Device information on IOS XE"""
        device_list = dict()
        # device_list['Cisco-IOS-XE-native:native'] = {'device':[]}
        api_data = self._execute_call('Cisco-IOS-XE-native:native')
        device = DictQuery(api_data.json).get(
            'Cisco-IOS-XE-native:native')

        # print(system)

        hostname = device.get('hostname')
        version = device.get('version')

        dict_temp = dict()
        dict_temp['hostname'] = hostname
        dict_temp['version'] = version
        device_list['Cisco-IOS-XE-native:native'] = dict()
        device_list['Cisco-IOS-XE-native:native']['device'] = dict_temp


        return json.dumps(device_list, sort_keys=False, indent=4)


    def get_interfaces_oper(self):
        """Function to get interface information on IOS XE"""
        # return self._execute_call('Cisco-IOS-XE-interfaces-oper:interfaces')
        interfaces_list = dict()
        interfaces_list['Cisco-IOS-XE-interfaces-oper:interfaces'] = {'interface':[]}
        api_data = self._execute_call('Cisco-IOS-XE-interfaces-oper:interfaces')
        interfaces = DictQuery(api_data.json).get('Cisco-IOS-XE-interfaces-oper:interfaces/interface')

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

    def get_interfaces_list(self):
        """Function to get interface information on IOS XE"""
        interfaces_list = str()
        api_data = self._execute_call('Cisco-IOS-XE-interfaces-oper:interfaces')
        interfaces = DictQuery(api_data.json).get('Cisco-IOS-XE-interfaces-oper:interfaces/interface')

        for interface in interfaces:
            interfaces_list = interfaces_list + interface.get('name') + '\n'

        return interfaces_list

    def add_access_group(self, interface):
        """Function to create a IP accessgroup on IOS XE"""
        parsed_interface =re.search(r"(?P<intrfname>[A-Za-z]+)(?P<intf_num>\d((/\d+)+(\.\d+)?)|\d)",interface).groupdict()
        interface_name = parsed_interface.get('intrfname')
        interface_number = parsed_interface.get('intf_num')
        api_interface = '{0}={1}'.format(interface_name, interface_number)
        url = 'https://{0}:{1}/data/Cisco-IOS-XE-native:native/interface/{2}'.format(self.host, self.port, api_interface)
        headers = {
        'Accept': 'application/yang-data+json',
        'content-type': 'application/yang-data+json'
        }

        data = {
        "Cisco-IOS-XE-native:GigabitEthernet":[
              {
                 "name":interface_number,
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

        response = self._execute_call('Cisco-IOS-XE-native:native/interface/{0}'.format(api_interface), method='patch', data=data)
        return response

    def delete_access_group(self, interface):
        """Function to delete a IP accessgroup on IOS XE"""
        parsed_interface =re.search(r"(?P<intrfname>[A-Za-z]+)(?P<intf_num>\d((/\d+)+(\.\d+)?)|\d)",interface).groupdict()
        interface_name = parsed_interface.get('intrfname')
        interface_number = parsed_interface.get('intf_num')
        api_interface = '{0}={1}'.format(interface_name, interface_number)
        url = 'https://{0}:{1}/data/Cisco-IOS-XE-native:native/interface/{2}/ip/access-group/in/acl'.format(self.host, self.port, api_interface)
        headers = {
        'Accept': 'application/yang-data+json',
        'content-type': 'application/yang-data+json'
        }

        data = {}
        response = self._execute_call('Cisco-IOS-XE-native:native/interface/{0}/ip/access-group/in/acl'.format(api_interface), method='delete', data=json.dumps(data))
        return response
