package com.example.mlb_predictions.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {
    @Bean
    public WebClient pythonClient() {
        return WebClient.builder()
            .baseUrl("http://python-ml-api:8000")  // <- Use Docker service name here
            .build();
    }
}