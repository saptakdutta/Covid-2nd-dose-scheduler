@echo off
call activate vaccine_sched

@echo on
python Scheduler.py -lat 45.3640192 -lng -75.710464 -cfg Config-dev.json

@echo off
call conda deactivate
goto:eof