package com.vane.neurochat.cotrollers

import org.springframework.stereotype.Controller
import org.springframework.ui.Model
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestParam

@Controller
class FrameController {

    // Get the frame view
    @GetMapping("/frame")
    fun getFrameView(
            model: Model,
            @RequestParam("url", defaultValue = "http://www.mpoisk.ru/") url: String
    ): String {
        // Add the url parameter to the model
        model.addAttribute("url", url)
        // Return the view name
        return "index"
    }
}
