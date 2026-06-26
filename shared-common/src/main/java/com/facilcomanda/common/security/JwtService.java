package com.facilcomanda.common.security;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;
@Service
public class JwtService {
    @Value("${application.security.jwt.secret-key}") private String secretKey;
    @Value("${application.security.jwt.expiration:86400000}") private long jwtExpiration;
    public String extractUsername(String token) { return extractClaim(token, Claims::getSubject); }
    public Long extractOrganizationId(String token) { return extractClaim(token, claims -> claims.get("organizationId", Long.class)); }
    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) { return claimsResolver.apply(extractAllClaims(token)); }
    public String generateToken(String email, Long organizationId, String roleName) {
        Map<String, Object> claims = new HashMap<>(); claims.put("organizationId", organizationId); claims.put("role", roleName); return buildToken(claims, email, jwtExpiration);
    }
    public boolean isTokenValid(String token) { try { return extractExpiration(token).after(new Date()); } catch (Exception e) { return false; } }
    private String buildToken(Map<String, Object> claims, String subject, long expiration) {
        return Jwts.builder().claims(claims).subject(subject).issuedAt(new Date()).expiration(new Date(System.currentTimeMillis() + expiration)).signWith(getSignInKey(), Jwts.SIG.HS256).compact();
    }
    private Date extractExpiration(String token) { return extractClaim(token, Claims::getExpiration); }
    private Claims extractAllClaims(String token) { return Jwts.parser().verifyWith(getSignInKey()).build().parseSignedClaims(token).getPayload(); }
    private SecretKey getSignInKey() { return Keys.hmacShaKeyFor(Decoders.BASE64.decode(secretKey)); }
}
