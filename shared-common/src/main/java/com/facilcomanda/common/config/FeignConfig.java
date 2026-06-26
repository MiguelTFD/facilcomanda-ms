package com.facilcomanda.common.config;
import feign.RequestInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import java.util.List;
@Configuration
public class FeignConfig {
    private static final List<String> HEADERS = List.of("Authorization", "X-Correlation-ID", "X-Request-ID", "X-Trace-ID");
    @Bean RequestInterceptor headerForwardingInterceptor() {
        return template -> {
            if (RequestContextHolder.getRequestAttributes() instanceof ServletRequestAttributes attrs) {
                var request = attrs.getRequest();
                for (String header : HEADERS) {
                    String value = request.getHeader(header);
                    if (value != null) template.header(header, value);
                }
            }
        };
    }
}
