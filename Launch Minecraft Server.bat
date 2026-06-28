@echo off
title Minecraft Server Launcher

echo ==========================
echo Starting Minecraft Server...
echo ==========================

start "" "%~dp0run.bat"

echo.
echo ==========================
echo Starting Server Monitor...
echo ==========================

start "" "%~dp0shutdown_monitor.bat"

exit