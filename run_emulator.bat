@echo off
REM Train models (creates synthetic models if the dataset is missing).
py train_models.py

REM Start the Flask API in a new window.
start "Flask API" py api.py

REM Start the Streamlit app in a new window.
start "Streamlit App" py -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501

echo.
echo Streamlit should be accessible from the emulator at:
echo     http://10.0.2.2:8501

echo Flask API should be accessible from the emulator at:
echo     http://10.0.2.2:5000 (or 5001+ if 5000 is already in use)

echo.
echo Press any key to close this window.
pause >nul
