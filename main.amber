# Variable definition
let myVar = 20
# Arithmetics (with float support)
let calc = myVar / 8
# Arrays and Texts
let myFruits = ['apple', 'orange', 'banana']
# if statements
if calc > 2 {
    # Assignment to 
    # existing variable
    myVar = false
}
# Single line else block
else
    myVar = true
# endless loop
loop {
    calc += 1
    if calc > 15
        break
}
# array loop
loop fruit in myFruits {
    # Embedded Bash and 
    # interpolated fruit variable
    $ echo {fruit} $
}
# While loop
loop calc < 30 {
    calc += 1
}
# Functions
fun print(text) {
    $ echo {text} $
}
print('Hello World')
# Show exit code of latest command
print(status)
# Run Embedded Bash code silently (statement)
silent $ very_annoying_command $
# Save standard output to variable
let std = $ ls -a $
# Save standard error to variable
let err = error $ this_will_error $

