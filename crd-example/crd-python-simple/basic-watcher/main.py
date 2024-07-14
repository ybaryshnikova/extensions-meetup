from kubernetes import client, config, watch
import signal
import sys

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
# Use in-cluster config instead of kube_config
# config.load_incluster_config()

# Define the custom resource details
group = 'crd.dev'
version = 'v1'                             # CRD's spec.group
kind = 'EphemeralVolumeClaim'              # CRD's kind
namespace = 'default'                      # Namespace where your CRD instances are deployed
resource_plural = 'ephemeralvolumeclaims'  # CRD spec.names.plural

# Create a custom API client
api = client.CustomObjectsApi()


# Note: when restarted, the script will replay all events from the beginning.
# To avoid this, manual state management is required.
def watch_custom_resource_events():
    w = watch.Watch()
    try:
        # Setup a signal handler to stop watching when receiving SIGINT or SIGTERM
        def stop_watch(signum, frame):
            print("Exiting gracefully...")
            sys.exit(0)  # Exit using sys.exit to allow cleanup

        signal.signal(signal.SIGINT, stop_watch)
        signal.signal(signal.SIGTERM, stop_watch)

        for event in w.stream(api.list_namespaced_custom_object, group, version, namespace, resource_plural, pretty='true'):
            # Print the event type and the name of the custom resource
            event_type = event['type']  # ADDED, MODIFIED, DELETED
            resource_name = event['object']['metadata']['name']
            print(f"Event: {event_type}, Name: {resource_name}")
            print(f"Event: {event}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        w.stop()
        print("Watch has been stopped.")


if __name__ == '__main__':
    watch_custom_resource_events()
