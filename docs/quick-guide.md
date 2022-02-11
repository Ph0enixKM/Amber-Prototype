# Quick Guide
If you have experience in other languages - I think this guide will be sufficient
for you as some form of cheat sheet on top of which you can play around with this language.

## Variables and values
Variables are mutable, dynamically typed and lifetime-limited to scopes.
AmberScript handles 4 value types (`Text`, `Number`, `Boolean`, `Array`)

```amberscript
let name = 'John'
let age = 20
let isAlive = true
let fruits = ['apple', 'orange', 'banana']

age += 12
fruits += ['kiwi']
isAlive = (age < 100 and age > 0) or name != 'dead'
```

## Command
Commands are basically embedded BashScript commands. They evaluate to `Text` type and return standard output. It is possible to add certain flags (`error` which returns standard error, `silent` which supresses any standard or error output and can only be used as a statement). There is also keyword for retrieving exit code of latest command and it's name is `status`.

```amberscript
# Receive stdout
let files = $ ls $
# Receive stderr
let err = error $ this_should_fail $
# Download website silently
silent $ curl http://example.com $
# Get the exit code
let code = status

# This will FAIL as silent can only be used as statement 
let mywebsite = silent $ curl http://example.com $
```

## If statement
If statements are very simple. Just like in c-like languages, it is possible to create 
blocks containing multiple statements and single-statement ones.

```amberscript
# Multiline blocks
if age >= 18 {
    $ echo Welcome $
} else {
    $ echo Nope $
}

# Singleline blocks
if 'something' == name
    let value = 12
```

## Text and Command interpolations
This is how we interpolate strings and variables into commands in AmberScript.

```amberscript
let name = 'Pablo'
let message = 'My name is {name}'
$ echo {message}! $

# Nested interpolations
'This {'is a {'fun'} thing'} to do'
```

## Loops
There are 3 types of loops in AmberScript. The simplest one is an infinite loop, another one is a "while" loop and third one the "for in" loop.

```amberscript
loop {
    $ echo Over and over... $
}

loop age < 100 {
    $ echo Living in progress...$
}

loop fruit in fruits {
    $ echo Buy {fruit}! $
}
```

## Functions
Creating and calling functions. Functions can take any amount of parameters. They are immutable and can return string value throught the standard output (just like in bash) and can return exit code (using `return` keyword)

```amberscript
fun fooBaz(n) {
    let index = 1
    loop index <= n {
        if index % 3 == 0
            $ echo "Foo!" $
        if index % 5 == 0
            $ echo "Baz!" $
        if index % 15 == 0
            $ echo "Foo Baz!" $
        index += 1
    }
}

fooBaz(20)
```