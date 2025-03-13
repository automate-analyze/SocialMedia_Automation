@echo off
cd /d C:\Development\Portfolio\SocialMedia_Automation
call sm_auto\Scripts\activate.bat
sm_auto\Scripts\python.exe fb_posts.py
deactivate
pause
exit