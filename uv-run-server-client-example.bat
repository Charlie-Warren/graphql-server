@echo off
REM Run app.main in a new window
start "Server" cmd /k uv run -m app.main

timeout /t 5 /nobreak >nul

REM Run example.py in a new window
start "Example Client" cmd /k uv run client_example.py
