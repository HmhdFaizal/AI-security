# AI-Security   
**Cross-Platform AI-Based Endpoint Security System**

AI-Security is a cross-platform, behavior-based security tool inspired by modern EDR (Endpoint Detection & Response) solutions.  
It uses machine learning to detect anomalous **process** and **network** behavior instead of relying on traditional virus signatures.

This project is designed for **learning, experimentation, and portfolio demonstration**.

---

## Features
- Cross-platform support (Linux, Windows, macOS)
- Behavior-based anomaly detection (no signatures)
- Machine Learning using **Isolation Forest**
- Process activity monitoring (CPU & memory)
- Network behavior monitoring (process → remote IP)
- Persistent learning & detection states
- Modular, professional project architecture

---

## How It Works
1. **Learning Mode**
   - Observes normal system behavior
   - Records CPU & memory usage of running processes
   - Builds a baseline for the current operating system

2. **Detection Mode**
   - Trains an AI model on baseline data
   - Monitors live processes and network connections
   - Flags repeated anomalous behavior
   - Maintains anomaly history across runs

> An anomaly does **not** automatically mean malware — it indicates behavior that deviates from learned norms.

---

## Architecture Overview
