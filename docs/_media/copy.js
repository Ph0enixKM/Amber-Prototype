// If no plugins
if (!window.$docsify.plugins) {
    window.$docsify.plugins = []
}

window.$docsify.plugins.push((hook, vm) => {
    hook.doneEach(() => {
        const codes = document.querySelectorAll('code')
        for (const code of codes) {
            // Create a copy button
            const el = document.createElement('img')
            el.src = '_media/copy.svg'
            el.className = 'copy-code'
            el.addEventListener('click', () => {
                // Support for mobile devices
                if (code.select) code.select()
                if (code.setSelectionRange) code.setSelectionRange(0, 9999)
                // Copy the actual text
                navigator.clipboard.writeText(code.innerText);
            })
            code.appendChild(el)
        }
    })
})
