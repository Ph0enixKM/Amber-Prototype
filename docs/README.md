# About
A beautiful, programmer-friendly and modern looking programming language that is compiled to **BashScript**. It's designed to make it easier for developers to maintain scripts for  It can also be easily evaluated on the go.

> The docs are not completely ready yet! Come back soon to see how to install and use it

## Example usage
Here is a sample AmberScript code so that you can see how it looks like in action.

```amberscript
fun fibonacci(num) {
	box before = 0
	box actual = 1
	box next = 1
    box i = 0

    loop i < num {
        $ echo {next} $
        before = actual + next
        actual = next
		next = before
        i += 1
    }
}

$ echo {fibonacci(100)} $
```