# Operations Checklist

This runbook is written for operators running a private AI application on a compact OpenShift cluster with one dedicated AI-serving node. The exact namespaces, route names, and storage classes in your environment will differ. The patterns and commands below are intentionally sanitized but directly usable once adapted.

## Daily checks
### 1. Cluster health
```bash
oc get clusterversion version
oc get co
oc get nodes
oc get mcp
```

What to look for:
- all cluster operators available and not degraded
- all nodes `Ready`
- no machine config pool stuck progressing longer than expected

### 2. Application namespace health
```bash
oc -n private-ai-app get pods
oc -n private-ai-app get deploy
oc -n private-ai-app get hpa
oc -n private-ai-app get pdb
oc -n private-ai-app get pvc
```

What to look for:
- no crash loops
- no high restart counts creeping upward
- PDBs aligned with your replica counts
- PVCs still bound and healthy

### 3. Route and metadata checks
```bash
curl -fsS https://private-ai-app.example.com/health
curl -fsS https://private-ai-app.example.com/api/meta
```

What to look for:
- route resolves and returns healthy status quickly
- metadata reflects the version you believe is live

### 4. Log review
```bash
oc -n private-ai-app logs deploy/ai-web --since=30m | egrep 'ERROR|Traceback|502|503|504'
oc -n private-ai-app logs deploy/ai-core --since=30m | egrep 'ERROR|Traceback|WARNING'
oc -n private-ai-app logs deploy/ai-inference-gateway --since=30m | egrep 'ERROR|Traceback'
oc -n private-ai-app logs ai-postgres-0 --since=30m | egrep 'FATAL|PANIC|ERROR'
```

What to look for:
- fresh stack traces
- upstream timeouts
- bursty warnings that indicate a latent product or routing issue
- Postgres errors that imply state or storage trouble

### 5. Serving health
```bash
oc -n private-ai-app get inferenceservice
oc -n private-ai-app get pods -l app=ai-inference-gateway
oc -n private-ai-app top pods
```

What to look for:
- serving pods up and ready
- resource use aligned with expectations
- no signs of runaway memory growth or throttling

## Weekly checks
### 1. Resource review
```bash
oc adm top nodes
oc adm top pods -n private-ai-app
```

Questions to ask:
- are requests and limits still honest?
- are compact nodes carrying too much inference pressure?
- is the AI worker doing the heavy lifting you intended?

### 2. Alert review
```bash
oc get --raw /api/v1/namespaces/openshift-monitoring/services/https:alertmanager-main:9095/proxy/api/v2/alerts | jq '.[].labels.alertname' | sort -u
```

Questions to ask:
- which alerts are real problems?
- which alerts are accepted environmental constraints?
- do any historical alerts deserve a documented silence?

### 3. Upgrade readiness
```bash
oc adm upgrade
oc get co | grep -v 'True[[:space:]]*False[[:space:]]*False' || true
```

Questions to ask:
- is the cluster upgradeable?
- are any operators blocking the next patch or minor release?
- are app workloads prepared to drain cleanly?

### 4. Benchmark spot-check
```bash
curl -fsS https://private-ai-app.example.com/api/meta
oc -n private-ai-app logs deploy/ai-inference-gateway --since=1h | tail -100
```

Questions to ask:
- does first-token latency still feel normal?
- is the serving lane still using the models and device paths you expect?
- has any silent regression crept into the product experience?

## Monthly checks
### 1. Security and secrets review
```bash
oc -n private-ai-app get secrets
oc -n private-ai-app get sa
oc -n private-ai-app auth can-i --list
```

Tasks:
- rotate external API keys where appropriate
- review service-account scope
- remove stale credentials and old test secrets

### 2. Storage review
```bash
oc -n openshift-storage get pods
oc -n openshift-storage exec deploy/rook-ceph-tools -- ceph status
oc -n private-ai-app get pvc
```

Tasks:
- confirm storage health remains clean
- verify model-cache behavior if you use local NVMe
- review any persistent-volume growth that suggests data retention is drifting

### 3. Adjacent-endpoint review
If your platform includes adjacent compute endpoints, verify:
- they are reporting fresh health
- version drift is understood
- they are not being treated as routing candidates when their heartbeats are stale

## Deployment checklist
### Before a deploy
1. confirm git state is clean
2. bump the patch version
3. run targeted tests for the touched area
4. review current logs so you know whether an error is old or new
5. deploy to staging first when practical

### After a deploy
1. wait for rollout completion
2. verify route health and `/api/meta`
3. run one real product action, not just a liveness probe
4. review fresh logs for web, core, inference, and database
5. verify cluster operators stayed healthy
6. park staging if you are not actively using it

## Cluster upgrade checklist
### Before upgrading
1. confirm all operators healthy
2. confirm no application workload depends on an undrainable node
3. review PDBs and replica counts
4. review active alerts and decide which are real versus expected

### During the upgrade
1. watch operator progress
2. watch node readiness
3. do not stack unrelated application changes on top of a noisy cluster event unless you must

### After the upgrade
1. confirm `oc get co` is clean
2. verify application routes
3. verify serving endpoints and storage health
4. review pod restarts
5. document anything that changed operationally

## Demo-call checklist
If you are using the platform for a customer or stakeholder walkthrough:
1. confirm the public route loads cleanly
2. confirm `/api/meta` shows the expected version
3. confirm the serving endpoint is ready
4. run one short prompt and one longer prompt before the meeting
5. keep one OpenShift console view and one application view available
6. verify notebook or KServe assets if they are part of the demo story
