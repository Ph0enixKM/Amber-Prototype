# Getting Started
## Instalation
### MacOS
Make sure that your operating system satisfies the follorwing prerequsites
- Bash or Zsh or any other Bourne-again shell *(usually comes with MacOS)*
- Ruby 2.0 or newer *(usually comes with MacOS)*
- Python 3.9 or newer
```bash
$(ruby -e "require 'open-uri'; puts open('https://raw.githubusercontent.com/Ph0enixKM/AmberScript/master/install.sh').read")
```

### Linux
Make sure that your operating system satisfies the follorwing prerequsites
- Bash or Zsh or any other Bourne-again shell
- Curl tool for downloading the installation script
- Python 3.9 or newer
```bash
curl https://raw.githubusercontent.com/Ph0enixKM/AmberScript/master/install.sh | bash
```

## Syntax Highlighting
You can install syntax highlighting for Visual Studio Code. You can find it in Visual Studio Code extension store under the name `AmberScript Language`.

Or you can download it here in [the Visual Studio Marketplace website](https://marketplace.visualstudio.com/items?itemName=Ph0enixKM.amberscript-language).


## Hello World Example
One of the first things that programmers do when learning a new programming language is infamous "hello world" program.

> **Warning!**
> Since AmberScript does not have implemented any standard library yet - we will handle all the IO by embedding BashScript code.
> In the future you will be able to just call `print('Hello world!')`

```amberscript
$ echo Hello World! $
```