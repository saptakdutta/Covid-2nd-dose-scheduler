@echo off
call activate vaccine_sched

@echo on
python Scanner.py -cfg Clients-dev.csv
python Scheduler.py -lat 45.3640192 -lng -75.710464 -cfg Config-dev.json
python Mailer.py

@echo off
call conda deactivate
goto:eof