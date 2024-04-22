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
`kubectl apply -f crd.yaml`

### CRD watcher
`python watch_custom_resource_events.py`
`kubectl apply -f evc.yaml`
`kubectl get evc` - get custom resources
`kubectl get pvc` - get child resources

### Cleanup
Remove the CRD and the custom resources
```commandline
kubectl delete -f evc.yaml
kubectl delete -f crd.yaml
```


## Threaded watcher with some logic
TODO: add description




## Deactivate the venv
```commandline
deactivate
```



