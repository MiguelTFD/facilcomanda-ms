package com.facilcomanda.common.security;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.lang.NonNull;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;
import java.util.Collections;
@Component
public class AuthenticationFilter extends OncePerRequestFilter {
    private final JwtService jwtService;
    public AuthenticationFilter(JwtService jwtService) { this.jwtService = jwtService; }
    protected void doFilterInternal(@NonNull HttpServletRequest request, @NonNull HttpServletResponse response, @NonNull FilterChain chain) throws ServletException, IOException {
        String header = request.getHeader("Authorization");
        if (header == null || !header.startsWith("Bearer ")) { chain.doFilter(request, response); return; }
        String jwt = header.substring(7);
        try {
            String email = jwtService.extractUsername(jwt);
            if (email != null && SecurityContextHolder.getContext().getAuthentication() == null && jwtService.isTokenValid(jwt)) {
                Long organizationId = jwtService.extractOrganizationId(jwt);
                String role = jwtService.extractClaim(jwt, c -> c.get("role", String.class));
                CustomAuthentication auth = new CustomAuthentication(email, Collections.singletonList(new SimpleGrantedAuthority("ROLE_" + role.toUpperCase())), organizationId);
                auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(auth);
            }
        } catch (Exception ignored) { }
        chain.doFilter(request, response);
    }
}
