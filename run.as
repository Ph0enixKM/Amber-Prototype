fun build() {
    # Build the project
    sh cd('src')
    let err = sh python3('setup.py', 'build')

    # If error - stop
    if status != 0 {
        sh echo(err)
        sh exit()
    }

    # Package the build
    sh cd('../build')
    sh rm('amberscript.zip')
    $ zip -r -q ../amberscript.zip ./ $
}

# Workaround of saving first attribute
let attr = $ echo \$1 $

if attr == 'build'
    build()
else
    $ python3 src/main.py \$@ $
