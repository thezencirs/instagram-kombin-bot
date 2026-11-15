@echo off
cd /d "C:\Users\zenci\.gemini\antigravity\scratch\instagram-kombin-bot"
"C:\Users\zenci\.gemini\antigravity\scratch\tools\python\tools\python.exe" -X utf8 -u "src\continuous_flow_kombin_daemon.py" --daemon --interval-min 90 >> "output\continuous_flow_daemon_stdout.log" 2>&1
