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

#### Docker
```commandline
docker build -t apiservice-example .
docker run -p 443:443 apiservice-example
```

```commandline
docker run -p 443:443 apiservice-example
```

Push to DockerHub
```commandline
docker build -t <dockerhub_account>/apiservice-example:latest .         
docker push <dockerhub_account>/apiservice-example:latest
```

### Deactivate the venv
```commandline
deactivate
```

### Calling ApiService
#### Libraries
Go: The official Kubernetes Go client library, client-go, is the most widely used. It offers comprehensive features for interacting with Kubernetes API, including the Extension API servers.

Python: For Python, the official Kubernetes client, kubernetes-py, is commonly used. It provides a Pythonic way to work with Kubernetes APIs, including custom extension APIs.

Java: The official Kubernetes Java client library, kubernetes-client/java, is suitable for Java applications. It allows you to interact with Kubernetes API servers, including custom APIs, in a Java-friendly way.

JavaScript/Node.js: For applications written in JavaScript or Node.js, the kubernetes-client/javascript library is recommended. It provides JavaScript objects for interacting with the Kubernetes API, including extension APIs.

C#/.NET: If your application is built on the .NET platform, you can use the kubernetes-client/csharp library. It is the official .NET client for Kubernetes and supports accessing extension APIs.

Ruby: The kuby-core gem is an option for Ruby applications. It wraps around Kubernetes API, including extensions, and provides an easy-to-use interface for Ruby developers.

#### Code Example

```python
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def main():
    # Load kubeconfig
    config.load_kube_config()

    # Set up the dynamic client
    dyn_client = client.DynamicClient(client.ApiClient(configuration=config.load_kube_config()))

    # Define the group, version, and plural of your custom resource
    group = 'example.com'   # Your custom resource group
    version = 'v1'          # Your custom resource version
    plural = 'examples'     # Your custom resources plural

    try:
        # Fetching the custom resource definitions (CRDs)
        crd_api = dyn_client.resources.get(api_version=f"{group}/{version}", kind=plural)
        
        # Listing all instances of the custom resource
        cr_instances = crd_api.get()

        print("Listing all custom resource instances:")
        for cr in cr_instances.items:
            print(f"Name: {cr.metadata.name}")

    except ApiException as e:
        print("Exception encountered while calling Kubernetes API:", e)

if __name__ == '__main__':
    main()

```

```go
package main

import (
"context"
"fmt"
"path/filepath"

    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/clientcmd"
    // Assuming your custom resource is in a group called "example.com"
    examplev1 "your/custom/resource/package/example/v1" // Import your custom resource's versioned package
    "k8s.io/client-go/dynamic"
    "k8s.io/apimachinery/pkg/runtime/schema"
)

func main() {
// Load the kubeconfig file.
kubeconfigPath := filepath.Join(homeDir(), ".kube", "config")
config, err := clientcmd.BuildConfigFromFlags("", kubeconfigPath)
if err != nil {
panic(err.Error())
}

    // Create a dynamic client. We use dynamic client because extension APIs (CRDs) are not available in the typed client set.
    dynamicClient, err := dynamic.NewForConfig(config)
    if err != nil {
        panic(err.Error())
    }

    // Define the GVR (Group, Version, Resource) for your custom resource.
    crdGVR := schema.GroupVersionResource{
        Group:    "example.com", // Your custom resource's group
        Version:  "v1",          // Your custom resource's version
        Resource: "examples",    // Your custom resource's plural name
    }

    // Now, let's fetch a list of your custom resource instances
    crdList, err := dynamicClient.Resource(crdGVR).Namespace("").List(context.TODO(), metav1.ListOptions{})
    if err != nil {
        panic(err.Error())
    }

    // Iterate through all items in the custom resource list and print their names.
    fmt.Println("Listing all custom resources:")
    for _, crd := range crdList.Items {
        fmt.Printf("Name: %s\n", crd.GetName())
    }
}

// homeDir finds the home directory for the current user. This is used to locate the kubeconfig file.
func homeDir() string {
if h := os.Getenv("HOME"); h != "" {
return h
}
return os.Getenv("USERPROFILE") // windows
}

```
### Metrics server
Install with disabled certificate validation
```commandline
helm upgrade --install metrics-server metrics-server/metrics-server --set args="{--kubelet-insecure-tls}" -n kube-system
```
Follow the [tutorial](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)
