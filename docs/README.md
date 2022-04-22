# About
A beautiful, programmer-friendly and modern looking programming language that is compiled to **BashScript**. It's designed to make it easier for developers to maintain scripts for  It can also be easily evaluated on the go.

> The docs are not completely ready yet! Come back soon to see how to install and use it

## Example usage
Here is a sample Amber code so that you can see how it looks like in action.

```amber
fun fibonacci(num) {
	let before = 0
	let actual = 1
	let next = 1
    let i = 0

    loop i < num {
        sh echo(next)
        before = actual + next
        actual = next
		next = before
        i += 1
    }
}

$ echo {fibonacci(100)} $
```