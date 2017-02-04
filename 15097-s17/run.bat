c:\Python34\python.exe gameMain.py map2.json
del visual\map.txt
xcopy map.txt visual\
cd visual\
c:\Python34\python.exe -m http.server 
cd ..\