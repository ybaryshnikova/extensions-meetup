from kubernetes import client, config

# Load the kubeconfig file
config.load_kube_config()

# see https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CustomObjectsApi.md
custom_objects_api = client.CustomObjectsApi()
api_resources = custom_objects_api.get_api_resources(group='example.com', version='v1alpha1')
print(api_resources)
