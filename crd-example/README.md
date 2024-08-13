# Extending Kubernetes API Part 2: CRD
## Custom Resource Definitions
Custom Resource Definitions (or CRD) is a way to make the kube-apiserver recognize new kinds of object.
E.g. I can query pods like this
```commandline
kubectl get pods
```
I can register a custom resource via a CRD with names `myresource`, `myresources` and then it will be available in a similar way:
```commandline
kubectl get myresources
kubectl get myresource <name>
```
Typically, a CRD manifest is accompanied by a controller. Together this setup forms an operator.

### CRD vs APIService
In contrast with APIService, when you create a new custom resource definition (CRD), the Kubernetes API Server reacts by creating a new RESTful resource path, 
that can be accessed by an entire cluster or a single project (namespace).

Like APIService, CRD controller requires a deployment, but you focus on developer event handlers.
A particular URL that is available for a CRD is of no importance.

### CRD use cases
Use CRD when you need to extend or encapsulate some behavior to manage object in Kubernetes 
or create a custom workflow based on resource operations (creation, update, deletion).

An example of such a usage is integrating Prometheus server into Kubernetes. 
It is designed for collecting and storing metrics in a time-series db. In Kubernetes a popular solution
to install this monitoring tool is the Prometheus Operator. 
Prometheus uses a big config file that includes all scrape job configurations. Maintaining this configuration may become difficult.
Prometheus Operator adds ServiceMonitor CRD which allows to define individual scrape configs which are collected automatically
and added to the main config triggering a reload.

View all Resources:
```commandline
kubectl api-resources
```

View CRDs
```commandline
kubectl get crd
```

Let's start with simple examples written from scratch.
```commandline
cd crd-python-simple
```

## Basic single threaded watcher
### CRD
Verify that custom resource is not available yet
```commandline
kubectl get evc
```

```commandline
kubectl apply -f manifests/crd.yaml
```

Verify that custom resource is known to Kubernetes and the corresponding API is 
```commandline
kubectl get evc -v 6
```

Deploy a custom resource instance:
```commandline
kubectl apply -f manifests/evc.yaml
```

```commandline
kubectl get evc
```

### Install Python dependencies
```commandline
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

### Basic CRD controller
Run the main.py script to watch custom resource events in the main thread (custom resource must be registered)
```commandline
python basic-watcher/main.py
```

```commandline
kubectl apply -f manifests/evc.yaml
```

List custom resources
```commandline
kubectl get evc -v 6
```

The simple version of a controller does not do much. Let's see a more elaborate option that runs a watch stream in a separate thread.
## Threaded watcher with some logic
If you deleted the CRD on the previous step 
```commandline
kubectl apply -f manifests/crd.yaml
```

Make sure you don't have a persistent volume claim instance:
```commandline
kubectl get pvc
```

### Custom resource controller with a new thread
Run the main.py script to watch and handle custom resource events in a separate thread
```commandline
python threaded-watcher/main.py
```

If you did not delete an instance of a custom resource from the previous step, 
you will observe that there is an ADDED event issued right away. 

This is because the kubernetes client library has a replay capability. 
On script start it will issue an ADDED event for each existing watched resource

If you deleted the resource, recreate it again
Create a custom resource
```commandline
kubectl apply -f manifests/evc.yaml
```

List custom resources
```commandline
kubectl get evc -v 6
```
List child resources
```commandline
kubectl get pvc
```

Make a change in manifests/evc.yaml, apply them
```commandline
kubectl apply -f manifests/evc.yaml
```
and observe a new MODIFIED event

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

## Deactivate the venv
```commandline
deactivate
```

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
kopf run main.py --verbose
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

Delete the parent resource and check that PVC is deleted automatically.
```commandline
kubectl delete -f evc.yaml
kubectl get pvc
```

## Kopf adopt
When you use kopf.adopt to create a child resource, 
it modifies the metadata of the child resource to include an `ownerReferences` field. 
This field contains information about the parent resource, such as its name, UID, kind, and API version.
Kubernetes has a built-in garbage collector that uses the `ownerReferences` field to determine which resources should be deleted when their owner is deleted. 
When the parent resource is deleted, the garbage collector automatically deletes all child resources that have the parent listed in their ownerReferences field.

```commandline
kubectl apply -f evc.yaml
kubectl get pvc kopf-claim -o yaml
```

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

## TODO when to use CRD vs APIService
Use CRDs when you want to define and manage custom resources that can be managed natively by the Kubernetes API. 
It is suitable for simpler use cases where the custom resource can be fully managed within the Kubernetes control plane.
Simpler to use.

Use APIService when you need to implement complex logic, interact with external systems, 
or require custom API endpoints that go beyond the capabilities of CRDs.
APIService is considered more performant when working with ETCD.

## Other
APIService and CRD are the two ways to extend Kubernetes API. However, there are articles that consider other items as Kubernetes extensions.
### Webhooks
Admission Webhooks allow you to intercept and modify requests to the Kubernetes API server before they are processed. 
There are two types of admission webhooks: mutating (which can modify objects) and validating (which can validate objects).
Conversion Webhooks are used with CRDs to handle multiple versions of a resource and convert between them.

### Open Service Broker API (former Service Catalog)
The Open Service Broker API is a standard way for SaaS platforms to provide services to applications running on cloud native platforms such as Kubernetes.
They do not necessarily extend the Kubernetes API, but they are a way to provide services to applications running on Kubernetes.
See [link](https://www.openservicebrokerapi.org/)

### References
- https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
- https://flugel-it.medium.com/building-custom-kubernetes-operators-part-5-building-operators-in-python-141929c3d0db
- https://github.com/flugel-it/k8s-python-operator
- https://kopf.readthedocs.io/en/latest/
