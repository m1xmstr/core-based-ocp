# OpenShift Examples

These files are sanitized examples based on the patterns that mattered most in the reference platform.

Use them to adapt the ideas for your environment. Do not expect them to be copy-paste production manifests.

Files included:
- `configmap.yaml`: version and feature-flag style configuration
- `deployment-web.yaml`: web deployment with probes and resource shape
- `deployment-inference-gateway.yaml`: dedicated inference gateway deployment
- `hpa-and-pdb.yaml`: basic autoscaling and disruption control
- `inferenceservice-amd-vulkan.yaml`: sanitized OpenShift AI / KServe serving example
- `service-and-route.yaml`: service plus route for user-facing traffic
