# CRD Python example using KOPF library
## Install Python dependencies

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
```commandline
kubectl apply -f crd.yaml
```

## CRD watcher

Run the Kopf based watcher:
```commandline
kopf run ephemeral.py --verbose
```

Create the custom resource instance
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
