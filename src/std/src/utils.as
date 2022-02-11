fun toArray(iterable) {
    loop index in $ seq 1 \$\{#iterable} $ {
        let letter = $ printf '%s' "\$\{iterable:index - 1:1}" $
        if letter == ',' {
            sh printf('%s', ' ')
            continue
        }
        sh printf('%s', letter)
    }
}

fun split(text, by) {
    if by == '' {
        loop index in $ seq 1 \$\{#text} $ {
            let letter = $ printf '%s' "\$\{text:index - 1:1}" $
            if index != 1 {
                sh printf('%s', ' ')
            }
            sh printf('%s', letter)
        }
        return 0
    }
    toArray($ printf '%s' \$\{text//\$\{by}/,} $)
}