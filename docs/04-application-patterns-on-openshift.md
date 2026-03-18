# Application Patterns on OpenShift

## The Patterns That Actually Mattered
A private AI application on OpenShift does not need a giant microservice fleet to feel production-grade. What mattered most in this environment was getting a small set of patterns right:
- namespace isolation
- correct rollout mechanics
- good readiness and health checks
- durable state
- sane resource requests and limits
- route behavior that supports streaming
- logs that separate noise from real failures

## Namespace Isolation
Use separate namespaces for:
- production
- staging
- any notebook or evaluation space

That separation gives you:
- safer rollouts
- easier cleanup
- cleaner RBAC
- clearer quota and resource tracking
- fewer surprises during demos

Representative pattern:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: private-ai-app
```

## Web Tier Pattern
The web tier in this environment was a Flask-style app behind Gunicorn.

What worked:
- multiple replicas for the web layer
- health and readiness probes tuned for quick failure detection
- thread-capable workers for SSE and long-held connections
- a clean separation between web tier and inference lane

Representative deployment fragment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-web
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    spec:
      containers:
      - name: web
        image: example.com/private-ai-app/web:prod
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 20
```

## SSE and Route Configuration
Streaming is one of the easiest ways to make an AI app feel broken if the route path buffers or times out incorrectly.

What mattered:
- route annotations that reduce buffering problems
- app responses that explicitly discourage intermediary buffering
- Gunicorn worker behavior that tolerates longer-lived streams

Representative route fragment:
```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: ai-web
  annotations:
    haproxy.router.openshift.io/timeout: 5m
    haproxy.router.openshift.io/disable_cookies: 'true'
spec:
  to:
    kind: Service
    name: ai-web
  tls:
    termination: edge
```

## PostgreSQL Pattern
The database change from SQLite to PostgreSQL was one of the highest-value improvements in the whole program.

Representative stateful pattern:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ai-postgres
spec:
  serviceName: ai-postgres
  replicas: 1
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:16
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ReadWriteOnce]
      resources:
        requests:
          storage: 50Gi
```

## Inference Gateway Pattern
A dedicated inference gateway kept application logic and model execution loosely coupled.

That gave the system:
- a place to make serving-lane decisions
- a simpler app tier
- an easier CPU fallback path
- a cleaner OpenShift AI / KServe integration

Representative deployment fragment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-inference-gateway
spec:
  replicas: 2
  template:
    spec:
      nodeSelector:
        workload-role: ai-serving
      containers:
      - name: gateway
        image: example.com/private-ai-app/gateway:prod
        resources:
          requests:
            cpu: "2"
            memory: 4Gi
          limits:
            cpu: "8"
            memory: 24Gi
```

## Resource Requests and Limits
One of the easiest mistakes in an AI application is setting limits based on theoretical maximum desire rather than measured need.

What we learned:
- overcommit warnings are not cosmetic
- limits that look harmless in a spreadsheet become operationally dangerous during upgrades or burst traffic
- requests should reflect typical need
- limits should reflect realistic headroom, not fantasy peak values

Operational rule:
- measure first
- set requests second
- set limits conservatively enough that the cluster can still drain and recover

## PVC Management
Persistent volumes had to be used deliberately.

Distinct classes of storage:
- PostgreSQL PVCs for application truth
- Signal or other tool-specific PVCs for restart-sensitive state
- AI model cache PVCs or local storage for large model artifacts

Do not blur these together.

## ConfigMap Pattern
ConfigMaps were useful for:
- feature flags
- environment-level behavior
- rollout-safe config changes
- version-visible deployment metadata

Representative fragment:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ai-env-config
Data:
  APP_VERSION: vX.Y.Z
  ENABLE_KSERVE: "true"
  ENABLE_SIGNAL: "true"
```

## Secret Management
Secrets belonged in Kubernetes Secrets, not in ConfigMaps or checked-in files.

That includes:
- API keys
- OAuth client secrets
- database credentials
- provider tokens

Representative fragment:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ai-app-secrets
type: Opaque
stringData:
  POSTGRES_PASSWORD: change-me
  OAUTH_CLIENT_SECRET: change-me
```

## Zero-Downtime Rollouts
Zero-downtime rollouts were not optional polish. They were required to keep trust in the platform.

A healthy rollout routine looked like:
1. build the image
2. apply manifests
3. wait for rollout success
4. hit `/health`
5. hit `/api/meta`
6. inspect logs immediately
7. verify routes and serving lanes

## HPA and PDB Patterns
Use HPAs and PDBs carefully.

HPAs help when:
- traffic is bursty
- startup behavior is already clean
- readiness is honest

PDBs help when:
- you test them before an upgrade
- they do not accidentally block normal maintenance

Representative fragment:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ai-web-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: ai-web
```

## Build Strategy
A Dockerfile-based build path was a good fit because it gave predictable control over:
- Python dependencies
- runtime packages such as OCR or Java dependencies
- signal or helper tooling
- exact image contents during repeated rollouts

S2I is viable in many environments, but the Dockerfile path was easier to reason about for this platform.

## The Main Pattern To Keep
The best OpenShift pattern for a private AI application is not complexity. It is disciplined separation:
- web tier for UX and auth
- gateway tier for serving decisions
- stateful tier for truth
- dedicated inference lane for heavy work
