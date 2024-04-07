# Kubernetes Extensions
## ApiService

### Virtual environment
```commandline
cd apiservice-example
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### Running the app
```commandline
pip install -r requirements.txt
gunicorn -c config.py -b 0.0.0.0:8000 server:application
```
**Note**: for the purpose of this demo requirements.txt contains the necessary packages for both the ApiService and for the consumer of the ApiService.

#### Docker
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

See an example of calling the custom API via the Kubernetes PY client library in `query-service.py`.

#### Remove the APIService
```commandline
kubectl delete -f deployment.yaml -f service.yaml -f api-service.yaml
```
