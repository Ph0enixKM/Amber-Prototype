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
if [ $(bc -l <<< "$index != 1") != 0 ]; then
printf "%s" " "
fi
printf "%s" ${letter[@]}
done
return $(echo "0/1" | bc)
fi
toArray $( printf '%s' ${text//${by}/,} )
}
function downloadFile {
local url=$1
local target=$2
function downloadRuby {
local url=$1
local target=$2
local code="require \"open-uri\"; open(\"$target\", \"wb\") do |file|; file << open(\"$url\").read; end"
 ruby -e "$code" 
}
function downloadCurl {
local url=$1
local target=$2
 curl -o "$target" "$url"  > /dev/null 2>&1
}
function downloadWget {
local url=$1
local target=$2
 wget -O "$target" "$url" 
}
 wget -v  > /dev/null 2>&1
local wgetStatus=$?
 ruby -v  > /dev/null 2>&1
local rubyStatus=$?
 curl -v  > /dev/null 2>&1
local curlStatus=$?
if [ $(bc -l <<< "$rubyStatus == 0") != 0 ]; then
downloadRuby ${url[@]} ${target[@]}
else
if [ $(bc -l <<< "$curlStatus == 0") != 0 ]; then
downloadCurl ${url[@]} ${target[@]}
else
if [ $(bc -l <<< "$wgetStatus == 0") != 0 ]; then
downloadWget ${url[@]} ${target[@]}
fi
fi
fi
}
function int {
local number=$1
 echo -n ${number%.*}
}
tag="1.0.0"
place="/opt/amber"
url="https://github.com/Ph0enixKM/AmberScript/releases/download/$tag/amber.zip"
 mkdir /opt/amber  > /dev/null 2>&1
downloadFile ${url[@]} "$place/amber.zip"
unzip "$place/amber.zip"
rm "amber.zip"
 ln -s -T $place/main /bin/amber 