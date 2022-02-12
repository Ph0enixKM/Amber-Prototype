# Getting Started
## Instalation
### MacOS
Make sure that your operating system satisfies the follorwing prerequsites
- Bash or Zsh or any other Bourne-again shell *(usually comes with MacOS)*
- Ruby 2.0 or newer *(usually comes with MacOS)*
```bash
$(ruby -e "require 'open-uri'; puts open('https://raw.githubusercontent.com/Ph0enixKM/AmberScript/master/install.sh').read")
```

### Linux
Make sure that your operating system satisfies the follorwing prerequsites
- Bash or Zsh or any other Bourne-again shell
- Curl tool for downloading the installation script
```bash
curl https://raw.githubusercontent.com/Ph0enixKM/AmberScript/master/install.sh | bash
```

## Syntax Highlighting
You can install syntax highlighting for Visual Studio Code. You can find it in Visual Studio Code extension store under the name `AmberScript Language`.

Or you can download it here in [the Visual Studio Marketplace website](https://marketplace.visualstudio.com/items?itemName=Ph0enixKM.amberscript-language).


## Hello World Example
One of the first things that programmers do when learning a new programming language is infamous "hello world" program. Here we are using *shell function call* which is not checked by compiler at compiletime if such command exists. But we assume our shell does support `echo` command.

```amberscript
sh echo('Hello World!')
```