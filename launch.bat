@echo off
REM EmailIntelligence Launcher for Windows
REM This script forwards to the actual launch.bat in the setup subtree
REM It maintains backward compatibility for references to launch.bat in the root directory

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Execute the actual launch.bat in the setup subtree with all arguments
call "%SCRIPT_DIR%setup\launch.bat" %*

REM Preserve the exit code
exit /b %ERRORLEVEL%