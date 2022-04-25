# Uninstalling Amber
If you feel like you no longer need Amber on your system or you want to reinstall it - you can use provided uninstallation scripts.
### MacOS
```bash
sudo ruby -e "require 'open-uri'; puts open('https://raw.githubusercontent.com/Ph0enixKM/Amber/master/uninstall.sh').read" | $(echo $SHELL)
```

### Linux
```bash
sudo curl https://raw.githubusercontent.com/Ph0enixKM/Amber/master/uninstall.sh | $(echo $SHELL)
```
