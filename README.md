#Federated Distributed Secure Key Management System

A **distributed, federated key management system** that securely stores and reconstructs cryptographic keys using independent nodes, secure REST APIs, and a centralized reconstruction service. Built with **Python and Flask**, this project demonstrates modern **distributed security architecture**, **zero-trust principles**, and **secure key fragmentation**.

---

#Table of Contents

* Overview
* Key Features
* System Architecture
* Core Concepts
* How the System Works
* Component Breakdown
* Security Model
* Project Structure
* Installation
* Running the System
* API Reference
* Example Workflow
* Real-World Applications
* Future Improvements

---

#Overview

Traditional systems store cryptographic keys in a single location, creating a **single point of failure**. If that system is compromised, the entire key is exposed.

This project solves that problem using a **federated distributed architecture**, where:

* The key is split into fragments
* Each fragment is stored on a separate node
* Nodes communicate using secure APIs
* The full key is reconstructed only when authorized
* All activity is monitored and logged

No single node ever possesses the full key.

---

#Key Features

Distributed key storage
Federated node architecture
Secure key reconstruction process
REST APIs using Flask
Node health monitoring
Audit logging system
Dashboard integration
Fault-tolerant design
Zero-trust inspired model

---

#System Architecture

```
                    ┌─────────────────────────┐
                    │       Dashboard         │
                    │ Monitoring & Audit Log │
                    └────────────┬────────────┘
                                 │
                          Secure API Calls
                                 │
                    ┌────────────▼────────────┐
                    │ Key Reconstruction Core │
                    │   Secure Aggregator    │
                    └──────┬──────┬──────────┘
                           │      │
            ┌──────────────┘      └──────────────┐
            │                                     │
     ┌──────▼──────┐                     ┌───────▼──────┐
     │   Node 1    │                     │    Node 2     │
     │ Flask Server│                     │ Flask Server  │
     │ Key Fragment│                     │ Key Fragment  │
     └──────┬──────┘                     └───────┬──────┘
            │                                     │
            └──────────────┬──────────────┬──────┘
                           │              │
                     ┌─────▼─────┐ ┌─────▼─────┐
                     │   Node 3  │ │   Node N  │
                     │ Fragment  │ │ Fragment  │
                     └───────────┘ └───────────┘
```

---

#Core Concepts

## Federated System

A federated system consists of **independent nodes cooperating without centralized data storage**.

Each node:

* Operates independently
* Stores only partial data
* Communicates via APIs

Example real-world systems:

Cloud key management services
Blockchain networks
Distributed authentication systems

---

## Key Fragmentation

Instead of storing:

```
FULL KEY:
A94F3D82C1B7E6F9
```

The system stores:

```
Node 1 → A94F3
Node 2 → D82C1
Node 3 → B7E6F9
```

No node has the complete key.

---

## Key Reconstruction

The central reconstruction service:

Requests fragments from nodes
Receives fragments securely
Combines fragments
Rebuilds the original key

Example:

```
fragment1 + fragment2 + fragment3 = full key
```

---

## Flask REST APIs

Each node runs a Flask server exposing secure endpoints.

Example:

```
GET /status
GET /fragment
```

Example implementation:

```python
@app.route("/fragment")
def fragment():
    return {"fragment": load_fragment()}
```

---

## Dashboard and Monitoring

The dashboard monitors:

Node status
Fragment availability
Reconstruction events
Security logs

This simulates a real Security Operations Center.

---

## Audit Logging

Every operation is logged:

```
[INFO] Node 1 responded
[INFO] Fragment received
[INFO] Reconstruction successful
```

Purpose:

Security auditing
Debugging
Incident analysis

---

#How the System Works

Step 1 — Node startup

Each node starts a Flask server:

```
python node.py
```

---

Step 2 — Fragment loading

Node loads fragment from:

```
data.txt
```

Example:

```
NODE_ID=1
KEY_FRAGMENT=A94F3
```

---

Step 3 — Reconstruction request

Central service sends request:

```
GET http://node1:5000/fragment
```

---

Step 4 — Fragment transmission

Node responds:

```
{
  "fragment": "A94F3"
}
```

---

Step 5 — Key reconstruction

Central service combines fragments:

```
A94F3 + D82C1 + B7E6F9
```

---

Step 6 — Logging and monitoring

Dashboard updates system status.

---

#Component Breakdown

## Federated Nodes

Responsibilities:

Store key fragment
Expose secure API
Report status
Respond to reconstruction requests

Files:

```
node/app.py
node/data.txt
```

---

## data.txt

Secure local fragment storage.

Example:

```
NODE_ID=2
KEY_FRAGMENT=D82C1
STATUS=ACTIVE
```

---

## Reconstruction Service

Responsibilities:

Contact nodes
Collect fragments
Rebuild key
Log operations

File:

```
reconstruct.py
```

Example:

```python
import requests

nodes = ["http://localhost:5001", "http://localhost:5002"]

fragments = []

for node in nodes:
    response = requests.get(node + "/fragment")
    fragments.append(response.json()["fragment"])

key = "".join(fragments)
```

---

## Dashboard

Responsibilities:

Display node health
Display logs
Monitor system

Simulates enterprise monitoring tools.

---

#Security Model

This system protects against:

Server compromise
Single-point failure
Key theft
Unauthorized access

Zero-Trust principle:

No node is fully trusted.

Even if one node is hacked, the attacker cannot reconstruct the key.

---

#Project Structure

```
federated-key-management/

│
├── nodes/
│   ├── node1/
│   │   ├── app.py
│   │   └── data.txt
│   │
│   ├── node2/
│   │   ├── app.py
│   │   └── data.txt
│   │
│   └── node3/
│       ├── app.py
│       └── data.txt
│
├── reconstruction/
│   └── reconstruct.py
│
├── dashboard/
│   └── monitor.py
│
└── README.md
```

---

#Installation

Install dependencies:

```
pip install flask requests
```

---

#Running the System

Start nodes:

```
python nodes/node1/app.py
python nodes/node2/app.py
python nodes/node3/app.py
```

Run reconstruction:

```
python reconstruction/reconstruct.py
```

---

#API Reference

## Node Status

```
GET /status
```

Response:

```
{
 "status": "active"
}
```

---

## Get Key Fragment

```
GET /fragment
```

Response:

```
{
 "fragment": "A94F3"
}
```

---

#Example Output

```
Connecting to Node 1...
Fragment received

Connecting to Node 2...
Fragment received

Connecting to Node 3...
Fragment received

Key reconstructed successfully
Key: A94F3D82C1B7E6F9
```

---

#Real-World Applications

Cloud key management (AWS KMS)
Cryptocurrency wallets
Distributed authentication systems
Military secure communication
Enterprise encryption systems

---

#Why This Architecture Matters

Traditional system:

```
One server → Full key → High risk
```

Distributed system:

```
Multiple nodes → Partial keys → High security
```

No single point of compromise.

---

#Future Improvements

Shamir Secret Sharing implementation
TLS encrypted communication
Authentication tokens
Docker container deployment
Web-based dashboard
Database storage
Automatic node discovery

---

#Academic Context

This project demonstrates concepts in:

Distributed Systems
Cybersecurity
Secure Key Management
Federated Architectures
REST API Communication

Suitable for university-level cybersecurity and distributed systems courses.

---
