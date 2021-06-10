@echo off
call activate vaccine_sched

@echo on
python Scheduler.py -l 45 -o -75

@echo off
call conda deactivate
goto:eof