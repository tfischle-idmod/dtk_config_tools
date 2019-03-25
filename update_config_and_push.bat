@echo off

REM some constants
set TempBranch=update_config
set AllTests=generic,vector,malaria,sti,hiv,tb,environmental,polio,py,tbhiv,typhoid,dengue,serialization
set SkipedTests=typhoid,dengue,serialization

IF "%~1"=="" (GOTO No_Parameters) ELSE (GOTO Param_Branch)

:No_Parameters
echo Please define a branch to be checked out.
echo Usage: 
echo %0 branch e.g. %0 remote/TBHIV-Ongoing
echo To create a new branch %TempBranch% use -new-branch parameter, e.g.  %0 remote/TBHIV-Ongoing -new-branch
exit /B

:Param_Branch
echo This script reset the index and working tree. Any changes to tracked files in the working tree since last commit are discarded.
echo Checking out: %1
IF "%2"=="-new-branch" (echo A new branch %TempBranch% will be created)

:Skip_Message
set /p cont=Continue [y/n]?:

IF NOT %cont%==y IF NOT %cont%==Y exit /B

REM set CheckoutBranch=ifdm/TBHIV-Ongoing
set CheckoutBranch=%1

REM pull current and reset
git reset --hard %CheckoutBranch%

REM compile
"C:\Program Files (x86)\MSBuild\14.0\Bin\MSBuild.exe" ..\EradicationKernel.sln /p:Configuration=Release

REM run all tests
"%IDM_PYTHON3_PATH%\python" regression_test.py %AllTests%

REM add all config.json
git add */config.json
git commit -m "update all config.json"

REM Not sure if we can branch and checkout after a commit
IF "%2"=="-new-branch" (echo Creating new branch %TempBranch%) ELSE (GOTO NO_NEW_BRANCH)
REM checkout branch
git branch %TempBranch%
git checkout %TempBranch%

REM push, did reset --hard so a push -f should be fine
git push --set-upstream -f origin %TempBranch%

:NO_NEW_BRANCH
git push -f