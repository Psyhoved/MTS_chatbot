package com.vane.neurochat.configs

import org.springframework.context.annotation.Configuration
import org.springframework.messaging.simp.config.MessageBrokerRegistry
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker
import org.springframework.web.socket.config.annotation.StompEndpointRegistry
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer

@Configuration
@EnableWebSocketMessageBroker
class WebSocketConfig : WebSocketMessageBrokerConfigurer {

    override fun configureMessageBroker(config: MessageBrokerRegistry) {
        // Enable a simple in-memory message broker to carry messages back to the client on destinations prefixed with "/topic"
        config.enableSimpleBroker("/topic")
        // Set the prefix for destinations targeting application annotated methods (via @MessageMapping)
        config.setApplicationDestinationPrefixes("/app")
    }

    override fun registerStompEndpoints(registry: StompEndpointRegistry) {
        // Register the "/chat" endpoint, enabling Spring's STOMP support and SockJS fallback options
        registry.addEndpoint("/chat").withSockJS()
    }
}
