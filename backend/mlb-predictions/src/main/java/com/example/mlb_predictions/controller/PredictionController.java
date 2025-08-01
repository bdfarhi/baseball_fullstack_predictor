// package com.example.mlb_predictions.controller;

// import com.example.mlb_predictions.dto.Prediction;
// import com.example.mlb_predictions.service.PredictionService;
// import org.springframework.web.bind.annotation.GetMapping;
// import org.springframework.web.bind.annotation.RequestMapping;
// import org.springframework.web.bind.annotation.RestController;
// import reactor.core.publisher.Flux;

// @RestController
// @RequestMapping("/api/predictions")
// public class PredictionController {

//     private final PredictionService service;

//     public PredictionController(PredictionService service) {
//         this.service = service;
//     }

//     /**
//      * GET /api/predictions/today
//      */
//     @GetMapping("/today")
//     public Flux<Prediction> today() {
//         return service.fetchTodayPredictions();
//     }
// }
package com.example.mlb_predictions.controller;

import com.example.mlb_predictions.model.MatchupRequest;
import com.example.mlb_predictions.model.MatchupResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


@RestController
@CrossOrigin(origins = "http://localhost:3000")
@RequestMapping("/api")
public class PredictionController {

    private static final Logger logger = LoggerFactory.getLogger(PredictionController.class);

    @Autowired
    private RestTemplate restTemplate;

    @PostMapping("/predict")
    public ResponseEntity<MatchupResponse> predictWinner(@RequestBody MatchupRequest request) {
        logger.info("Received prediction request: team1={}, team2={}", request.getTeam1(), request.getTeam2());

        String fastApiUrl = "http://python-ml-api:8000/predict";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<MatchupRequest> entity = new HttpEntity<>(request, headers);

        try {
            ResponseEntity<MatchupResponse> response = restTemplate.exchange(
                    fastApiUrl,
                    HttpMethod.POST,
                    entity,
                    MatchupResponse.class
            );

            logger.info("FastAPI response: {}", response.getBody().getWinner());
            return ResponseEntity.ok(response.getBody());
        } catch (Exception e) {
            logger.error("Error calling FastAPI service: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}