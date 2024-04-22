## Python dependencies
`python3 -m venv venv`
`. ./venv/bin/activate`

`pip install kubernetes`
`pip freeze > requirements.txt`


## Custom resource
`kubectl apply -f crd.yaml`

## Custom resource watcher
`python main.py`
`kubectl apply -f evc.yaml`
`kubectl get evc` - get custom resources
`kubectl get pvc` - get child resources


## Cleanup
`kubectl delete evc --all`
`kubectl delete pvc --all`
`kubectl delete crd ephemeralvolumeclaims.crd.dev`
`kubectl delete -f crd.yaml`

`kubectl delete -f evc.yaml`

## Links
- https://flugel-it.medium.com/building-custom-kubernetes-operators-part-5-building-operators-in-python-141929c3d0db
- https://github.com/flugel-it/k8s-python-operator
