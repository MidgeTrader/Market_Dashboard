@echo off
echo Updating dashboard data...
python scripts/build_data.py --out-dir data
echo.
echo Starting local server at http://localhost:8000...
echo Close this window to stop the server.
start http://localhost:8000
python -m http.server 8000
