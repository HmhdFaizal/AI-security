# AI Security Monitor 

A beginner-friendly AI-inspired system monitoring tool built with Python on Linux.

## What it does
- Monitors running system processes
- Tracks CPU and memory usage
- Applies risk scoring to detect suspicious behavior
- Learns normal system behavior over time

## How it works
This tool uses behavior-based detection instead of signature-based scanning.
Processes are evaluated using:
- Process name
- CPU usage
- Memory usage

A simple risk score is calculated to flag abnormal behavior.

##Tech Stack
- Python 3
- psutil
- Linux (Mint / Ubuntu)

##How to run
```bash
python security_ai.py
