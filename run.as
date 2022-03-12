fun build() {
    # Build the project
    sh cd('src')
    let err = sh python3('setup.py', 'build')

    # If error - stop
    if status != 0 {
        sh echo(err)
        sh exit()
    }

    # Copy license and remove zip
    sh cd('..')
    silent $ rm amberscript.zip $
    sh cp('LICENSE', 'build/LICENSE')

    # Package the build
    sh cd('build')
    $ zip -r -q ../amberscript.zip ./ $
}

# Workaround of saving first attribute
let attr = $ echo \$1 $

if attr == 'build'
    build()
else
    $ python3 src/main.py \$@ $

if 12 > 5:
    print('TEST')