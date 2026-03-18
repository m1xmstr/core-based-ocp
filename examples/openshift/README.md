# Sanitized OpenShift Examples

These examples show the general shape we found useful for a private AI
application on OpenShift.

They are sanitized by design:
- no real domains
- no real cluster names
- no real namespaces from the private platform
- no private model catalogs or product logic
- no real storage class names or hardware-specific selectors beyond generic roles

Files included:
- `namespace.yaml`: generic namespace and labels
- `configmap.yaml`: non-secret runtime settings
- `deployment-web.yaml`: web/API deployment with streaming-friendly Gunicorn settings
- `deployment-inference-gateway.yaml`: generic inference gateway deployment
- `service-and-route.yaml`: service and route examples
- `inferenceservice-amd-vulkan.yaml`: generic KServe example for a dedicated AI worker
- `hpa-and-pdb.yaml`: baseline HPA and PDB examples
- `kustomization.yaml`: simple composition entrypoint

How to read these examples:
- start with `namespace.yaml` and `configmap.yaml` to understand the naming pattern
- deploy the web plane and inference gateway separately so you can scale and debug them independently
- treat the `InferenceService` as a specialized serving lane for heavier models or hardware acceleration
- replace the generic images, namespaces, and route hosts with values from your own environment

Adapt this for your environment:
- replace `private-ai-app` with your namespace
- replace example container images with your own registry path
- replace the `emptyDir` model cache with a PVC or node-local cache design
- adjust HPA and PDB settings to match your cluster size and disruption tolerance
- swap the example model filename for something your runtime can actually load

What these examples are meant to teach:
- keep the app plane and inference plane distinct
- label and pin dedicated AI-serving nodes intentionally
- use HPA and PDB conservatively on compact clusters
- always pair manifests with rollout verification and logs
