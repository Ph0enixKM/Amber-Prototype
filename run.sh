attr=""
attr=$1
if [ $([ _$attr != _"build" ]; echo $?) != 0 ]; then
 pyinstaller src/main.py --onefile --distpath ./build -n amber 
else
 python3 src/main.py $@ 
fi