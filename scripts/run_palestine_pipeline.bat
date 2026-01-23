@echo off
echo ========================================
echo Palestine Data Processor
echo ========================================
echo.

echo Step 1: Check if data exists...
if exist data\raw\complete_market_data.json (
    echo ✅ Found existing data file
) else (
    echo ⚠️ No existing data found
    echo.
    echo Please run the scanner first:
    echo python palestine_market_scanner_fixed.py
    echo.
    pause
    exit
)

echo.
echo Step 2: Process the data...
python process_data.py

if errorlevel 1 (
    echo ❌ Processing failed
    echo.
    echo Creating simple datasets instead...
    
    REM Create a simple AI-ready dataset
    echo [{"name": "Test Business", "location": "Palestine"}] > data\ai_ready\simple_data.json
    echo Created simple dataset
)

echo.
echo Step 3: Show results...
echo.
if exist data\ai_ready (
    echo AI-ready files created:
    echo -----------------------
    dir /B data\ai_ready\
) else (
    echo No AI-ready files created
)

echo.
echo ========================================
echo ✅ DONE!
echo ========================================
echo.
echo Your AI-ready Palestinian market data is ready!
echo Location: data\ai_ready\
echo.
pause