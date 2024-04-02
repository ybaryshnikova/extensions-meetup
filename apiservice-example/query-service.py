from kubernetes import client, config

# Load the kubeconfig file
config.load_kube_config()

discovery_v1_api = client.DiscoveryV1Api()
api_resources = discovery_v1_api.get_api_resources()
print(api_resources)
