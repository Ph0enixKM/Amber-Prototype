let attr = ''
$attr=\$1$
if attr == 'build' {
    $ pyinstaller src/main.py --onefile --distpath ./build -n amber $
}
else {
    $ python3 src/main.py \$@ $
}