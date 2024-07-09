# Kubernetes Extensions
## ApiService

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

Deactivate you Python virtual env when done:
```commandline
deactivate
```

#### Remove the APIService
```commandline
kubectl delete -f deployment.yaml -f service.yaml -f api-service.yaml
```
