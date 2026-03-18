# OpenShift AI and AAP

## Why These Products Mattered
OpenShift AI and Ansible Automation Platform were not used here as slideware. They became useful once the base application was stable enough to benefit from them.

That sequencing mattered.

If the base app is still unstable, OpenShift AI and AAP can add complexity without adding clarity. Once the base platform is stable, they become force multipliers.

## What OpenShift AI Contributed
OpenShift AI made the architecture more credible in four ways:
- it gave the cluster a first-class model-serving story
- it provided a clean KServe object model for serving workloads
- it enabled notebook-based demos and evaluation
- it created a clearer separation between app-plane and serving-plane concerns

## KServe / InferenceService Pattern
The practical pattern used here was:
- the application retained responsibility for auth, UX, request handling, and policy
- OpenShift AI hosted an explicit serving lane for cluster-local models
- the serving lane ran on the dedicated AI worker instead of competing with compact control-plane nodes

Representative sanitized InferenceService fragment:
```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: ai-worker-llama
spec:
  predictor:
    minReplicas: 1
    nodeSelector:
      workload-role: ai-serving
    containers:
    - name: predictor
      image: example.com/private-ai-app/llama-server:prod
      env:
      - name: MODEL_PATH
        value: /models/qwen2.5-7b-instruct.gguf
      volumeMounts:
      - name: model-cache
        mountPath: /models
```

## What OpenShift AI Was Good At
### Serving clarity
It gave the operator a clean object to inspect:
- is the InferenceService ready?
- what image is deployed?
- what node is hosting it?
- is the backing service responding?

### Demo credibility
For customer or stakeholder demos, it is powerful to show:
- the application route
- the OpenShift AI dashboard
- the InferenceService object
- the notebook used for validation

### Evaluation workspace
A notebook with a short validation script is much more useful than an empty notebook environment.

A good demo notebook shows:
- cluster metadata
- serving endpoint readiness
- sample latency numbers
- a few prompts that prove the lane is alive

## What AAP Contributed
AAP fit best as an operations automation layer.

Useful AAP jobs included:
- health snapshots across operators, namespaces, and routes
- pre-demo validation
- post-deploy verification
- rollout checklists for AI-serving components
- benchmark or health summaries that can be reused in meetings

Representative playbook fragment:
```yaml
---
- name: Capture private AI platform health snapshot
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Check cluster operators
      command: oc get co
      register: co_out
      changed_when: false

    - name: Check app pods
      command: oc -n private-ai-app get pods
      register: pods_out
      changed_when: false

    - name: Show summary
      debug:
        msg:
          - "Cluster operators checked"
          - "Application namespace checked"
```

## What Was Worth The Effort
Worth it:
- KServe as a dedicated serving lane
- notebooks as demo and validation tooling
- AAP for repeatable ops checks and walkthrough prep

Less valuable than expected:
- trying to push all application behavior into the AI platform objects
- using AAP where a simple shell script or single `oc` probe was already sufficient

## Recommended Usage Model
Use OpenShift AI when you need:
- a real serving story
- a KServe object model
- notebooks for evaluation and demos
- a cleaner separation between app engineering and model serving

Use AAP when you need:
- repeatable operations checks
- pre-demo or pre-release verification
- a reusable automation record for tasks operators will run repeatedly

Do not assume either one replaces application engineering. They strengthen the platform. They do not remove the need for clear app behavior.
