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

AmberScript provides a syntactic sugar for calling simple commands in a form of *shell function calls*.
This is alpha equivalent to just calling command as if it was defined somewhere in the code (but compiler has no ability how to check at compile time if that command exists).

```amberscript
$ echo hello $ == sh echo('hello')
```

Shell function call is just a syntax sugar and should be used where possible if given command does not require
complex arguments, pipes etc.

## If statement
If statements are very simple. Just like in c-like languages, it is possible to create 
blocks containing multiple statements and single-statement ones.

```amberscript
# Multiline blocks
if age >= 18 {
    sh echo('Welcome')
} else {
    sh echo('Nope')
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

## Ranges
Ranges exist to generate iterative sequences starting from one and then counting all the way up to the other. The range is inclusive - meaning it does count in provided bounds. Let's see range in action.

```amberscript
# Simple range
1 to 10

# You can also count down
let myRange = 15 to 10
print(myRange)
```


## Loops
There are 3 types of loops in AmberScript. The simplest one is an infinite loop, another one is a "while" loop and third one the "for in" loop.

```amberscript
# This loop will never stop
loop {
    sh echo('Over and over...')
}

# This will loop while a is smaller than hundred
loop age < 100 {
    sh echo('Living in progress...')
}

# This will tell you to buy each fruit in the list of fruits
loop fruit in fruits {
    sh echo('Buy {fruit}!')
}

# This will count down the rocket liftoff (please don't use this language to do that in production)
loop number in 10 to 1 {
    sh echo('Counting down {number}')
}
```

## Functions
Creating and calling functions. Functions can take any amount of parameters. They are immutable and can return string value throught the standard output (just like in bash) and can return exit code (using `return` keyword)

```amberscript
fun fooBaz(n) {
    let index = 1
    loop index <= n {
        if index % 3 == 0 sh echo('Foo!')
        if index % 5 == 0 sh echo('Baz!')
        if index % 15 == 0 sh echo('Foo Baz!')
        index += 1
    }
}

fooBaz(20)
```