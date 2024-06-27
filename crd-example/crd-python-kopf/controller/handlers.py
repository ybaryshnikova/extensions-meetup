import os
import kopf
import kubernetes
import yaml
import pprint

def load_kubernetes_config():
    if os.getenv('KUBERNETES_SERVICE_HOST'):
        # Running inside a Kubernetes cluster
        kubernetes.config.load_incluster_config()
    else:
        # Running outside a Kubernetes cluster
        kubernetes.config.load_kube_config()

# Load Kubernetes configuration
load_kubernetes_config()

def _build_claim_data(name, size):
    path = os.path.join(os.path.dirname(__file__), 'pvc.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=name, size=size)
    return yaml.safe_load(text)


def _build_claim(name, spec, namespace, logger):
    size = spec.get('size')
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    data = _build_claim_data(name, size)
    kopf.adopt(data) # connect evc to pvc

    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )

    logger.info(f"new PVC child is created: {obj}")
    return obj


def create_fn(spec, name, namespace, logger):
    print(f"Handle ADDED event for resource {name}")
    size = spec.get('size')
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    obj = _build_claim(name, spec, namespace, logger)

    return {'pvc-name': obj.metadata.name}


def update_fn(spec, status, namespace, logger):
    logger.info("UPDATE FN")
    pprint.pprint(status)
    pvc_name = status['create_fn']['pvc-name']
    logger.info(f"Handle MODIFIED event for resource {pvc_name}")
    size = spec.get('size', None)
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    # pvc_patch = {'spec': {'resources': {'requests': {'storage': size}}}}
    # To use patch, storage class should support resize
    # api = kubernetes.client.CoreV1Api()
    # obj = api.patch_namespaced_persistent_volume_claim(
    #     namespace=namespace,
    #     name=pvc_name,
    #     body=pvc_patch,
    # )

    api = kubernetes.client.CoreV1Api()
    api.delete_namespaced_persistent_volume_claim(name=pvc_name, namespace=namespace)
    logger.info(f"old PVC child is deleted: {pvc_name}")

    _build_claim(pvc_name, spec, namespace, logger)
    logger.info(f"PVC child is replaced: {pvc_name}")

