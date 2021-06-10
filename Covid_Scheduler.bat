@echo off
call activate vaccine_sched

@echo on
python Scheduler.py -lat 45 -lng -75

@echo off
call conda deactivate
goto:eof