{{/*
Expand the name of the chart.
*/}}
{{- define "apiservice-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Add version.
*/}}
{{- define "apiservice-chart.version" -}}
labels:
  app_version: "{{ .Chart.Version }}"
  app_test: "smth"
{{- end }}
