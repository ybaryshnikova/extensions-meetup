{{/*
Expand the name of the chart.
*/}}
{{- define "chart-example.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Add version.
*/}}
{{- define "chart-example.version" -}}
app_version: "{{ .Chart.Version }}"
{{- end }}
