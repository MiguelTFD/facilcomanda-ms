package com.facilcomanda.common.web;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;
import java.util.UUID;
@Component
public class CorrelationIdFilter extends OncePerRequestFilter {
    public static final String CORRELATION_ID = "X-Correlation-ID";
    public static final String TRACE_ID = "X-Trace-ID";
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain) throws ServletException, IOException {
        String correlationId = headerOrNew(request, CORRELATION_ID);
        String traceId = headerOrNew(request, TRACE_ID);
        MDC.put("correlationId", correlationId); MDC.put("traceId", traceId);
        response.setHeader(CORRELATION_ID, correlationId); response.setHeader(TRACE_ID, traceId);
        try { chain.doFilter(request, response); } finally { MDC.remove("correlationId"); MDC.remove("traceId"); }
    }
    private String headerOrNew(HttpServletRequest req, String name) { String v = req.getHeader(name); return (v == null || v.isBlank()) ? UUID.randomUUID().toString() : v; }
}
