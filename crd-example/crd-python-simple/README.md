# CRD basic Python example (withou Kopf or a similar library)

## Install Python dependencies
```commandline
cd crd-python-simple
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Basic single threaded watcher
### CRD
```commandline
kubectl apply -f crd.yaml
```

### CRD watcher
Run the watch_custom_resource_events.py script to watch custom resource events in the main thread
```commandline
python watch_custom_resource_events.py
```

Create the custom resource instance
```commandline
kubectl apply -f evc.yaml
```
Note: controller (+ crd) = Kubernetes operator

List custom resources
```commandline
kubectl get evc -v 6
```
List child resources
```commandline
kubectl get pvc
```

### Cleanup
Remove custom resource instances
```commandline
kubectl delete -f evc.yaml
```
Remove CRD
```commandline
kubectl delete -f crd.yaml
```
or
```commandline
kubectl delete crd ephemeralvolumeclaims.crd.dev
```


## Threaded watcher with some logic
### Register custom resource definition
```commandline
kubectl apply -f crd.yaml
```

### Custom resource watcher
Run the main.py script to watch and handle custom resource events in a separate thread
```commandline
python main.py
```
Create a custom resource
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

### Cleanup
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
kubectl delete crd ephemeralvolumeclaims.crd.dev
```

### Links
- https://flugel-it.medium.com/building-custom-kubernetes-operators-part-5-building-operators-in-python-141929c3d0db
- https://github.com/flugel-it/k8s-python-operator

## Deactivate the venv
```commandline
deactivate
```



