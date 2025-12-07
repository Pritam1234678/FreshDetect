@echo off
echo Initializing Git Repository...

echo # FreshDetect > README.md
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Pritam1234678/FreshDetect.git

echo.
echo ========================================================
echo Repo initialized!
echo Now run this command manually to upload:
echo    git push -u origin main
echo ========================================================
pause
