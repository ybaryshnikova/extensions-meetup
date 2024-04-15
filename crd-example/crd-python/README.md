# CRD Python example using KOPF library
## Install Python dependencies

`python3 -m venv venv`
`. ./venv/bin/activate`

`pip install kubernetes`
`pip install kopf`
`pip freeze > requirements.txt`

## CRD
`kubectl apply -f crd.yaml`

## CRD watcher
`kopf run ephemeral.py --verbose`
`kubectl apply -f evc.yaml`
`kubectl get evc` - get custom resources
`kubectl get pvc` - get child resources

## Advantages compared to no-library implementation
- Abstracts away boilerplate (event types, check if object exists on reload, run in a thread)
- Automatic Retry on error
- Status object
- connect the crd resource to a child resource with one line
- built-in ability to filter on fields, annotations

## Cleanup
`kubectl delete crd ephemeralvolumeclaims.kopf.dev`
`kubectl delete -f crd.yaml`
`kubectl delete pvc my-claim`
