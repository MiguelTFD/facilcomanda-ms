package com.facilcomanda.apigateway;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import java.util.UUID;
@Component
public class CorrelationGatewayFilter implements GlobalFilter, Ordered {
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String correlation = first(exchange, "X-Correlation-ID");
        String trace = first(exchange, "X-Trace-ID");
        ServerHttpRequest request = exchange.getRequest().mutate().header("X-Correlation-ID", correlation).header("X-Trace-ID", trace).build();
        exchange.getResponse().getHeaders().set("X-Correlation-ID", correlation);
        exchange.getResponse().getHeaders().set("X-Trace-ID", trace);
        return chain.filter(exchange.mutate().request(request).build());
    }
    private String first(ServerWebExchange exchange, String name) { String value = exchange.getRequest().getHeaders().getFirst(name); return value == null || value.isBlank() ? UUID.randomUUID().toString() : value; }
    public int getOrder() { return -100; }
}
