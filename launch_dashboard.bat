@echo off
title 🚀 NASA Bioscience Voice Dashboard

REM Activate virtual environment and run Flask API
start cmd /k "cd /d D:\nasa-biospace-llm\scripts && call ..\venv\Scripts\activate && python api.py"

REM Run Streamlit dashboard
start cmd /k "cd /d D:\nasa-biospace-llm\dashboard && call ..\venv\Scripts\activate && streamlit run app.py"

REM Open voice input interface in Chrome
start chrome http://localhost:5000/voice-ui
