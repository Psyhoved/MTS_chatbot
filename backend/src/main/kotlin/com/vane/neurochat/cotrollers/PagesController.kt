package com.vane.neurochat.cotrollers

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.web.bind.annotation.GetMapping

@Controller
class PagesController {

    val log: Logger = LoggerFactory.getLogger(this::class.java)

    @GetMapping("/")
    fun getMainPage(model: Model): String {
        log.info("Somebody loaded page")
        return "index"
    }
}
