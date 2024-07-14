{{/*
Expand the name of the chart.
*/}}
{{- define "basic-apiservice-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Add version.
*/}}
{{- define "basic-apiservice-chart.version" -}}
labels:
  app_version: "{{ .Chart.Version }}"
  app_test: "smth"
{{- end }}
