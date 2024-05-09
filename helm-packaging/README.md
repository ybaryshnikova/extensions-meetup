# Helm
```commandline
helm create chart-example
```

## Install a chart
```commandline
helm install release1 ./chart-example
helm get manifest release1
helm uninstall release1
```

## Update a chart
```commandline
helm upgrade release1 ./chart-example
```

## Run with individual params
```commandline
helm install custom-release ./chart-example --dry-run --debug --set image.pullPolicy=IfNotPresent
```

## Debugging
```commandline
helm install --debug --dry-run test-run ./chart-example
```

## Some best practices
.yaml for YAML files and .tpl for helpers are recommended.

Keep your values trees shallow, favoring flatness.

Creating a NOTES.txt file is strongly recommended, though it is not required.

The .helmignore file is used to specify files you don't want to include in your helm chart.

## Publish to Github
Package the chart into a .tgz file
```commandline
helm package chart-example/
```
This command will create a .tgz file in your current directory.

Create an index.yaml file:
```commandline
helm repo index --url https://<github-username>.github.io/<repo-name>/ .
```

Add the packaged chart (chart-example-0.1.0.tgz) and index.yaml to your repository.
Commit and push these files to your repository.

Enable GitHub Pages: in your repository, go to the Settings tab, find the Pages section, and select the branch and folder where your charts are located (usually main or master and / (root)).

Use your repo:
```commandline
helm repo add myrepo https://<username>.github.io/<repository>/
helm repo update
helm install myrelease myrepo/mychart
```
## Links
[Helm tutorial](https://helm.sh/docs/chart_template_guide/getting_started/)
[Helm best practices](https://helm.sh/docs/chart_best_practices/)
