package com.vane.neurochat.cotrollers

import org.springframework.messaging.handler.annotation.MessageMapping
import org.springframework.messaging.handler.annotation.SendTo
import org.springframework.stereotype.Controller

@Controller
class ChatController {

    // Listen for the "chat message" event from the clients
    @MessageMapping("/chat")
    // Broadcast the message to all the connected clients on "/topic/messages" destination
    @SendTo("/topic/messages")
    fun handleChatMessage(message: String): String {
        // Return the message as it is
        return message
    }
}
