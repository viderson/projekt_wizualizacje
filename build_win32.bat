@echo off

set ROOT=%cd%

if not exist %ROOT%\\bin mkdir %ROOT%\\bin
if not exist %ROOT%\\bin\\Windows mkdir %ROOT%\\bin\\Windows

pushd %ROOT%\\bin\\Windows

cl %ROOT%\\src\\run.c /DSETUP /Fesetup
cl %ROOT%\\src\\run.c /Ferun

del %ROOT%\\bin\\Windows\\run.obj

if not exist %ROOT%\\bin\\Windows\\templates mkdir %ROOT%\\bin\\Windows\\templates
if not exist %ROOT%\\bin\\Windows\\uploads mkdir %ROOT%\\bin\\Windows\\uploads
xcopy /y /q /s /e %ROOT%\\src\\templates %ROOT%\\bin\\Windows\\templates
xcopy /y /q /s /e %ROOT%\\src\\uploads %ROOT%\\bin\\Windows\\uploads

copy %ROOT%\\src\\dataHandler.py .\\
copy %ROOT%\\src\\generate_map.py .\\
copy %ROOT%\\src\\main.py .\\
copy %ROOT%\\src\\requirements.txt .\\

popd



