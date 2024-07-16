import os
import yaml
from kubernetes import config, client
import time


def _build_claim_data(name, size):
    path = os.path.join(os.path.dirname(__file__), 'pvc.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=name, size=size)
    return yaml.safe_load(text)


def _build_claim(name, spec, namespace):
    size = spec.get('size')
    if not size:
        raise Exception(f"Size must be set. Got {size!r}.")

    data = _build_claim_data(name, size)
    api = client.CoreV1Api()
    obj = api.create_namespaced_persistent_volume_claim(namespace=namespace, body=data)

    print(f"new PVC child is created: {name}")
    return obj


def create_fn(spec, name, namespace):
    size = spec.get('size')
    if not size:
        raise Exception(f"Size must be set. Got {size!r}.")

    obj = _build_claim(name, spec, namespace)
    return {'pvc-name': obj.metadata.name}  # is not used out of the box


def update_fn(spec, name, namespace):
    size = spec.get('size')
    if not size:
        raise Exception(f"Size must be set. Got {size!r}.")

    # !!!To use patch, storage class should support resize
    # pvc_patch = {'spec': {'resources': {'requests': {'storage': size}}}}
    # api = kubernetes.client.CoreV1Api()
    # obj = api.patch_namespaced_persistent_volume_claim(
    #     namespace=namespace,
    #     name=pvc_name,
    #     body=pvc_patch,
    # )

    api = client.CoreV1Api()
    api.delete_namespaced_persistent_volume_claim(name=name, namespace=namespace)
    print(f"old PVC child is deleted: {name}")
    time.sleep(0.05) # a simple workaround for deletion delay, only for demo

    _build_claim(name, spec, namespace)
    print(f"PVC child is replaced: {name}")
