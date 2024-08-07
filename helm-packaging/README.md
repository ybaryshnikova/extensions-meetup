# Helm

## Intro
Usually there is a need to work with multiple manifests in Kubernetes. 
E.g. adding an ApiService requires a deployment, a service, and a ApiService manifest.
Then they may be installed in different environments with different parameters.
Helm is to help with that. Also, lots of api extensions are distributed as Helm charts.
Helm is a package manager for Kubernetes. It allows to package and deploy applications in Kubernetes.

## Helm chart structure overview
A Helm chart is a collection of files organized in a specific directory structure.
The configuration information related to a chart is managed in the configuration file `values.yaml`.

A running instance of a chart with a specific config is called a release.
Releases are stored as Secrets by default in the namespace of the release directly. Previously, in Helm 2, releases were stored in ConfigMaps.
Helm uses a templating system based on Go template to render Kubernetes manifests from charts.
A chart is a consistent structure separating templates and values.

## Helm versioning overview
Helm charts use versions to track changes in your manifests – thus you can install a specific chart version for specific infrastructure configurations.
Helm keeps a release history of all deployed charts in a dedicated workspace.
This makes easier application updates and rollbacks if something wrong happens.

## Helm chart sharing overview
Helm allows you to compress charts.
The result of that is an artifact comparable to a Docker image.
Then, you can send it to a distant repository for reusability and sharing.

## Chart dependencies overview
As a package, a chart can also manage dependencies with other charts.
For example, if your application needs a MySQL database to work you can include the chart as a dependency.
When Helm runs at the top level of the chart directory it installs whole dependencies.
You have just a single command to render and release your application to Kubernetes.

## Create a chart
```commandline
helm create chart-example
```

## Chart structure:
#### Templates
Stores parameterized Kubernetes manifest files. The templating language is Go's text/template.
NOTES.txt is a special template that is rendered when the chart is deployed.
_helpers.tpl is a special template that contains reusable templates and functions.
#### values.yaml
Default values for the chart. These values can be overridden by passing them in with the --set flag or -f flag.
#### Chart.yaml
Contains metadata about the chart, such as the type, version, description.
#### .helmignore
Contains files that should be ignored when packaging the chart.
#### charts/
Contains dependencies for the chart.

## Install a chart
```commandline
helm install release1 basic-apiservice-chart
helm get manifest release1
```

## View releases
```commandline
helm list
```

## Release history
```commandline
helm history release1
```

## Update a chart
```commandline
helm upgrade release1 basic-apiservice-chart
helm history release1
```

## Rollback a release
Rollback version 2 of a release
```commandline
helm rollback release1 2
```


## Uninstall a release
```commandline
helm uninstall release1
```

## Run with individual params
```commandline
helm install custom-release ./chart-example --dry-run --debug --set image.pullPolicy=IfNotPresent
```
The `--dry-run` flag of `helm install` and `helm upgrade` is not currently supported for CRDs.

## Debugging
```commandline
helm install --debug --dry-run test-run basic-apiservice-chart
```

## Wait for the deployment to be ready
#### Wait for Pods, Services, PVCs and Deployments to be ready:
```commandline
helm install release1 basic-apiservice-chart --wait
```
#### Wait for jobs:
```commandline
helm install release1 basic-apiservice-chart --wait-for-jobs
```
#### Post-install hook to wait for an APIService to be available
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: wait-for-apiservice
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "0"
    "helm.sh/hook-delete-policy": hook-succeeded,hook-failed
spec:
  template:
    spec:
      serviceAccountName: apiservice-waiter
      containers:
        - name: wait-for-apiservice
          image: bitnami/kubectl:1.21
          command:
            - /bin/sh
            - -c
            - |
              set -e
              echo "Waiting for ApiService to be available..."
              kubectl wait --for=condition=Available --timeout=120s apiservice v1alpha1.example.com
      restartPolicy: Never
  backoffLimit: 4
```
See [Chart hooks](https://helm.sh/docs/topics/charts_hooks/)

#### install CRD before other resources
For a CRD, the declaration must be registered before any resources of that CRDs kind(s) can be used. 
To achieve that put CRDs in `crds` folder. Helm will install them first.
These CRDs are not templated, but will be installed by default when running a helm install for the chart. 
If the CRD already exists, it will be skipped with a warning. 
To skip the CRD installation step pass the --skip-crds flag.
There is no support at this time for upgrading or deleting CRDs using Helm.
A possible solution is to store the CRD in a separate chart and install it before the main chart.
See more info in [Helm docs](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/).

## CRD charts
### CRD with crds folder
See `helm-packaging/crd-chart`

The chart uses a `crds` folder to make sure the CRD is registered before everything else.
The instance of a CRD is included into `templates` folder and will be deployed after CRD.
The custom resource instance manifest `evc.yaml` is included into the chart. 
You don't need to wait for the controller deployment to be available before installing a custom resource instance thanks to the watch stream replay capability.

Pros:
- Simple, no additional code to wait for resource creation
- A single chart can be used to add both CRD and a custom resource instance.
Cons:
- CRD Helm functionality is limited: dry run, templating, update and delete won't work out of the box.

To delete the chart release, run
```commandline
kubectl uninstall <release-name>
kubectl delete crd ephemeralvolumeclaims.kopf.dev
```

### CRD in `templates` folder
See `helm-packaging/crd-template-chart` and `helm-packaging/crd-controller-chart`

In this chart option CRD is a part of `templates` and multiple charts are needed.
The custom resource instance is in a separate chart and a post-install hook is added. 
The `install`/`upgrade` command will wait until the CRD is registered before returning.
This way everything installed after the chart will be able to use the CRD.

Controller is in a second chart installed after the first one.
As before there is no need to wait for the controller deployment to be available to start creating custom resources,
but it is possible to add `--wait` option to install/upgrade command which will wait for Deployment resources.
```commandline
kubectl install release1 ./crd-template-chart
kubectl install release2 ./crd-controller-chart --wait
```

Pros:
- CRD templates support all the usual Helm functionality (upgrade, delete, dry run, template)
- Can easily wait for the controller Deployment to finish if needed
Cons: 
- more complicated charts structure, the options are:
  1. two separate charts: one for crd, one for controller. Controller chart may include custom resources instances, crd - no.
  2. Alternatively, to keep CRD and its controller together and keep custom resources separately, the controller needs to be able to restart the watch loop in case it starts first and crd is not registered yet

See [docs](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/#install-a-crd-declaration-before-using-the-resource),
[hip-0011](https://github.com/helm/community/blob/main/hips/hip-0011.md)

### Other approaches that did not work
Didn't work: CRD as a pre-install hook with order=0 and add a pre-install hook with order=1 to wait for CRD creation.
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: ephemeralvolumeclaims.kopf.dev
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "0"
...
```
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: wait-for-crd
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": hook-succeeded,hook-failed
spec:
  template:
    spec:
      serviceAccountName: crd-controller-sa
      containers:
        - name: wait-for-crd
          image: bitnami/kubectl:1.21
          command:
            - /bin/sh
            - -c
            - |
              set -e
              echo "Waiting for CRD to be available..."
              kubectl wait --for=condition=Established --timeout=120s crd ephemeralvolumeclaims.kopf.dev
      restartPolicy: Never
  backoffLimit: 1
```
Didn't work: CRD with a post-install wait hook in a dependency chart, referenced in the main chart like this:
```yaml
...
dependencies:
  - name: crd-dependent-chart
    version: 0.1.0
    repository: "file://../crd-dependent-chart"
```

## Notes on best practices
.yaml for YAML files and .tpl for helpers are recommended.

Keep your values trees shallow, favoring flatness.

Creating a NOTES.txt file is strongly recommended, though it is not required.

The .helmignore file is used to specify files you don't want to include in your helm chart.

## Publish to Github
Package the chart into a .tgz file
```commandline
helm package basic-apiservice-chart
```
This command will create a .tgz file in your current directory.

Create an index.yaml file:
```commandline
helm repo index --url https://<github-username>.github.io/<repo-name>/ .
```

Add the packaged chart (chart-example-0.1.0.tgz) and index.yaml to your repository.
Commit and push these files to your repository.

Enable GitHub Pages: in your repository, go to the Settings tab, find the Pages section, and select the branch and folder where your charts are located (usually main or master and / (root)).
GitHub Pages provides a convenient way to host static content directly from a GitHub repository

![example](github-pages.png)

Use your repo:
```commandline
helm repo add myrepo https://<username>.github.io/<repository>/
helm repo update
helm install myrelease myrepo/chart-example
```
## Links
[Helm tutorial](https://helm.sh/docs/chart_template_guide/getting_started/)
[Helm best practices](https://helm.sh/docs/chart_best_practices/)
