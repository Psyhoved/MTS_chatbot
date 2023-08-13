package com.vane.neurochat

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class NeurochatApplication

fun main(args: Array<String>) {
	runApplication<NeurochatApplication>(*args)
}
