#!/bin/bash
cd /home/smartrack/smartrack-pi
source .venv/bin/activate
nohup streamlit run /home/smartrack/smartrack-pi/smartrack_pi/app.py --server.port=8501 --server.address=0.0.0.0