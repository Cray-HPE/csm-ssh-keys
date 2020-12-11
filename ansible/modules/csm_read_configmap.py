"""
The purpose of this ansible module is to assist with the interaction
of the kubernetes binaries using the python kubernetes library from within the cluster.
This is a thin wrapper to the python-kubernetes client, designed exclusively to read
values from an already stored config_map.

Copyright 2020 Hewlett Packard Enterprise Development LP
"""

import base64
import logging
import os
from json import loads

from ansible.module_utils.basic import AnsibleModule
from kubernetes import client, config
from kubernetes.client.rest import ApiException


config.load_incluster_config()
LOGGER = logging.getLogger()
ORGANIZATION = 'hpe'
LOG_DIR = '/var/log/%s' % ( ORGANIZATION )
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview', 'stableinterface'],
    'supported_by': ORGANIZATION
}
DOCUMENTATION = '''
---
module: csm_read_configmap

short_description: This module provides ansible bindings for the python k8s client
library used to read configmaps.

description:
    - Performs the requested operation against the running k8s API from within the
    cluster.

options:
    name:
        required: True
        type: String
        description: The name of the kubernetes config_map to read
    namespace:
        required: True
        type: String
        description: The namespace that contains the config_map in question
    key:
        required: True
        type: String
        description: The key that contains the information requested
    decrypt:
        type: Boolean
        default: True
        description: Perform base64 decrypt on the value returned from the response.
'''

EXAMPLES = '''
- name: Read a configmap from the cluster
  csm_read_configmap:
    name: foo
    namespace: services
    key: bar
    decrypt: True
  register: foo_bar_value
'''
RETURN = '''
response:
    description: The value (encrypted or decrypted) of the config_map queried
    type: String
    returned: always
changed:
    description: Always False; read operations never change the structure of a config_map
    type: boolean
'''


class ReadConfigMapModule(AnsibleModule):
    """
    An Ansible module that reads config_maps from the incluster k8s API.
    """
    def __init__(self, *args, **kwargs):
        super(ReadConfigMapModule, self).__init__(*args, **kwargs)
        # Expose certain parameters as public attributes
        for keyword in ('name', 'namespace', 'decrypt','key'):
            if keyword in self.params:
                setattr(self, keyword.replace('-', '_'), self.params[keyword])
        self.client = client.CoreV1Api()

    @staticmethod
    def log_request(resp, *args, **kwargs):
        """
        This function logs the request.
    
        Args:
            resp : The response
        """
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug('\n%s\n%s\n%s\n\n%s',
                                       '-----------START REQUEST-----------',
                                       resp.request.method + ' ' + resp.request.url,
                                       '\n'.join('{}: {}'.format(k, v) for k, v in resp.request.headers.items()),
                                       resp.request.body)

    @staticmethod
    def log_response(resp, *args, **kwargs):
        """
        This function logs the response.
    
        Args:
            resp : The response
        """
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug('\n%s\n%s\n%s\n\n%s',
                         '-----------START RESPONSE----------',
                         resp.status_code,
                         '\n'.join('{}: {}'.format(k, v) for k, v in resp.headers.items()),
                         resp.content)

    def __call__(self):
        result = {}
        result['changed'] = False
        response = None
        try:
            response = self.client.read_namespaced_config_map(name=self.name, 
                                                              namespace=self.namespace)
            return_value = response.data['value']
            if self.key:
                return_value = return_value[self.key]
            if self.decrypt:
                return_value = base64.b64decode(return_value).decode('utf-8')
            result['response'] = return_value
        except ApiException as ae:
            self.fail_json(msg=str(ae))
        self.exit_json(**result)


def main():
    fields = {# Authentication Information
              'name': {'required': True, "type": 'str'},
              'namespace': {'required': False, "type": "str", 'default': 'services'},
              'key': {'required': False, "type": 'str', 'default': ''},
              'decrypt': {'required': False, "type": "bool", "default": True}}
    module = ReadConfigMapModule(argument_spec=fields)
    module()


if __name__ == '__main__':
    try:
        os.makedirs(LOG_DIR)
    except OSError:
        pass
    level = logging.DEBUG
    _disk_output_handler = logging.FileHandler(os.path.join(LOG_DIR, 'kubernetes_configmaps.log'))
    _disk_output_handler.setLevel(level)
    LOGGER.addHandler(_disk_output_handler)
    LOGGER.setLevel(level)
    main()
