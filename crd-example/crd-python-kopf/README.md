# CRD Python example using KOPF library
## Install Python dependencies

Go to `controller` directory.

`python -m venv venv`
`. ./venv/bin/activate`

Installing deps from requirements.txt:
```commandline
pip install -r requirements.txt
```

Installing deps from scratch:
`pip install kubernetes`
`pip install kopf`
`pip freeze > requirements.txt`

## CRD
Go to `manifests` directory

```commandline
kubectl apply -f crd.yaml
```

## CRD watcher

Run the Kopf based watcher in `controller` directory:
```commandline
kopf run ephemeral.py --verbose
```

Use `manifests` directory. Create the custom resource instance
```commandline
kubectl apply -f evc.yaml
```

List custom resources
```commandline
kubectl get evc -v 6
```
List child resources
```commandline
kubectl get pvc
```

## Kopf adopt
When you use kopf.adopt to create a child resource, 
it modifies the metadata of the child resource to include an `ownerReferences` field. 
This field contains information about the parent resource, such as its name, UID, kind, and API version.
Kubernetes has a built-in garbage collector that uses the `ownerReferences` field to determine which resources should be deleted when their owner is deleted. 
When the parent resource is deleted, the garbage collector automatically deletes all child resources that have the parent listed in their ownerReferences field.

```yaml
ownerReferences:
    - apiVersion: kopf.dev/v1
      blockOwnerDeletion: true
      controller: true
      kind: EphemeralVolumeClaim
      name: kopf-claim
      uid: 3e089bfd-fa7e-4d4c-bb5c-95326cc786a2
```

## Advantages compared to no-library implementation
- Abstracts away boilerplate (event types, check if object exists on reload, run in a thread)
- Automatic Retry on error
- Status object
- connect the crd resource to a child resource with one line
- built-in ability to filter on fields, annotations

## Cleanup
```commandline
kubectl delete evc --all
kubectl delete pvc --all
```

Remove CRD
```commandline
kubectl delete -f crd.yaml
```
or
```commandline
kubectl delete crd ephemeralvolumeclaims.kopf.dev
```
