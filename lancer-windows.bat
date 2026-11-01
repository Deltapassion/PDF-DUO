@echo off
REM Lance PDF DUO sous Windows (Python 3 et pip install -r requirements.txt requis)
cd /d "%~dp0"
pythonw pdfduo.py %*
