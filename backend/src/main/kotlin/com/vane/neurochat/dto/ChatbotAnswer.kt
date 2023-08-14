package com.vane.neurochat.dto

import com.fasterxml.jackson.annotation.JsonProperty

data class ChatbotAnswer(
        @JsonProperty("MTS_chatbot")
        val text: String
)
