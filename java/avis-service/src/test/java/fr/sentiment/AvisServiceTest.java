package fr.sentiment;

import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class AvisServiceTest {
    @Test
    void transmetLaCleEtLeVerdict() throws Exception {
        var serveur = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        serveur.createContext("/v1/predict", requete -> {
            boolean valide = "cle-test".equals(requete.getRequestHeaders().getFirst("X-API-Key"))
                    && "POST".equals(requete.getRequestMethod())
                    && new String(requete.getRequestBody().readAllBytes(), StandardCharsets.UTF_8)
                            .contains("Très satisfait");
            byte[] corps = "{\"label\":\"POSITIVE\",\"score\":0.78}"
                    .getBytes(StandardCharsets.UTF_8);
            requete.getResponseHeaders().set("Content-Type", "application/json");
            requete.sendResponseHeaders(valide ? 200 : 401, corps.length);
            try (var sortie = requete.getResponseBody()) {
                sortie.write(corps);
            }
        });
        serveur.start();
        try {
            var service = new AvisService("http://127.0.0.1:" + serveur.getAddress().getPort(), "cle-test");
            var resultat = service.analyser(new AvisService.Avis("Très satisfait"));
            assertEquals(200, resultat.getStatusCode().value());
            assertEquals("{\"label\":\"POSITIVE\",\"score\":0.78}", resultat.getBody());
        } finally {
            serveur.stop(0);
        }
    }
}
