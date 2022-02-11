name="John"
age=20.0
isAlive=1
fruits=("apple" "orange" "banana")
age=$(bc -l <<< "$age + 12.0")
fruits=(${fruits[@]} "kiwi")
isAlive=$(bc -l <<< "($(bc -l <<< "$(bc -l <<< "$age < 100.0") && $(bc -l <<< "$age > 0.0")")) || $([ _$name = _"dead" ]; echo $?)")
echo ${isAlive[@]}