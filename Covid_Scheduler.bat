@echo off
call activate vaccine_sched

@echo on
python Scheduler.py

@echo off
call conda deactivate
goto:eof