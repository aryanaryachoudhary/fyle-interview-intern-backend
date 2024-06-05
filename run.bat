@REM Added by me

@echo off

REM Set environment variable
set FLASK_APP=core/server.py

REM Uncomment the following lines if you want to run migrations
REM flask db init -d core/migrations/
REM flask db migrate -m "Initial migration." -d core/migrations/
REM flask db upgrade -d core/migrations/

REM Run server
@REM waitress-serve --call 'core.server:app'
waitress-serve core.server:app


