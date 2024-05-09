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

# Links
[Helm tutorial](https://helm.sh/docs/chart_template_guide/getting_started/)
[Helm best practices](https://helm.sh/docs/chart_best_practices/)
