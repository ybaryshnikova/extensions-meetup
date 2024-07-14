# Extending Kubernetes API Part 1: API Server, APIService
## Overview
Part 1:
- Intro into API Server, the core API, the API structure, Discovery API
- A simple example of extending the API Server with a custom API
- Accessing the API Server via client libraries
- Metrics server example

Part 2:
- Custom Resource Definitions (CRDs)
- Using Helm

## Introduction
First it is important to look into the Kubernetes API Server and its API structure.
The design of the API Server establishes the basis that needs to be implemented.

The API server is an integral part of Kubernetes. It provides mostly REST API (there is also API that does not follow REST conventions, like health checks. This API is used for internal purposes and does not manage resources.).
See API conventions [here](https://github.com/kubernetes/community/blob/7f3f3205448a8acfdff4f1ddad81364709ae9b71/contributors/devel/sig-architecture/api-conventions.md#verbs-on-resources).
The REST API handles all of the communication between components and external users, 
that is all interaction in a Kubernetes cluster is a REST call behind the scenes.

API Server is the only component that communicates with the etcd database.
It is deployed on nodes that are configured as control plane nodes and is horizontally scalable.
All critical components of the cluster are located on these nodes.

In other words, the API server gives access to the Kubernetes resources and non-resource objects.

By resources we usually mean objects managed by Kubernetes: pods, services, deployments, etc.

Non-resource objects are metrics, logs, etc.

Strictly speaking, according to the docs,
"A resource is an endpoint in the Kubernetes API that stores a collection of API objects of a certain kind; 
for example, the built-in pods resource contains a collection of Pod objects".

## API Server API paths
Find API Server host and port:
```commandline
kubectl cluster-info
```

## Requests to the API Server

As mentioned above all the requests to the cluster are REST API calls.
For example, I want to view all pods in the default namespace:
```commandline
kubectl get pods
```
This command is translated into a REST API call to the API:
```text
GET /api/v1/namespaces/default/pods
```
To show what endpoint is called, you can use the `-v 6` flag:
```commandline
kubectl get pods -v 6
```
The result will be similar to this:
```commandline
I0405 17:12:02.757038   98373 loader.go:395] Config loaded from file:  /Users/yulya/.kube/config
I0405 17:12:02.762524   98373 cert_rotation.go:137] Starting client certificate rotation controller
I0405 17:12:02.780999   98373 round_trippers.go:553] GET https://127.0.0.1:62152/api/v1/namespaces/default/pods?limit=500 200 OK in 11 milliseconds
NAME                                   READY   STATUS    RESTARTS       AGE
api-extension-server-d498d9b74-pdwrf   1/1     Running   1 (2d3h ago)   3d1h
```
As shown above, `api/v1` API was called.

The same call to pods list can be made directly to the API Server (with kube-proxy):
```commandline
kubectl proxy
curl localhost:8001/api/v1/namespaces/default/pods
```

Or sending the raw request:
```commandline
kubectl get --raw /api/v1/namespaces/default/pods |  jq '.'
```

Normally the direct calls to the API Server are not used. 
Instead, a typical approach is to use a client library which we'll see later.

View raw API paths:
```commandline
kubectl proxy
curl http://localhost:8001/
```

## Kubernetes API structure
![Kubernetes API Structure](kube-api-structure2.avif)

Most API follows the REST architectural style.
The API are organized in groups.

API starting with `/api` is the core API group that gives access to standard Kubernetes resources (pods, services, etc).

API starting with `/apis` is a named group of API. It also includes some core API but is usually the extension API that gives access to custom resources.

API starting with `/healthz` is the health check API. The healthz endpoint is deprecated (since Kubernetes v1.16).

API starting with `/livez` is the liveness check API.

API starting with `/readyz` is the readiness check API.

API starting with `/metrics` is the metrics API.

API like `healthz` and `readyz` do not follow the REST convention.
Liveness Probes: Continuous checks throughout the lifecycle of the container to ensure it remains operational. If a liveness probe fails at any point, it indicates a severe problem that requires restarting the container.
Readiness Probes: Often used at the initial startup and during the lifetime of the container to ensure it is ready to handle requests. These probes can fail temporarily without requiring a restart, simply stopping traffic to the container until it is ready again.

An API group is followed by the version of the API. 
When creating a resource, the API group and version is specified in the `apiVersion` field.

### Discovery API
The Discovery API is a special API that gives information about the API groups and versions available in the cluster.
It comprises several Kubernetes API endpoints under /api and /apis paths:

`/api`: Lists the versions of the core API group.

`/apis`: Lists the available API groups and their versions.

`/api/<version>`: Provides information about the resources in the core group for a specific version.

`/apis/<group>/<version>`: Provides information about the resources in a specific group and version.

#### How It Works
Clients can query these endpoints to retrieve a list of API resources and operations supported by the Kubernetes API server. This information is returned in a structured format, allowing clients to dynamically discover resources and construct requests based on the capabilities of the API server they are communicating with.

#### Use Cases
The Discovery API is particularly useful for:

- Dynamic Clients: Clients that need to work with multiple versions of Kubernetes or with custom resources can use the Discovery API to adapt their behavior based on the available API resources.
- Tooling and Integration: Tools like Kubernetes CLI (kubectl), dashboard UIs, and IDE plugins can use the Discovery API to provide dynamic resource exploration and management capabilities.
- Custom Controllers and Operators: Developers building custom controllers or operators that manage custom resources can leverage the Discovery API to ensure compatibility with different Kubernetes clusters and versions.

### Get API Versions:
```commandline
kubectl api-versions
```
When adding a resource manifest we add an apiVersion that contains a group name and a version
```yaml
apiVersion: apps/v1
kind: Deployment
...
```

## Extending API server: Aggregation Layer
The API server supports API aggregation, allowing third-party API extensions to be registered and managed alongside built-in Kubernetes APIs. 
This extensibility enables the integration of additional features and custom resources.

## Extending API Server: APIService
`APIService` is a resource that allows you to expose a new API group to the Kubernetes API Server.
This resource is available in the `/apis/apiregistration.k8s.io/v1` API group.
`APIService` requires adding what is called an API extension server. You must add an APIService manifest and an appropriate service+deployment.

Get registered APIService
```commandline
kubectl get apiservice
```
The caveat: core api is shown as APIService too.
E.g. `v1` is a core API group, but it is also shown as an APIService.
`kubectl get apiservice v1. -o yaml` will show the details of the core API group but it is not a custom API.

## Custom API example

### Virtual environment
```commandline
cd apiservice-example/extension-server
python -m venv venv
. ./venv/bin/activate
```

### Running the app
```commandline
pip install -r requirements.txt
python server.py
```
Note: Python apps usually use gunicorn so the launch command could look something like this
`gunicorn -c config.py -b 0.0.0.0:8000 server:application`

#### Docker
In the directory containing the Dockerfile run:
```commandline
docker build -t apiservice-example .
docker run -p 443:443 apiservice-example
```

```commandline
docker run -p 443:443 apiservice-example
```

#### Deactivate the venv
```commandline
deactivate
```

### Install the custom APIService
Go to the `api-example` folder
```commandline
cd apiservice-example
```
Build the apiservice-example image and push to DockerHub:
```commandline
docker build -t <dockerhub_account>/apiservice-example:latest .         
docker push <dockerhub_account>/apiservice-example:latest
```
Modify the image in `deployment.yaml` to point to your image. Apply the manifests:
```commandline
kubectl apply -f deployment.yaml -f service.yaml -f api-service.yaml
```
Check the ApiService is registered:
```commandline
kubectl get apiservice | grep example
kubectl describe apiservice v1alpha1.example.com
```

#### Calling ApiService

A simple example of calling the custom API:
```commandline
kubectl get --raw /apis/example.com/v1alpha1
```

Resources defined in the REST endpoints do not translate into Kubernetes resources. To achieve that use CRD.

##### Kubernetes Python client
See an example of calling the custom API via the Kubernetes PY client library in `query-api/query-service.py`.
Go to `query-api` folder

```commandline
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python query-service.py
```
Explore the docs [Kubernetes Python client custom API](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CustomObjectsApi.md).

See also:

[Python client example](https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/#python-client)

[Access custom API](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CustomObjectsApi.md)
The docs also specify HTTP requests for each API operation.

[Kubernetes Go Client library](https://github.com/kubernetes/client-go)


##### Cleanup
Deactivate you Python virtual env when done:
```commandline
deactivate
```
Remove the APIService:
```commandline
kubectl delete -f deployment.yaml -f service.yaml -f api-service.yaml
```

## Metrics server API
Now let's look at the metrics-server - one of the most popular addons for Kubernetes
which extends API Server with the metrics API.
It provides metrics for pods and nodes.
It also uses the aggregation layer.
Check metrics API before installation:
```commandline
kubectl api-versions | grep metrics
curl http://localhost:8001 | grep metrics
```

Install the metrics server with disabled certificate validation:
```commandline
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/  
kubectl create namespace metrics-server
```
```commandline
helm install metrics-server metrics-server/metrics-server --set args="{--kubelet-insecure-tls}" -n metrics-server
```

Check metrics API after installation:
```commandline
curl http://localhost:8001 | grep metrics
```
or
```commandline
kubectl api-versions | grep metrics
```
New metrics API should be available:
```text
"/apis/metrics.k8s.io",
"/apis/metrics.k8s.io/v1beta1",
```

Describe the metrics API:
```commandline
kubectl describe apiservice v1beta1.metrics.k8s.io
```

#### metrics-server registration
See metrics-server components in `apiservice-example/metrics-server-example/metrics-server.yaml`

#### metrics-server REST API implementation
See `pkg/api/pod.go` in metrics-server source code

#### Autoscaling with metrics-server
Follow the [tutorial](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)

#### metrics-server cleanup
```
helm uninstall metrics-server -n kube-system
```

## References
[Kubernetes API guide](https://blog.kubesimplify.com/practical-guide-to-kubernetes-api)

[Kubernetes Python client custom API](https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CustomObjectsApi.md)

[Working with Kubernetes API Series](https://iximiuz.com/en/series/working-with-kubernetes-api/)

[Metrics server tutorial](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)
