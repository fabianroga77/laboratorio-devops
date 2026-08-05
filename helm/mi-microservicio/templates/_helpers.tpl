{{/*
Plantillas reutilizables de Helm.
Evitan repetir nombres y labels en deployment.yaml y service.yaml.
*/}}

{{/* nombre del recurso, ej: mi-microservicio-mi-microservicio */}}
{{- define "mi-microservicio.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* labels que ves en kubectl get pods --show-labels */}}
{{- define "mi-microservicio.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* labels minimas para que Service encuentre los pods correctos */}}
{{- define "mi-microservicio.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
