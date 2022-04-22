# Getting Started
## Instalation
### MacOS
Make sure that your operating system satisfies the follorwing prerequsites
- Bash or Zsh or any other Bourne-again shell *(usually comes with MacOS)*
- Ruby 2.0 or newer *(usually comes with MacOS)*
```bash
$(ruby -e "require 'open-uri'; puts open('https://raw.githubusercontent.com/Ph0enixKM/Amber/master/install.sh').read")
```

### Linux
Make sure that your operating system satisfies the follorwing prerequsites
- Bash or Zsh or any other Bourne-again shell
- Curl tool for downloading the installation script
```bash
curl https://raw.githubusercontent.com/Ph0enixKM/Amber/master/install.sh | bash
```

## Syntax Highlighting
You can install syntax highlighting for Visual Studio Code. You can find it in Visual Studio Code extension store under the name `Amber Language`.

Or you can download it here in [the Visual Studio Marketplace website](https://marketplace.visualstudio.com/items?itemName=Ph0enixKM.amber-language).


## Hello World Example
One of the first things that programmers do when learning a new programming language is infamous "hello world" program. Here we are using function call to display text *Hello World!*.

```amber
print('Hello World!')
```