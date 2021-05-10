# Copyright 2020-2021 Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# (MIT License)

'''
Created on Nov 24, 2020

@author: jsl
'''

import logging
import sys
import base64
import time
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.rest import ApiException

from cfsssh.kubernetes import KubeToken
from cfsssh.vault import VaultClient, VaultSshKey
from cfsssh.setup.service.values import VAULT_CLIENT_ROLE

from csmsshkeys.values import CSM_PRIVATE_KEY, CSM_PUBLIC_KEY, K8S_NAMESPACE, CSM_VAULT_KEY_NAME

# Log setup
LOG_LEVEL = logging.DEBUG
lh = logging.StreamHandler(sys.stdout)
lh.setLevel(LOG_LEVEL)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(LOG_LEVEL)
LOGGER.addHandler(lh)

#Bootstrapping k8s client
try:
    config.load_incluster_config()
except ConfigException:  # pragma: no cover
    config.load_kube_config()  # Development


def cor_secret(name, namespace, value, keyname='value', k8s_client=None):
    """
    Create Or Replace a secret within a namespace.
    """
    k8s_client = k8s_client or client.CoreV1Api()
    api_version = 'v1'
    metadata = {'name': name, 'namespace': namespace}
    data = {keyname: base64.b64encode(value.encode('utf-8')).decode('utf-8')}
    body = client.V1Secret(api_version=api_version, kind='Secret', type='Opaque',
                           metadata=metadata, data=data)
    try:
        k8s_client.create_namespaced_secret(K8S_NAMESPACE, body)
        LOGGER.info("Created new Secret %s.", name)
    except ApiException:
        LOGGER.info("Replacing existing secret '%s'...", name)
        k8s_client.replace_namespaced_secret(name=name, namespace=K8S_NAMESPACE, body=body)


def cor_configmap(name, namespace, value, keyname='value', k8s_client=None):
    """
    Create Or Replace a config_map within a namespace.
    """
    k8s_client = k8s_client or client.CoreV1Api()
    api_version = 'v1'
    metadata = {'name': name, 'namespace': namespace}
    data = {keyname: base64.b64encode(value.encode('utf-8')).decode('utf-8')}
    body = client.V1ConfigMap(api_version=api_version, kind='ConfigMap',
                           metadata=metadata, data=data)
    try:
        k8s_client.create_namespaced_config_map(K8S_NAMESPACE, body)
        LOGGER.info("Created new Secret %s.", name)
    except ApiException:
        LOGGER.info("Replacing expiring config_map '%s'...", name)
        k8s_client.replace_namespaced_config_map(name=name, namespace=K8S_NAMESPACE, body=body)


def setup():
    """
    Performs basic setup of ssh keys for use with Cray System Management.

    Note: If we have kubernetes secrets and config_maps already, we will not
    overwrite them. There is a very real chance that these artifacts were
    overwritten by the customer. We should not assume to replace them unconditionally.
    """
    LOGGER.info("Cray System Management SSH Keys setting up...")
    v1 = client.CoreV1Api()

    # Ascertain what configuration is set
    public_key_defined = False
    try:
        _ = v1.read_namespaced_config_map(CSM_PUBLIC_KEY, K8S_NAMESPACE)
        public_key_defined = True
    except ApiException:
        LOGGER.info("CSM Public key not available in config_map '%s' namespace '%s'.",
                    CSM_PUBLIC_KEY, K8S_NAMESPACE)
    private_key_defined = False
    try:
        _ = v1.read_namespaced_secret(CSM_PRIVATE_KEY, K8S_NAMESPACE)
        private_key_defined = True
    except ApiException:
        LOGGER.info("CSM Private key not available in secret '%s' namespace '%s'.",
                    CSM_PRIVATE_KEY, K8S_NAMESPACE)
    if all([public_key_defined, private_key_defined]):
        LOGGER.info("CSM Keypair components already published; skipping...")
        return
    else:
        LOGGER.info("Generating CSM public/private keypair with vault...")

    # Obtain credentialing information for vault
    kt = KubeToken.from_pod()
    vc = VaultClient(kt.value, VAULT_CLIENT_ROLE)
    vssh = VaultSshKey.CreateOrReference(CSM_VAULT_KEY_NAME, vc)

    # Publish keys within named config_maps and secrets
    k8s_client = client.CoreV1Api()
    cor_secret(CSM_PRIVATE_KEY, K8S_NAMESPACE, vssh.private_key, k8s_client=k8s_client)
    cor_configmap(CSM_PUBLIC_KEY, K8S_NAMESPACE, vssh.public_key, k8s_client=k8s_client)
    LOGGER.info("Done publishing public/private key pair; they can now be consumed \
and applied to running systems.")

def periodically_setup():
    """
    Bad Stuff Happens (tm); and we should only have to set up
    keys once, however if our key information goes missing due
    to partial-re-install, database corruption, or administrator
    user error, we want to obtain and republish the information
    when possible. As a result, there is a strong desire to
    heal the configuration as best we can, so we will periodically
    call our setup routine to ensure that there are a public/private
    keypair that can be consumed. These routines should be re-entrant safe,
    and will only create new vault keys and associated published artifacts
    should they go missing. If they are not missing, setup does not
    touch them.
    """
    while True:
        setup()
        time.sleep(60*60) # Every hour, check and ensure we have keys

if __name__ == '__main__':
    periodically_setup()
