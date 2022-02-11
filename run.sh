function print {
local text=$1
 echo $text 
}
function toArray {
local iterable=$1
for index in $( seq 1 ${#iterable} )
do
local letter=$( printf '%s' "${iterable:index - 1:1}" )
if [ $([ _$letter != _"," ]; echo $?) != 0 ]; then
printf "%s" " "
continue
fi
printf "%s" ${letter[@]}
done
}
function split {
local text=$1
local by=$2
if [ $([ _$by != _"" ]; echo $?) != 0 ]; then
for index in $( seq 1 ${#text} )
do
local letter=$( printf '%s' "${text:index - 1:1}" )
if [ $(bc -l <<< "$index != 1.0") != 0 ]; then
printf "%s" " "
fi
printf "%s" ${letter[@]}
done
return $(echo "0.0/1" | bc)
fi
toArray $( printf '%s' ${text//${by}/,} )
}
function build {
cd "src"
local err=$(python3 "setup.py" "build")
if [ $(bc -l <<< "$? != 0.0") != 0 ]; then
echo ${err[@]}
exit 
fi
cd "../build"
 zip -r -q ../amberscript.zip ./ 
}
attr=$( echo $1 )
if [ $([ _$attr != _"build" ]; echo $?) != 0 ]; then
build 
else
 python3 src/main.py $@ 
fi