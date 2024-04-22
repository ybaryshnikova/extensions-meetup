from threadedwatch import ThreadedWatcher
from kubernetes import config, client
import pprint
import handlers

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

# Define the custom resource details
group = 'crd.dev'
version = 'v1'                             # CRD's spec.group
kind = 'EphemeralVolumeClaim'              # CRD's kind
namespace = 'default'                      # Namespace where your CRD instances are deployed
resource_plural = 'ephemeralvolumeclaims'  # CRD spec.names.plural

# Create a custom API client
custom_api = client.CustomObjectsApi()
ADDED = 'ADDED'
MODIFIED = 'MODIFIED'


def handle_custom_resource_added_event(spec, name):
    print(f"handle resource {name} ({kind}) ADDED event")
    try:
        handlers.create_fn(spec, name, namespace)
    except client.exceptions.ApiException as e:
        if e.status == 409:
            pass
        else:
            raise


def handle_custom_resource_updated_event(spec, name):
    print(f"handle resource {name} ({kind}) MODIFIED event")
    handlers.update_fn(spec, name, namespace)


def on_event(event):
    type = event['type']
    manifest = event['object']
    spec = manifest['spec']
    name = manifest['metadata']['name']
    if not name:
        raise Exception(f"Name must be set. Got {name!r}.")

    print(f"{type} event occurred on resource {name} ({kind})")
    pprint.pprint(spec)

    if type == ADDED:
        handle_custom_resource_added_event(spec, name)
    elif type == MODIFIED:
        handle_custom_resource_updated_event(spec, name)
    else:
        raise Exception(f"{type} handling is not yet implemented")


# v1 = client.CoreV1Api()
# watcher = ThreadedWatcher(v1.list_pod_for_all_namespaces)
watcher = ThreadedWatcher(custom_api.list_namespaced_custom_object, group, version, namespace, resource_plural, pretty='true')
watcher.add_handler(on_event)
watcher.start()
watcher.join()
