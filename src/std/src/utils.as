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

fun download(url, target) {
    fun downloadRuby(url, target) {
        let code = 'require "open-uri"; open("{target}", "wb") do |file|; file << open("{url}").read; end'
        $ ruby -e "{code}" $
    }

    fun downloadCurl(url, target) {
        silent $ curl -o "{target}" "{url}" $
    }

    fun downloadWget(url, target) {
        $ wget -O "{target}" "{url}" $
    }

    silent $ wget -v $
    let wgetStatus = status
    silent $ ruby -v $
    let rubyStatus = status
    silent $ curl -v $
    let curlStatus = status

    if rubyStatus == 0 downloadRuby(url, target)
    else if curlStatus == 0 downloadCurl(url, target)
    else if wgetStatus == 0 downloadWget(url, target)
}