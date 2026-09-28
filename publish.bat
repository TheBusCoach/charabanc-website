@echo off
REM ------------------------------------------------------------------
REM  Publish charabancfinancial.com
REM  Double-click this file. It rebuilds the site, commits every change,
REM  and pushes to GitHub. Netlify goes live about a minute later.
REM ------------------------------------------------------------------
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
  echo Building site...
  python build_site.py || goto :fail
  python build_pages.py || goto :fail
) else (
  echo Python not found - skipping rebuild and publishing the site folder as-is.
)

echo.
echo Committing changes...
git add -A
git diff --cached --quiet && (
  echo Nothing changed - nothing to publish.
  goto :done
)
set "MSG=Site update %date% %time:~0,5%"
if not "%~1"=="" set "MSG=%~1"
git commit -m "%MSG%" || goto :fail

echo.
echo Pushing to GitHub...
git push origin main || goto :fail

echo.
echo Done. Netlify will publish in about a minute.
goto :done

:fail
echo.
echo Something went wrong - see the messages above.

:done
echo.
pause
