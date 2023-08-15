package com.vane.neurochat.cotrollers

import com.vane.neurochat.dto.ChatbotAnswer
import jakarta.annotation.PostConstruct
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.http.HttpEntity
import org.springframework.http.HttpHeaders
import org.springframework.http.HttpMethod
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.client.RestTemplate

private const val defaultBotResponse = "Не получилось сформировать ответ"

@RestController
class ChatController(
        @Value("\${app.baseUrl}") private val baseUrl: String,
        private val restTemplate: RestTemplate
) {

    val log: Logger = LoggerFactory.getLogger(this::class.java)

    @PostConstruct
    fun postConstruct() {
        log.info("Base url = $baseUrl")
    }

    @PostMapping("chat/getBotNextMessage")
    fun handleChatMessage(@RequestBody message: String): ChatbotAnswer {
        log.info("Somebody wants bot response for: $message")

        return getBotResponse(message)
    }

    fun getBotResponse(prompt: String): ChatbotAnswer {
        return try {
            val url = "$baseUrl/generate_bot_response"
            val headers = HttpHeaders()
            headers.set("accept", "application/json")
            val entity = HttpEntity(
                    object {
                        val prompt = prompt
                    },
                    headers)
            val response = restTemplate.exchange(url, HttpMethod.POST, entity, ChatbotAnswer::class.java)
            log.info("Got response: ${response.body}")

            response.body ?: ChatbotAnswer(defaultBotResponse)
        } catch (e: Exception) {
            log.error("Got error on promt: $prompt", e)
            ChatbotAnswer(defaultBotResponse)
        }
    }
}
