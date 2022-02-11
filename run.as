let attr = ''
$attr=\$1 $
if attr == 'build' {
    sh cd('src')
    let err = sh python3('setup.py', 'build')
    if status != 0 {
        sh echo(err)
    }
    silent $ rm -rf ../build $
    sh mv('build', '../build')
}
else {
    $ python3 src/main.py \$@ $
}
