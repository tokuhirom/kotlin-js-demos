package org.example

import react.Fragment
import react.create
import react.dom.client.createRoot
import react.dom.html.ReactHTML.h1
import web.dom.document

fun main() {
    val container = document.getElementById("root") ?: error("Couldn't find root container!")
    createRoot(container).render(Fragment.create {
        h1 {
            +"Hello, React+Kotlin/JS!"
        }
    })
}
