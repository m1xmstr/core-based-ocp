# Architecture Diagrams

These diagrams are sanitized and intentionally generic, but they are based on the real reference architecture documented in this repository.

## 1. Cluster topology
```mermaid
graph TB
  subgraph "Compact Nodes (x3)"
    CP1["Control Plane 1<br/>Mini PC, 64GB"]
    CP2["Control Plane 2<br/>Mini PC, 64GB"]
    CP3["Control Plane 3<br/>Mini PC, 64GB"]
  end
  subgraph "AI Worker"
    W1["AI Worker 1<br/>Strix Halo, 128GB<br/>GPU: gfx1151"]
  end
  subgraph "Storage"
    ODF["ODF/Ceph<br/>Distributed across CP1-3"]
    NVMe["NVMe Model Cache<br/>2TB on AI Worker"]
  end
  CP1 --- CP2 --- CP3
  CP1 --> W1
  W1 --> NVMe
  CP1 --> ODF
  CP2 --> ODF
  CP3 --> ODF
```

## 2. Inference routing
```mermaid
graph LR
  User["User"] --> Route["OCP Route + TLS"]
  Route --> Web["Web Tier x3"]
  Web --> Classify["Prompt Classifier"]
  Classify -->|simple| Fast["Fast Path<br/>Smallest model"]
  Classify -->|complex| Quality["Quality Path<br/>Largest model"]
  Classify -->|thinking| Think["Reasoning Path<br/>Longer chain"]
  Fast --> GPU["AI Worker GPU"]
  Quality --> GPU
  Think --> GPU
  GPU -->|streaming| User
```

## 3. Storage architecture
```mermaid
graph TB
  subgraph "Persistent Storage"
    PG["PostgreSQL<br/>ODF PVC"]
    Signal["Signal CLI<br/>Dedicated PVC"]
    Models["Model Cache<br/>Local NVMe 2TB"]
  end
  subgraph "Ephemeral"
    Container["Container filesystem<br/>logs, temp files"]
  end
  Web["Web pods"] --> PG
  Core["Core pod"] --> Signal
  Inference["Inference pods"] --> Models
  Web --> Container
  Core --> Container
  Inference --> Container
```

## 4. Edge to application path
```mermaid
graph LR
  Client["Browser / API Client"] --> DNS["Public DNS / CDN"]
  DNS --> Edge["Edge TLS / reverse proxy"]
  Edge --> Route["OpenShift Route"]
  Route --> Web["ai-web"]
  Web --> PG["PostgreSQL"]
  Web --> Gateway["Inference gateway"]
  Gateway --> CPU["CPU fallback"]
  Gateway --> GPU["Dedicated AI worker"]
  Gateway --> KServe["OpenShift AI / KServe"]
```
