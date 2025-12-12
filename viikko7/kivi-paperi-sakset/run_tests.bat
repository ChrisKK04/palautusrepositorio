@echo off
REM Windows batch script to run tests

cd "%~dp0src"
"%~dp0.venv\Scripts\python.exe" -m pytest test_app.py -v
