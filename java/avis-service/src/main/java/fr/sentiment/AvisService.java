package fr.sentiment;

import java.net.http.HttpClient;
import java.time.Duration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientResponseException;

@SpringBootApplication
@RestController
public class AvisService {
    private final RestClient api;

    public AvisService(
            @Value("${SENTIMENT_API_URL:http://127.0.0.1:8000}") String url,
            @Value("${SENTIMENT_API_KEY:}") String cle) {
        var transport = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(3)).build();
        var factory = new JdkClientHttpRequestFactory(transport);
        factory.setReadTimeout(Duration.ofSeconds(10));
        api = RestClient.builder().baseUrl(url).requestFactory(factory)
                .defaultHeader("X-API-Key", cle).build();
    }

    public static void main(String[] args) {
        SpringApplication.run(AvisService.class, args);
    }

    @PostMapping("/avis")
    public ResponseEntity<String> analyser(@RequestBody Avis avis) {
        try {
            return api.post().uri("/v1/predict")
                    .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                    .body(avis)
                    .retrieve().toEntity(String.class);
        } catch (RestClientResponseException erreur) {
            return ResponseEntity.status(erreur.getStatusCode())
                    .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                    .body(erreur.getResponseBodyAsString());
        } catch (ResourceAccessException erreur) {
            return ResponseEntity.status(503)
                    .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
                    .body("{\"erreur\":\"API de sentiment injoignable\"}");
        }
    }

    public record Avis(String text) {}
}
