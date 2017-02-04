c:\Python34\python.exe gameMain.py
del visual\map.txt
xcopy map.txt visual\
cd visual\
c:\Python34\python.exe -m http.server 
cd ..\