@echo off

REM Parse pip info command
if exist .spotisyncupdate del .spotisyncupdate
pip show spotdl | findstr Requires > .spotisyncupdate
set /p requires=<.spotisyncupdate
del .spotisyncupdate

REM Remove "Requires:" by splitting by colons
for /f "tokens=2 delims=:" %%a in ("%requires%") do (
    set requires=%%a
)

REM Remove commas and construct final command
set command=pip install --upgrade%requires:,=%

REM Run the install command
%command%
