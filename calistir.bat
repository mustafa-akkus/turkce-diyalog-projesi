@echo off
chcp 65001 >nul
set PYTHON_EXE="C:\Users\Musta\AppData\Local\Python\pythoncore-3.14-64\python.exe"

echo ========================================================
echo   TURKCE DIYALOG AJANI - BASELINE MODEL (TF-IDF)
echo ========================================================
echo 1. Tum Sureci Calistir (Veri Bolme + Egitim + Degerlendirme)
echo 2. Canli Sohbeti Baslat (Soru-Cevap Testi)
echo 3. Ornek Sorularla Demo Testi Yap
echo ========================================================
set /p secim="Seciminiz (1/2/3): "

if "%secim%"=="1" (
    %PYTHON_EXE% src/preprocessing.py
    %PYTHON_EXE% src/train.py
    %PYTHON_EXE% src/evaluate.py
    pause
) else if "%secim%"=="2" (
    %PYTHON_EXE% src/inference.py
    pause
) else if "%secim%"=="3" (
    %PYTHON_EXE% src/inference.py --demo
    pause
) else (
    echo Gecersiz secim!
    pause
)
