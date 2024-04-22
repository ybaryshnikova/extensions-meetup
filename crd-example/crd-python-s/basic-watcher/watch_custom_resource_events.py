from kubernetes import client, config, watch

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

# Define the custom resource details
group = 'crd.dev'
version = 'v1'                             # CRD's spec.group
kind = 'EphemeralVolumeClaim'              # CRD's kind
namespace = 'default'                      # Namespace where your CRD instances are deployed
resource_plural = 'ephemeralvolumeclaims'  # CRD spec.names.plural

# Create a custom API client
api = client.CustomObjectsApi()


def watch_custom_resource_events():

    # Watch the custom resource events
    w = watch.Watch()
    for event in w.stream(api.list_namespaced_custom_object, group, version, namespace, resource_plural, pretty='true'):
        # Print the event type and the name of the custom resource
        event_type = event['type']  # ADDED, MODIFIED, DELETED
        resource_name = event['object']['metadata']['name']
        print(f"Event: {event_type}, Name: {resource_name}")
        print(f"Event: {event}")


if __name__ == '__main__':
    watch_custom_resource_events()
