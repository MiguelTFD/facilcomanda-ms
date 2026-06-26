from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
GROUP = "com.facilcomanda"
BOOT = "3.2.5"
CLOUD = "2023.0.1"

def w(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")

def java_base(module):
    compact = module.replace("-", "")
    return Path(module) / "src/main/java/com/facilcomanda" / compact

def res_base(module):
    return Path(module) / "src/main/resources"

modules = [
    "discovery-server", "config-server", "api-gateway", "shared-common",
    "auth-service", "audit-service", "user-service", "category-service",
    "product-service", "restaurant-service", "table-service", "order-service",
]

w("pom.xml", f"""
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>{GROUP}</groupId>
    <artifactId>facilcomanda-microservices</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>pom</packaging>
    <name>facilcomanda-microservices</name>

    <modules>
{''.join(f'        <module>{m}</module>\n' for m in modules)}
    </modules>

    <properties>
        <java.version>17</java.version>
        <spring-boot.version>{BOOT}</spring-boot.version>
        <spring-cloud.version>{CLOUD}</spring-cloud.version>
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${{spring-boot.version}}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${{spring-cloud.version}}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                    <version>${{spring-boot.version}}</version>
                    <executions>
                        <execution>
                            <goals>
                                <goal>repackage</goal>
                            </goals>
                        </execution>
                    </executions>
                </plugin>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.11.0</version>
                    <configuration>
                        <release>${{maven.compiler.release}}</release>
                    </configuration>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
""")

def service_pom(module, artifact_deps="", gateway=False, discovery=False, config=False, common=True, jpa=True, web=True, security=True, feign=True, amqp=True):
    deps = []
    if common:
        deps.append(f"""
        <dependency>
            <groupId>{GROUP}</groupId>
            <artifactId>shared-common</artifactId>
            <version>${{project.version}}</version>
        </dependency>""")
    if web:
        deps.append("""
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>""")
    if security:
        deps.append("""
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>""")
    if jpa:
        deps.append("""
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>""")
    if feign:
        deps.append("""
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>""")
    if amqp:
        deps.append("""
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-amqp</artifactId>
        </dependency>""")
    deps.append("""
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>2.5.0</version>
        </dependency>
        <dependency>
            <groupId>io.github.resilience4j</groupId>
            <artifactId>resilience4j-spring-boot3</artifactId>
            <version>2.2.0</version>
        </dependency>""")
    deps.append(artifact_deps)
    w(f"{module}/pom.xml", f"""
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <parent>
            <groupId>{GROUP}</groupId>
            <artifactId>facilcomanda-microservices</artifactId>
            <version>0.0.1-SNAPSHOT</version>
        </parent>
        <artifactId>{module}</artifactId>
        <dependencies>{''.join(deps)}
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-test</artifactId>
                <scope>test</scope>
            </dependency>
        </dependencies>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                </plugin>
            </plugins>
        </build>
    </project>
    """)

w("shared-common/pom.xml", f"""
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>{GROUP}</groupId>
        <artifactId>facilcomanda-microservices</artifactId>
        <version>0.0.1-SNAPSHOT</version>
    </parent>
    <artifactId>shared-common</artifactId>
    <dependencies>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-web</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-security</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-amqp</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-validation</artifactId></dependency>
        <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-openfeign</artifactId></dependency>
        <dependency><groupId>io.jsonwebtoken</groupId><artifactId>jjwt-api</artifactId><version>0.12.5</version></dependency>
        <dependency><groupId>io.jsonwebtoken</groupId><artifactId>jjwt-impl</artifactId><version>0.12.5</version><scope>runtime</scope></dependency>
        <dependency><groupId>io.jsonwebtoken</groupId><artifactId>jjwt-jackson</artifactId><version>0.12.5</version><scope>runtime</scope></dependency>
    </dependencies>
</project>
""")

for module in ["auth-service", "audit-service", "user-service", "category-service", "product-service", "restaurant-service", "table-service", "order-service"]:
    service_pom(module)

service_pom("discovery-server", common=False, jpa=False, web=False, security=False, feign=False, amqp=False, artifact_deps="""
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>""")

service_pom("config-server", common=False, jpa=False, web=False, security=False, feign=False, amqp=False, artifact_deps="""
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
        </dependency>""")

w("api-gateway/pom.xml", f"""
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>{GROUP}</groupId>
        <artifactId>facilcomanda-microservices</artifactId>
        <version>0.0.1-SNAPSHOT</version>
    </parent>
    <artifactId>api-gateway</artifactId>
    <dependencies>
        <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-gateway</artifactId></dependency>
        <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-netflix-eureka-client</artifactId></dependency>
        <dependency><groupId>org.springframework.cloud</groupId><artifactId>spring-cloud-starter-config</artifactId></dependency>
        <dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-actuator</artifactId></dependency>
    </dependencies>
    <build><plugins><plugin><groupId>org.springframework.boot</groupId><artifactId>spring-boot-maven-plugin</artifactId></plugin></plugins></build>
</project>
""")

common = Path("shared-common/src/main/java/com/facilcomanda/common")
w(common/"enums/RoleName.java", """
package com.facilcomanda.common.enums;
public enum RoleName {
    MESERO, CAJERO, COCINERO, ADMIN, SUPERADMIN, WEB_OWNER, ORG_MASTER, WAITER, SENIOR_WAITER
}
""")
w(common/"enums/OrderStatus.java", """
package com.facilcomanda.common.enums;
public enum OrderStatus { PENDING, PREPARING, READY, DELIVERED, PAID, CANCELLED }
""")
w(common/"enums/TableState.java", """
package com.facilcomanda.common.enums;
public enum TableState { AVAILABLE, OCCUPIED, IDLE }
""")

dtos = {
"CategoryRequest.java": "import jakarta.validation.constraints.NotBlank; public record CategoryRequest(@NotBlank String name, String description, Long parentCategoryId) {}",
"CategoryResponse.java": "public record CategoryResponse(Long id, String name, String description, Long parentCategoryId) {}",
"LoginRequest.java": "import jakarta.validation.constraints.NotBlank; public record LoginRequest(@NotBlank String email, @NotBlank String password) {}",
"LoginResponse.java": "public record LoginResponse(String token, UserAuthDTO user) {}",
"OrderItemRequest.java": "import jakarta.validation.constraints.Min; import jakarta.validation.constraints.NotNull; public record OrderItemRequest(@NotNull Long productId, @NotNull @Min(1) Integer quantity, String comments) {}",
"OrderItemResponse.java": "import java.math.BigDecimal; public record OrderItemResponse(Long id, Long productId, String productName, Integer quantity, BigDecimal subtotal, String comments) {}",
"OrderRequest.java": "import jakarta.validation.constraints.NotBlank; import jakarta.validation.constraints.NotEmpty; import java.util.List; public record OrderRequest(Long restaurantTableId, @NotBlank String type, @NotBlank String idempotencyKey, @NotEmpty List<OrderItemRequest> items) {}",
"OrderResponse.java": "import com.facilcomanda.common.enums.OrderStatus; import java.math.BigDecimal; import java.time.LocalDateTime; import java.util.List; public record OrderResponse(Long id, Long restaurantTableId, String tableName, String floorName, String type, OrderStatus status, BigDecimal total, LocalDateTime orderDate, List<OrderItemResponse> items) {}",
"OrderStatusRequest.java": "import com.facilcomanda.common.enums.OrderStatus; import jakarta.validation.constraints.NotNull; public record OrderStatusRequest(@NotNull OrderStatus status) {}",
"OrganizationRequest.java": "import jakarta.validation.constraints.NotBlank; public record OrganizationRequest(@NotBlank String name, String taxIdentificationNumber, String taxIdentificationType) {}",
"OrganizationResponse.java": "public record OrganizationResponse(Long id, String name, String taxIdentificationNumber, String taxIdentificationType) {}",
"ProductRequest.java": "import jakarta.validation.constraints.NotBlank; import jakarta.validation.constraints.NotNull; import java.math.BigDecimal; import java.time.LocalDateTime; import java.util.Set; public record ProductRequest(@NotBlank String name, String description, @NotNull Integer stock, @NotNull BigDecimal unitPrice, BigDecimal discount, LocalDateTime expirationDate, Set<Long> categoryIds) {}",
"ProductResponse.java": "import java.math.BigDecimal; import java.time.LocalDateTime; import java.util.List; public record ProductResponse(Long id, String name, String description, Integer stock, BigDecimal unitPrice, BigDecimal discount, LocalDateTime expirationDate, List<Long> categoryIds, List<String> categoryNames) {}",
"RegisterRequest.java": "import jakarta.validation.constraints.Email; import jakarta.validation.constraints.NotBlank; import jakarta.validation.constraints.NotNull; import jakarta.validation.constraints.Size; public record RegisterRequest(@NotBlank @Email String email, @NotBlank @Size(min = 6) String password, @NotBlank String firstName, @NotBlank String lastName, @NotNull Long roleId, @NotNull Long organizationId) {}",
"RestaurantFloorRequest.java": "import jakarta.validation.constraints.NotBlank; public record RestaurantFloorRequest(@NotBlank String name, String description) {}",
"RestaurantFloorResponse.java": "public record RestaurantFloorResponse(Long id, String name, String description, Long organizationId) {}",
"RoleRequest.java": "import jakarta.validation.constraints.NotBlank; public record RoleRequest(@NotBlank String name, String description) {}",
"RoleResponse.java": "public record RoleResponse(Long id, String name, String description, Long organizationId) {}",
"TableRequest.java": "import com.facilcomanda.common.enums.TableState; import jakarta.validation.constraints.NotBlank; import jakarta.validation.constraints.NotNull; public record TableRequest(@NotBlank String name, String description, @NotNull TableState state, @NotNull Integer chairs, @NotNull Long floorId) {}",
"TableResponse.java": "import com.facilcomanda.common.enums.TableState; public record TableResponse(Long id, String name, String description, TableState state, Integer chairs, Long organizationId, Long floorId, String floorName) {}",
"UserAuthDTO.java": "import com.facilcomanda.common.enums.RoleName; public record UserAuthDTO(Long id, String email, String firstName, String lastName, RoleName roleName, Long organizationId) {}",
"UserRequest.java": "import jakarta.validation.constraints.Email; import jakarta.validation.constraints.NotBlank; import jakarta.validation.constraints.NotNull; public record UserRequest(@NotBlank @Email String email, String password, @NotBlank String firstName, @NotBlank String lastName, @NotNull Long roleId) {}",
"UserResponse.java": "public record UserResponse(Long id, String email, String firstName, String lastName, String roleName, Long organizationId) {}",
"ProductSnapshot.java": "import java.math.BigDecimal; public record ProductSnapshot(Long id, String name, BigDecimal unitPrice, BigDecimal discount, Integer stock) {}",
"UserSnapshot.java": "public record UserSnapshot(Long id, String email, String firstName, String lastName, String roleName, Long organizationId) {}",
}
for name, body in dtos.items():
    w(common/f"dto/{name}", "package com.facilcomanda.common.dto;\n" + body)

w(common/"event/AuditEvent.java", """
package com.facilcomanda.common.event;
import java.time.Instant;
public record AuditEvent(String serviceName, String entityName, String entityId, String operation, String oldValues,
                         String newValues, String performedBy, String requestIp, String correlationId,
                         String traceId, Instant createdAt) {}
""")
w(common/"event/DomainEvent.java", """
package com.facilcomanda.common.event;
import java.time.Instant;
public record DomainEvent(String serviceName, String entityName, String entityId, String eventType, Object payload,
                          String correlationId, String traceId, Instant createdAt) {}
""")
w(common/"event/EventPublisher.java", """
package com.facilcomanda.common.event;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;
import java.time.Instant;
@Component
public class EventPublisher {
    public static final String DOMAIN_EXCHANGE = "domain.events.exchange";
    public static final String AUDIT_EXCHANGE = "audit.events.exchange";
    private final RabbitTemplate rabbitTemplate;
    public EventPublisher(RabbitTemplate rabbitTemplate) { this.rabbitTemplate = rabbitTemplate; }
    public void publishDomain(String routingKey, DomainEvent event) { rabbitTemplate.convertAndSend(DOMAIN_EXCHANGE, routingKey, event); }
    public void publishAudit(AuditEvent event) { rabbitTemplate.convertAndSend(AUDIT_EXCHANGE, "audit.created", event); }
    public void publishAudit(String service, String entity, Object id, String operation, Object oldValues, Object newValues, String actor, String ip, String correlationId, String traceId) {
        publishAudit(new AuditEvent(service, entity, id == null ? null : String.valueOf(id), operation, String.valueOf(oldValues), String.valueOf(newValues), actor, ip, correlationId, traceId, Instant.now()));
    }
}
""")
w(common/"config/RabbitMqConfig.java", """
package com.facilcomanda.common.config;
import com.facilcomanda.common.event.EventPublisher;
import org.springframework.amqp.core.*;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
@Configuration
public class RabbitMqConfig {
    @Bean TopicExchange domainExchange() { return ExchangeBuilder.topicExchange(EventPublisher.DOMAIN_EXCHANGE).durable(true).build(); }
    @Bean TopicExchange auditExchange() { return ExchangeBuilder.topicExchange(EventPublisher.AUDIT_EXCHANGE).durable(true).build(); }
    @Bean Queue auditQueue() { return QueueBuilder.durable("audit.queue").withArgument("x-dead-letter-exchange", "audit.events.dlx").build(); }
    @Bean TopicExchange auditDlx() { return ExchangeBuilder.topicExchange("audit.events.dlx").durable(true).build(); }
    @Bean Binding auditBinding(Queue auditQueue, TopicExchange auditExchange) { return BindingBuilder.bind(auditQueue).to(auditExchange).with("audit.created"); }
    @Bean MessageConverter jsonMessageConverter() { return new Jackson2JsonMessageConverter(); }
}
""")
w(common/"security/CustomAuthentication.java", """
package com.facilcomanda.common.security;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import java.util.Collection;
public class CustomAuthentication implements Authentication {
    private final String email; private final Collection<? extends GrantedAuthority> authorities; private final Long organizationId;
    private Object details; private boolean authenticated = true;
    public CustomAuthentication(String email, Collection<? extends GrantedAuthority> authorities, Long organizationId) { this.email = email; this.authorities = authorities; this.organizationId = organizationId; }
    public Collection<? extends GrantedAuthority> getAuthorities() { return authorities; }
    public Object getCredentials() { return null; }
    public Object getDetails() { return details; }
    public void setDetails(Object details) { this.details = details; }
    public Object getPrincipal() { return email; }
    public boolean isAuthenticated() { return authenticated; }
    public void setAuthenticated(boolean authenticated) throws IllegalArgumentException { this.authenticated = authenticated; }
    public String getName() { return email; }
    public Long getOrganizationId() { return organizationId; }
}
""")
w(common/"security/JwtService.java", """
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
""")
w(common/"security/AuthenticationFilter.java", """
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
""")
w(common/"security/SecurityConfig.java", """
package com.facilcomanda.common.security;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    private final AuthenticationFilter authenticationFilter;
    public SecurityConfig(AuthenticationFilter authenticationFilter) { this.authenticationFilter = authenticationFilter; }
    @Bean SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.csrf(csrf -> csrf.disable()).cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth.requestMatchers("/api/auth/**", "/internal/**", "/actuator/**", "/v3/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll().requestMatchers("/api/**").authenticated().anyRequest().permitAll())
            .exceptionHandling(e -> e.authenticationEntryPoint((req, res, ex) -> res.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Unauthorized")))
            .addFilterBefore(authenticationFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
    @Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }
    @Bean UrlBasedCorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration c = new CorsConfiguration(); c.addAllowedOriginPattern("*"); c.addAllowedMethod("*"); c.addAllowedHeader("*"); c.setAllowCredentials(false);
        UrlBasedCorsConfigurationSource s = new UrlBasedCorsConfigurationSource(); s.registerCorsConfiguration("/**", c); return s;
    }
}
""")
w(common/"web/CorrelationIdFilter.java", """
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
""")
w(common/"web/AuthContext.java", """
package com.facilcomanda.common.web;
import com.facilcomanda.common.security.CustomAuthentication;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
public final class AuthContext {
    private AuthContext() {}
    public static Long organizationId(Authentication authentication) {
        if (authentication instanceof CustomAuthentication custom) return custom.getOrganizationId();
        throw new RuntimeException("Authentication is invalid or missing organization ID context");
    }
    public static boolean hasRole(Authentication authentication, String roleName) {
        return authentication.getAuthorities().stream().map(GrantedAuthority::getAuthority).anyMatch(r -> r.equals(roleName) || r.equals("ROLE_" + roleName));
    }
}
""")
w(common/"exception/GlobalExceptionHandler.java", """
package com.facilcomanda.common.exception;
import jakarta.validation.ConstraintViolationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.OptimisticLockingFailureException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.TransactionSystemException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
@RestControllerAdvice
public class GlobalExceptionHandler {
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    @ExceptionHandler(TransactionSystemException.class)
    public ResponseEntity<Map<String, String>> handleTransactionSystemException(TransactionSystemException ex) {
        Throwable cause = ex.getRootCause(); String message = "Could not commit JPA transaction";
        if (cause instanceof ConstraintViolationException c) message = c.getConstraintViolations().stream().map(v -> v.getPropertyPath() + ": " + v.getMessage()).collect(Collectors.joining(", "));
        else if (cause != null) message = cause.getMessage();
        logger.error("Transaction Error: {}", message, ex); return error(message, HttpStatus.BAD_REQUEST);
    }
    @ExceptionHandler(DataIntegrityViolationException.class)
    public ResponseEntity<Map<String, String>> handleDataIntegrityViolationException(DataIntegrityViolationException ex) {
        String msg = ex.getRootCause() != null ? ex.getRootCause().getMessage() : ex.getMessage(); logger.error("Data Integrity Violation: {}", msg, ex); return error("Database constraint error: " + msg, HttpStatus.CONFLICT);
    }
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationException(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult().getFieldErrors().stream().map(e -> e.getField() + ": " + e.getDefaultMessage()).collect(Collectors.toList());
        Map<String, Object> response = new HashMap<>(); response.put("message", "Validation failed"); response.put("errors", errors); return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }
    @ExceptionHandler(OptimisticLockingFailureException.class)
    public ResponseEntity<Map<String, String>> handleOptimisticLockingFailureException(OptimisticLockingFailureException ex) { return error("The resource has been modified by another user. Please try again.", HttpStatus.CONFLICT); }
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, String>> handleRuntimeException(RuntimeException ex) { logger.error("Runtime Exception: {}", ex.getMessage(), ex); return error(ex.getMessage(), HttpStatus.BAD_REQUEST); }
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, String>> handleGeneralException(Exception ex) { logger.error("Unhandled Exception: ", ex); return error("An unexpected error occurred: " + ex.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR); }
    private ResponseEntity<Map<String, String>> error(String message, HttpStatus status) { Map<String, String> response = new HashMap<>(); response.put("message", message); return new ResponseEntity<>(response, status); }
}
""")
w(common/"config/FeignConfig.java", """
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
""")

# Infrastructure applications
w("discovery-server/src/main/java/com/facilcomanda/discoveryserver/DiscoveryServerApplication.java", """
package com.facilcomanda.discoveryserver;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;
@EnableEurekaServer
@SpringBootApplication
public class DiscoveryServerApplication { public static void main(String[] args) { SpringApplication.run(DiscoveryServerApplication.class, args); } }
""")
w("discovery-server/src/main/resources/application.yml", """
spring:
  application:
    name: discovery-server
server:
  port: ${PORT:8761}
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
management:
  endpoints:
    web:
      exposure:
        include: health,info
""")
w("config-server/src/main/java/com/facilcomanda/configserver/ConfigServerApplication.java", """
package com.facilcomanda.configserver;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;
@EnableConfigServer
@SpringBootApplication
public class ConfigServerApplication { public static void main(String[] args) { SpringApplication.run(ConfigServerApplication.class, args); } }
""")
w("config-server/src/main/resources/application.yml", """
spring:
  application:
    name: config-server
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/config
server:
  port: ${PORT:8888}
eureka:
  client:
    service-url:
      defaultZone: ${EUREKA_DEFAULT_ZONE:http://localhost:8761/eureka}
management:
  endpoints:
    web:
      exposure:
        include: health,info
""")
w("config-server/src/main/resources/config/application.yml", """
spring:
  datasource:
    url: ${DB_URL:jdbc:postgresql://localhost:5432/facilcomanda}
    username: ${DB_USER:postgres}
    password: ${DB_PASSWORD:postgres}
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: ${DB_DDL_AUTO:update}
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.PostgreSQLDialect
  rabbitmq:
    host: ${RABBITMQ_HOST:localhost}
    port: ${RABBITMQ_PORT:5672}
    username: ${RABBITMQ_USER:guest}
    password: ${RABBITMQ_PASSWORD:guest}
eureka:
  client:
    service-url:
      defaultZone: ${EUREKA_DEFAULT_ZONE:http://localhost:8761/eureka}
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
logging:
  pattern:
    level: "%5p [correlationId:%X{correlationId:-},traceId:%X{traceId:-}]"
application:
  security:
    jwt:
      secret-key: ${JWT_SECRET:404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970}
      expiration: ${JWT_EXPIRATION:86400000}
feign:
  client:
    config:
      default:
        connectTimeout: 3000
        readTimeout: 5000
""")
w("api-gateway/src/main/java/com/facilcomanda/apigateway/ApiGatewayApplication.java", """
package com.facilcomanda.apigateway;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class ApiGatewayApplication { public static void main(String[] args) { SpringApplication.run(ApiGatewayApplication.class, args); } }
""")
w("api-gateway/src/main/java/com/facilcomanda/apigateway/CorrelationGatewayFilter.java", """
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
""")
w("api-gateway/src/main/resources/application.yml", """
spring:
  application:
    name: api-gateway
  config:
    import: optional:configserver:${CONFIG_SERVER_URL:http://localhost:8888}
  cloud:
    gateway:
      default-filters:
        - DedupeResponseHeader=Access-Control-Allow-Credentials Access-Control-Allow-Origin
      globalcors:
        corsConfigurations:
          '[/**]':
            allowedOriginPatterns: "*"
            allowedMethods: "*"
            allowedHeaders: "*"
      routes:
        - id: auth-service
          uri: lb://auth-service
          predicates: [ Path=/api/auth/** ]
        - id: user-service
          uri: lb://user-service
          predicates: [ Path=/api/users/**,/api/roles/** ]
        - id: category-service
          uri: lb://category-service
          predicates: [ Path=/api/categories/** ]
        - id: product-service
          uri: lb://product-service
          predicates: [ Path=/api/products/** ]
        - id: restaurant-service
          uri: lb://restaurant-service
          predicates: [ Path=/api/organizations/**,/api/restaurant-floors/** ]
        - id: table-service
          uri: lb://table-service
          predicates: [ Path=/api/tables/** ]
        - id: order-service
          uri: lb://order-service
          predicates: [ Path=/api/orders/** ]
        - id: audit-service
          uri: lb://audit-service
          predicates: [ Path=/api/audit/** ]
server:
  port: ${PORT:8080}
eureka:
  client:
    service-url:
      defaultZone: ${EUREKA_DEFAULT_ZONE:http://localhost:8761/eureka}
management:
  endpoints:
    web:
      exposure:
        include: health,info
""")

def app(module, cls):
    compact = module.replace("-", "")
    w(java_base(module)/f"{cls}.java", f"""
    package com.facilcomanda.{compact};
    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    import org.springframework.cloud.openfeign.EnableFeignClients;
    @EnableFeignClients(basePackages = "com.facilcomanda")
    @SpringBootApplication(scanBasePackages = "com.facilcomanda")
    public class {cls} {{ public static void main(String[] args) {{ SpringApplication.run({cls}.class, args); }} }}
    """)
    w(res_base(module)/"application.yml", f"""
    spring:
      application:
        name: {module}
      config:
        import: optional:configserver:${{CONFIG_SERVER_URL:http://localhost:8888}}
    server:
      port: ${{PORT:{ports[module]}}}
    """)

ports = {"auth-service":8081,"user-service":8082,"category-service":8083,"product-service":8084,"restaurant-service":8085,"table-service":8086,"order-service":8087,"audit-service":8088}
for m, cls in {"auth-service":"AuthServiceApplication","user-service":"UserServiceApplication","category-service":"CategoryServiceApplication","product-service":"ProductServiceApplication","restaurant-service":"RestaurantServiceApplication","table-service":"TableServiceApplication","order-service":"OrderServiceApplication","audit-service":"AuditServiceApplication"}.items():
    app(m, cls)

# User service
ub = java_base("user-service")
w(ub/"entity/Role.java", """
package com.facilcomanda.userservice.entity;
import com.facilcomanda.common.enums.RoleName;
import jakarta.persistence.*;
@Entity @Table(name = "roles", indexes = @Index(name = "idx_role_org", columnList = "organization_id"))
public class Role {
 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
 @Column(name = "organization_id") private Long organizationId;
 @Enumerated(EnumType.STRING) private RoleName name;
 private String description;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;}
 public RoleName getName(){return name;} public void setName(RoleName name){this.name=name;} public String getDescription(){return description;} public void setDescription(String description){this.description=description;}
}
""")
w(ub/"entity/User.java", """
package com.facilcomanda.userservice.entity;
import jakarta.persistence.*;
@Entity @Table(name = "users", indexes = @Index(name = "idx_user_org", columnList = "organization_id"))
public class User {
 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
 @Column(name = "organization_id") private Long organizationId;
 @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "role_id") private Role role;
 private String email; private String password; private String firstName; private String lastName; private String identityType; private String identityNumber; private String phone;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;}
 public Role getRole(){return role;} public void setRole(Role role){this.role=role;} public String getEmail(){return email;} public void setEmail(String email){this.email=email;} public String getPassword(){return password;} public void setPassword(String password){this.password=password;}
 public String getFirstName(){return firstName;} public void setFirstName(String firstName){this.firstName=firstName;} public String getLastName(){return lastName;} public void setLastName(String lastName){this.lastName=lastName;}
 public String getIdentityType(){return identityType;} public void setIdentityType(String identityType){this.identityType=identityType;} public String getIdentityNumber(){return identityNumber;} public void setIdentityNumber(String identityNumber){this.identityNumber=identityNumber;} public String getPhone(){return phone;} public void setPhone(String phone){this.phone=phone;}
}
""")
w(ub/"repository/UserRepository.java", """
package com.facilcomanda.userservice.repository;
import com.facilcomanda.userservice.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
public interface UserRepository extends JpaRepository<User, Long> {
 Optional<User> findByEmail(String email); Optional<User> findByIdAndOrganizationId(Long id, Long organizationId); List<User> findByOrganizationId(Long organizationId);
}
""")
w(ub/"repository/RoleRepository.java", """
package com.facilcomanda.userservice.repository;
import com.facilcomanda.userservice.entity.Role;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
public interface RoleRepository extends JpaRepository<Role, Long> { Optional<Role> findByIdAndOrganizationId(Long id, Long organizationId); List<Role> findByOrganizationId(Long organizationId); }
""")
w(ub/"service/UserService.java", """
package com.facilcomanda.userservice.service;
import com.facilcomanda.common.dto.*;
import com.facilcomanda.common.enums.RoleName;
import com.facilcomanda.common.event.EventPublisher;
import com.facilcomanda.userservice.entity.*;
import com.facilcomanda.userservice.repository.*;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class UserService {
 private final UserRepository users; private final RoleRepository roles; private final PasswordEncoder encoder; private final EventPublisher publisher;
 public UserService(UserRepository users, RoleRepository roles, PasswordEncoder encoder, EventPublisher publisher){this.users=users;this.roles=roles;this.encoder=encoder;this.publisher=publisher;}
 public UserResponse createUser(UserRequest request, Long organizationId){ if(request.password()==null||request.password().isBlank()) throw new IllegalArgumentException("Password is required for user creation"); User user=new User(); user.setOrganizationId(organizationId); user.setPassword(encoder.encode(request.password())); map(request,user,organizationId); User saved=users.save(user); UserResponse response=toResponse(saved); audit("CREATE", saved.getId(), null, response); return response; }
 public List<UserResponse> getAllUsers(Long organizationId){ return users.findByOrganizationId(organizationId).stream().map(this::toResponse).toList(); }
 public UserResponse getUserById(Long id, Long organizationId){ return toResponse(fetch(id,organizationId)); }
 public UserResponse updateUser(Long id, UserRequest request, Long organizationId){ User user=fetch(id,organizationId); UserResponse old=toResponse(user); if(request.password()!=null&&!request.password().isBlank()) user.setPassword(encoder.encode(request.password())); map(request,user,organizationId); User saved=users.save(user); UserResponse response=toResponse(saved); audit("UPDATE", id, old, response); return response; }
 public void deleteUser(Long id, Long organizationId){ User user=fetch(id,organizationId); UserResponse old=toResponse(user); users.delete(user); audit("DELETE", id, old, null); }
 public UserSnapshot findByEmail(String email){ return users.findByEmail(email).map(u -> new UserSnapshot(u.getId(), u.getEmail(), u.getFirstName(), u.getLastName(), u.getRole().getName().name(), u.getOrganizationId())).orElseThrow(() -> new RuntimeException("User not found")); }
 private void map(UserRequest request, User user, Long organizationId){ user.setEmail(request.email()); user.setFirstName(request.firstName()); user.setLastName(request.lastName()); Role role=roles.findByIdAndOrganizationId(request.roleId(), organizationId).orElseThrow(() -> new RuntimeException("Role not found or unauthorized")); user.setRole(role); }
 private User fetch(Long id, Long org){ return users.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("User not found or unauthorized")); }
 private UserResponse toResponse(User u){ return new UserResponse(u.getId(), u.getEmail(), u.getFirstName(), u.getLastName(), u.getRole()!=null?u.getRole().getName().name():null, u.getOrganizationId()); }
 private void audit(String op,Object id,Object old,Object val){ publisher.publishAudit("user-service","User",id,op,old,val,null,null,null,null); }
 public RoleResponse createRole(RoleRequest request, Long org){ Role r=new Role(); r.setOrganizationId(org); r.setName(RoleName.valueOf(request.name().toUpperCase())); r.setDescription(request.description()); Role saved=roles.save(r); RoleResponse res=toRole(saved); audit("CREATE", saved.getId(), null, res); return res; }
 public List<RoleResponse> getAllRoles(Long org){ return roles.findByOrganizationId(org).stream().map(this::toRole).toList(); }
 public RoleResponse getRoleById(Long id, Long org){ return toRole(fetchRole(id,org)); }
 public RoleResponse updateRole(Long id, RoleRequest request, Long org){ Role r=fetchRole(id,org); RoleResponse old=toRole(r); r.setName(RoleName.valueOf(request.name().toUpperCase())); r.setDescription(request.description()); RoleResponse res=toRole(roles.save(r)); audit("UPDATE", id, old, res); return res; }
 public void deleteRole(Long id, Long org){ Role r=fetchRole(id,org); RoleResponse old=toRole(r); roles.delete(r); audit("DELETE", id, old, null); }
 private Role fetchRole(Long id, Long org){ return roles.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("Role not found or unauthorized")); }
 private RoleResponse toRole(Role r){ return new RoleResponse(r.getId(), r.getName().name(), r.getDescription(), r.getOrganizationId()); }
}
""")
w(ub/"controller/UserController.java", """
package com.facilcomanda.userservice.controller;
import com.facilcomanda.common.dto.*;
import com.facilcomanda.common.web.AuthContext;
import com.facilcomanda.userservice.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/users")
public class UserController {
 private final UserService service; public UserController(UserService service){this.service=service;}
 @PostMapping public ResponseEntity<UserResponse> createUser(@Valid @RequestBody UserRequest request, Authentication auth){return new ResponseEntity<>(service.createUser(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<UserResponse>> getAllUsers(Authentication auth){return ResponseEntity.ok(service.getAllUsers(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<UserResponse> getUserById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getUserById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<UserResponse> updateUser(@PathVariable Long id,@Valid @RequestBody UserRequest request, Authentication auth){return ResponseEntity.ok(service.updateUser(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteUser(@PathVariable Long id, Authentication auth){service.deleteUser(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
 @GetMapping("/internal/by-email/{email}") public UserSnapshot findByEmail(@PathVariable String email){ return service.findByEmail(email); }
}
""")
w(ub/"controller/RoleController.java", """
package com.facilcomanda.userservice.controller;
import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import com.facilcomanda.userservice.service.UserService;
import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/roles")
public class RoleController {
 private final UserService service; public RoleController(UserService service){this.service=service;}
 @PostMapping public ResponseEntity<RoleResponse> createRole(@Valid @RequestBody RoleRequest request, Authentication auth){return new ResponseEntity<>(service.createRole(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<RoleResponse>> getAllRoles(Authentication auth){return ResponseEntity.ok(service.getAllRoles(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<RoleResponse> getRoleById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getRoleById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<RoleResponse> updateRole(@PathVariable Long id,@Valid @RequestBody RoleRequest request, Authentication auth){return ResponseEntity.ok(service.updateRole(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteRole(@PathVariable Long id, Authentication auth){service.deleteRole(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
}
""")

# Auth service
ab = java_base("auth-service")
w(ab/"entity/AuthUser.java", """
package com.facilcomanda.authservice.entity;
import com.facilcomanda.common.enums.RoleName;
import jakarta.persistence.*;
@Entity @Table(name = "users")
public class AuthUser {
 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
 @Column(name = "organization_id") private Long organizationId;
 @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "role_id") private AuthRole role;
 private String email; private String password; private String firstName; private String lastName;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;}
 public AuthRole getRole(){return role;} public void setRole(AuthRole role){this.role=role;} public String getEmail(){return email;} public void setEmail(String email){this.email=email;} public String getPassword(){return password;} public void setPassword(String password){this.password=password;}
 public String getFirstName(){return firstName;} public void setFirstName(String firstName){this.firstName=firstName;} public String getLastName(){return lastName;} public void setLastName(String lastName){this.lastName=lastName;}
}
""")
w(ab/"entity/AuthRole.java", """
package com.facilcomanda.authservice.entity;
import com.facilcomanda.common.enums.RoleName;
import jakarta.persistence.*;
@Entity @Table(name = "roles")
public class AuthRole {
 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
 @Column(name = "organization_id") private Long organizationId;
 @Enumerated(EnumType.STRING) private RoleName name; private String description;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;} public RoleName getName(){return name;} public void setName(RoleName name){this.name=name;} public String getDescription(){return description;} public void setDescription(String description){this.description=description;}
}
""")
w(ab/"entity/AuthOrganization.java", """
package com.facilcomanda.authservice.entity;
import jakarta.persistence.*;
@Entity @Table(name = "organizations")
public class AuthOrganization { @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id; private String name; private String taxIdentificationType; private String taxIdentificationNumber; public Long getId(){return id;} public void setId(Long id){this.id=id;} }
""")
w(ab/"repository/AuthUserRepository.java", "package com.facilcomanda.authservice.repository; import com.facilcomanda.authservice.entity.AuthUser; import org.springframework.data.jpa.repository.JpaRepository; import java.util.*; public interface AuthUserRepository extends JpaRepository<AuthUser,Long>{ Optional<AuthUser> findByEmail(String email); }")
w(ab/"repository/AuthRoleRepository.java", "package com.facilcomanda.authservice.repository; import com.facilcomanda.authservice.entity.AuthRole; import org.springframework.data.jpa.repository.JpaRepository; public interface AuthRoleRepository extends JpaRepository<AuthRole,Long>{}")
w(ab/"repository/AuthOrganizationRepository.java", "package com.facilcomanda.authservice.repository; import com.facilcomanda.authservice.entity.AuthOrganization; import org.springframework.data.jpa.repository.JpaRepository; public interface AuthOrganizationRepository extends JpaRepository<AuthOrganization,Long>{}")
w(ab/"service/AuthService.java", """
package com.facilcomanda.authservice.service;
import com.facilcomanda.authservice.entity.*; import com.facilcomanda.authservice.repository.*; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.event.EventPublisher; import com.facilcomanda.common.security.JwtService;
import org.springframework.security.crypto.password.PasswordEncoder; import org.springframework.stereotype.Service;
@Service
public class AuthService {
 private final AuthUserRepository users; private final AuthRoleRepository roles; private final AuthOrganizationRepository orgs; private final JwtService jwt; private final PasswordEncoder encoder; private final EventPublisher publisher;
 public AuthService(AuthUserRepository users, AuthRoleRepository roles, AuthOrganizationRepository orgs, JwtService jwt, PasswordEncoder encoder, EventPublisher publisher){this.users=users;this.roles=roles;this.orgs=orgs;this.jwt=jwt;this.encoder=encoder;this.publisher=publisher;}
 public UserAuthDTO register(RegisterRequest request){ if(users.findByEmail(request.email()).isPresent()) throw new RuntimeException("User with this email already exists."); orgs.findById(request.organizationId()).orElseThrow(() -> new RuntimeException("Organization not found.")); AuthRole role=roles.findById(request.roleId()).orElseThrow(() -> new RuntimeException("Role not found.")); AuthUser user=new AuthUser(); user.setEmail(request.email()); user.setFirstName(request.firstName()); user.setLastName(request.lastName()); user.setOrganizationId(request.organizationId()); user.setRole(role); user.setPassword(encoder.encode(request.password())); AuthUser saved=users.save(user); UserAuthDTO dto=new UserAuthDTO(saved.getId(), saved.getEmail(), saved.getFirstName(), saved.getLastName(), role.getName(), saved.getOrganizationId()); publisher.publishAudit("auth-service","User",saved.getId(),"CREATE",null,dto,null,null,null,null); return dto; }
 public LoginResponse login(LoginRequest request){ AuthUser user=users.findByEmail(request.email()).orElseThrow(() -> new RuntimeException("Usuario no encontrado")); if(!encoder.matches(request.password(), user.getPassword())) throw new RuntimeException("Credenciales invalidas"); String token=jwt.generateToken(user.getEmail(), user.getOrganizationId(), user.getRole().getName().name()); return new LoginResponse(token, new UserAuthDTO(user.getId(), user.getEmail(), user.getFirstName(), user.getLastName(), user.getRole().getName(), user.getOrganizationId())); }
}
""")
w(ab/"controller/AuthController.java", """
package com.facilcomanda.authservice.controller;
import com.facilcomanda.authservice.service.AuthService; import com.facilcomanda.common.dto.*; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/auth")
public class AuthController {
 private final AuthService service; public AuthController(AuthService service){this.service=service;}
 @PostMapping("/login") public LoginResponse login(@Valid @RequestBody LoginRequest request){ return service.login(request); }
 @PostMapping("/register") public ResponseEntity<UserAuthDTO> register(@Valid @RequestBody RegisterRequest request){ return new ResponseEntity<>(service.register(request), HttpStatus.CREATED); }
}
""")

# Category service
cb=java_base("category-service")
w(cb/"entity/Category.java", """
package com.facilcomanda.categoryservice.entity;
import jakarta.persistence.*;
@Entity @Table(name="categories", indexes=@Index(name="idx_category_org", columnList="organization_id"))
public class Category { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; @Column(name="organization_id") private Long organizationId; private String name; private String description; @ManyToOne @JoinColumn(name="parent_category_id") private Category parentCategory;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;} public String getName(){return name;} public void setName(String name){this.name=name;} public String getDescription(){return description;} public void setDescription(String description){this.description=description;} public Category getParentCategory(){return parentCategory;} public void setParentCategory(Category parentCategory){this.parentCategory=parentCategory;} }
""")
w(cb/"repository/CategoryRepository.java", "package com.facilcomanda.categoryservice.repository; import com.facilcomanda.categoryservice.entity.Category; import org.springframework.data.jpa.repository.JpaRepository; import java.util.*; public interface CategoryRepository extends JpaRepository<Category,Long>{ Optional<Category> findByIdAndOrganizationId(Long id, Long organizationId); List<Category> findByOrganizationId(Long organizationId); }")
w(cb/"service/CategoryService.java", """
package com.facilcomanda.categoryservice.service;
import com.facilcomanda.categoryservice.entity.Category; import com.facilcomanda.categoryservice.repository.CategoryRepository; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.event.EventPublisher; import org.springframework.stereotype.Service; import java.util.List;
@Service public class CategoryService { private final CategoryRepository repo; private final EventPublisher publisher; public CategoryService(CategoryRepository repo, EventPublisher publisher){this.repo=repo;this.publisher=publisher;}
 public CategoryResponse createCategory(CategoryRequest request, Long org){ Category c=new Category(); c.setOrganizationId(org); map(request,c,org); Category saved=repo.save(c); CategoryResponse res=toResponse(saved); audit("CREATE", saved.getId(), null, res); return res; }
 public List<CategoryResponse> getAllCategories(Long org){return repo.findByOrganizationId(org).stream().map(this::toResponse).toList();}
 public CategoryResponse getCategoryById(Long id, Long org){return toResponse(fetch(id,org));}
 public CategoryResponse updateCategory(Long id, CategoryRequest request, Long org){Category c=fetch(id,org); CategoryResponse old=toResponse(c); map(request,c,org); CategoryResponse res=toResponse(repo.save(c)); audit("UPDATE", id, old, res); return res;}
 public void deleteCategory(Long id, Long org){Category c=fetch(id,org); CategoryResponse old=toResponse(c); repo.delete(c); audit("DELETE", id, old, null);}
 private Category fetch(Long id,Long org){return repo.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("Category not found or unauthorized"));}
 private void map(CategoryRequest r, Category c, Long org){c.setName(r.name()); c.setDescription(r.description()); c.setParentCategory(r.parentCategoryId()==null?null:fetch(r.parentCategoryId(), org));}
 private CategoryResponse toResponse(Category c){return new CategoryResponse(c.getId(), c.getName(), c.getDescription(), c.getParentCategory()!=null?c.getParentCategory().getId():null);}
 private void audit(String op,Object id,Object old,Object val){publisher.publishAudit("category-service","Category",id,op,old,val,null,null,null,null);}
}
""")
w(cb/"controller/CategoryController.java", """
package com.facilcomanda.categoryservice.controller;
import com.facilcomanda.categoryservice.service.CategoryService; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/categories") public class CategoryController { private final CategoryService service; public CategoryController(CategoryService service){this.service=service;}
 @PostMapping public ResponseEntity<CategoryResponse> createCategory(@Valid @RequestBody CategoryRequest request, Authentication auth){return new ResponseEntity<>(service.createCategory(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<CategoryResponse>> getAllCategories(Authentication auth){return ResponseEntity.ok(service.getAllCategories(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<CategoryResponse> getCategoryById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getCategoryById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<CategoryResponse> updateCategory(@PathVariable Long id,@Valid @RequestBody CategoryRequest request, Authentication auth){return ResponseEntity.ok(service.updateCategory(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteCategory(@PathVariable Long id, Authentication auth){service.deleteCategory(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
 @GetMapping("/internal/{id}") public CategoryResponse internalCategory(@PathVariable Long id, @RequestHeader("X-Organization-ID") Long org){ return service.getCategoryById(id, org); }
}
""")

# Restaurant service
rb=java_base("restaurant-service")
w(rb/"entity/Organization.java", "package com.facilcomanda.restaurantservice.entity; import jakarta.persistence.*; @Entity @Table(name=\"organizations\") public class Organization { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; private String name; private String taxIdentificationType; private String taxIdentificationNumber; public Long getId(){return id;} public void setId(Long id){this.id=id;} public String getName(){return name;} public void setName(String name){this.name=name;} public String getTaxIdentificationType(){return taxIdentificationType;} public void setTaxIdentificationType(String taxIdentificationType){this.taxIdentificationType=taxIdentificationType;} public String getTaxIdentificationNumber(){return taxIdentificationNumber;} public void setTaxIdentificationNumber(String taxIdentificationNumber){this.taxIdentificationNumber=taxIdentificationNumber;} }")
w(rb/"entity/RestaurantFloor.java", "package com.facilcomanda.restaurantservice.entity; import jakarta.persistence.*; @Entity @Table(name=\"restaurant_floors\", indexes=@Index(name=\"idx_floor_org\", columnList=\"organization_id\")) public class RestaurantFloor { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; @Column(name=\"organization_id\") private Long organizationId; private String name; private String description; public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;} public String getName(){return name;} public void setName(String name){this.name=name;} public String getDescription(){return description;} public void setDescription(String description){this.description=description;} }")
w(rb/"repository/OrganizationRepository.java", "package com.facilcomanda.restaurantservice.repository; import com.facilcomanda.restaurantservice.entity.Organization; import org.springframework.data.jpa.repository.JpaRepository; public interface OrganizationRepository extends JpaRepository<Organization,Long>{}")
w(rb/"repository/RestaurantFloorRepository.java", "package com.facilcomanda.restaurantservice.repository; import com.facilcomanda.restaurantservice.entity.RestaurantFloor; import org.springframework.data.jpa.repository.JpaRepository; import java.util.*; public interface RestaurantFloorRepository extends JpaRepository<RestaurantFloor,Long>{ Optional<RestaurantFloor> findByIdAndOrganizationId(Long id,Long org); List<RestaurantFloor> findByOrganizationId(Long org); }")
w(rb/"service/RestaurantService.java", """
package com.facilcomanda.restaurantservice.service;
import com.facilcomanda.common.dto.*; import com.facilcomanda.common.event.EventPublisher; import com.facilcomanda.restaurantservice.entity.*; import com.facilcomanda.restaurantservice.repository.*; import org.springframework.stereotype.Service; import java.util.List;
@Service public class RestaurantService { private final OrganizationRepository orgs; private final RestaurantFloorRepository floors; private final EventPublisher publisher; public RestaurantService(OrganizationRepository orgs, RestaurantFloorRepository floors, EventPublisher publisher){this.orgs=orgs;this.floors=floors;this.publisher=publisher;}
 public OrganizationResponse createOrganization(OrganizationRequest r){Organization o=new Organization(); o.setName(r.name()); o.setTaxIdentificationNumber(r.taxIdentificationNumber()); o.setTaxIdentificationType(r.taxIdentificationType()); Organization saved=orgs.save(o); OrganizationResponse res=toOrg(saved); audit("Organization","CREATE",saved.getId(),null,res); return res;}
 public OrganizationResponse getOrganizationById(Long id){return toOrg(orgs.findById(id).orElseThrow(() -> new RuntimeException("Organization not found")));}
 public OrganizationResponse updateOrganization(Long id, OrganizationRequest r){Organization o=orgs.findById(id).orElseThrow(() -> new RuntimeException("Organization not found")); OrganizationResponse old=toOrg(o); o.setName(r.name()); o.setTaxIdentificationNumber(r.taxIdentificationNumber()); o.setTaxIdentificationType(r.taxIdentificationType()); OrganizationResponse res=toOrg(orgs.save(o)); audit("Organization","UPDATE",id,old,res); return res;}
 private OrganizationResponse toOrg(Organization o){return new OrganizationResponse(o.getId(),o.getName(),o.getTaxIdentificationNumber(),o.getTaxIdentificationType());}
 public RestaurantFloorResponse createFloor(RestaurantFloorRequest r, Long org){RestaurantFloor f=new RestaurantFloor(); f.setOrganizationId(org); f.setName(r.name()); f.setDescription(r.description()); RestaurantFloor saved=floors.save(f); RestaurantFloorResponse res=toFloor(saved); audit("RestaurantFloor","CREATE",saved.getId(),null,res); return res;}
 public List<RestaurantFloorResponse> getAllFloors(Long org){return floors.findByOrganizationId(org).stream().map(this::toFloor).toList();}
 public RestaurantFloorResponse getFloorById(Long id, Long org){return toFloor(fetchFloor(id,org));}
 public RestaurantFloorResponse updateFloor(Long id, RestaurantFloorRequest r, Long org){RestaurantFloor f=fetchFloor(id,org); RestaurantFloorResponse old=toFloor(f); f.setName(r.name()); f.setDescription(r.description()); RestaurantFloorResponse res=toFloor(floors.save(f)); audit("RestaurantFloor","UPDATE",id,old,res); return res;}
 public void deleteFloor(Long id, Long org){RestaurantFloor f=fetchFloor(id,org); RestaurantFloorResponse old=toFloor(f); floors.delete(f); audit("RestaurantFloor","DELETE",id,old,null);}
 private RestaurantFloor fetchFloor(Long id,Long org){return floors.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("Floor not found or unauthorized"));}
 private RestaurantFloorResponse toFloor(RestaurantFloor f){return new RestaurantFloorResponse(f.getId(), f.getName(), f.getDescription(), f.getOrganizationId());}
 private void audit(String entity,String op,Object id,Object old,Object val){publisher.publishAudit("restaurant-service",entity,id,op,old,val,null,null,null,null);}
}
""")
w(rb/"controller/OrganizationController.java", """
package com.facilcomanda.restaurantservice.controller; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import com.facilcomanda.restaurantservice.service.RestaurantService; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/organizations") public class OrganizationController { private final RestaurantService service; public OrganizationController(RestaurantService service){this.service=service;}
 @PostMapping public ResponseEntity<OrganizationResponse> createOrganization(@Valid @RequestBody OrganizationRequest request, Authentication auth){ if(!AuthContext.hasRole(auth,"WEB_OWNER")) throw new RuntimeException("Unauthorized: Only WEB_OWNER can create organizations"); return new ResponseEntity<>(service.createOrganization(request), HttpStatus.CREATED);}
 @GetMapping("/my") public ResponseEntity<OrganizationResponse> getMyOrganization(Authentication auth){return ResponseEntity.ok(service.getOrganizationById(AuthContext.organizationId(auth)));}
 @PutMapping("/my") public ResponseEntity<OrganizationResponse> updateMyOrganization(@Valid @RequestBody OrganizationRequest request, Authentication auth){ if(!AuthContext.hasRole(auth,"ORG_MASTER")) throw new RuntimeException("Unauthorized: Only ORG_MASTER can update this organization"); return ResponseEntity.ok(service.updateOrganization(AuthContext.organizationId(auth), request));}
}
""")
w(rb/"controller/RestaurantFloorController.java", """
package com.facilcomanda.restaurantservice.controller; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import com.facilcomanda.restaurantservice.service.RestaurantService; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/restaurant-floors") public class RestaurantFloorController { private final RestaurantService service; public RestaurantFloorController(RestaurantService service){this.service=service;}
 @PostMapping public ResponseEntity<RestaurantFloorResponse> createFloor(@Valid @RequestBody RestaurantFloorRequest request, Authentication auth){return new ResponseEntity<>(service.createFloor(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<RestaurantFloorResponse>> getAllFloors(Authentication auth){return ResponseEntity.ok(service.getAllFloors(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<RestaurantFloorResponse> getFloorById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getFloorById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<RestaurantFloorResponse> updateFloor(@PathVariable Long id,@Valid @RequestBody RestaurantFloorRequest request, Authentication auth){return ResponseEntity.ok(service.updateFloor(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteFloor(@PathVariable Long id, Authentication auth){service.deleteFloor(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
 @GetMapping("/internal/{id}") public RestaurantFloorResponse internalFloor(@PathVariable Long id, @RequestHeader("X-Organization-ID") Long org){return service.getFloorById(id, org);}
}
""")

# Product service
pb=java_base("product-service")
w(pb/"entity/Product.java", "package com.facilcomanda.productservice.entity; import jakarta.persistence.*; import java.math.BigDecimal; import java.time.LocalDateTime; import java.util.*; @Entity @Table(name=\"products\", indexes=@Index(name=\"idx_product_org\", columnList=\"organization_id\")) public class Product { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; @Column(name=\"organization_id\") private Long organizationId; private String name; private String description; private Integer stock; private BigDecimal unitPrice; private BigDecimal discount; private LocalDateTime expirationDate; @Version private Long version=0L; @ElementCollection @CollectionTable(name=\"product_category\", joinColumns=@JoinColumn(name=\"product_id\")) @Column(name=\"category_id\") private Set<Long> categoryIds=new HashSet<>(); public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;} public String getName(){return name;} public void setName(String name){this.name=name;} public String getDescription(){return description;} public void setDescription(String description){this.description=description;} public Integer getStock(){return stock;} public void setStock(Integer stock){this.stock=stock;} public BigDecimal getUnitPrice(){return unitPrice;} public void setUnitPrice(BigDecimal unitPrice){this.unitPrice=unitPrice;} public BigDecimal getDiscount(){return discount;} public void setDiscount(BigDecimal discount){this.discount=discount;} public LocalDateTime getExpirationDate(){return expirationDate;} public void setExpirationDate(LocalDateTime expirationDate){this.expirationDate=expirationDate;} public Set<Long> getCategoryIds(){return categoryIds;} public void setCategoryIds(Set<Long> categoryIds){this.categoryIds=categoryIds;} public Long getVersion(){return version;} public void setVersion(Long version){this.version=version;} }")
w(pb/"repository/ProductRepository.java", "package com.facilcomanda.productservice.repository; import com.facilcomanda.productservice.entity.Product; import org.springframework.data.jpa.repository.JpaRepository; import java.util.*; public interface ProductRepository extends JpaRepository<Product,Long>{ Optional<Product> findByIdAndOrganizationId(Long id,Long org); List<Product> findByOrganizationId(Long org); }")
w(pb/"client/CategoryClient.java", "package com.facilcomanda.productservice.client; import com.facilcomanda.common.config.FeignConfig; import com.facilcomanda.common.dto.CategoryResponse; import org.springframework.cloud.openfeign.FeignClient; import org.springframework.web.bind.annotation.*; @FeignClient(name=\"category-service\", configuration=FeignConfig.class) public interface CategoryClient { @GetMapping(\"/api/categories/internal/{id}\") CategoryResponse getCategory(@PathVariable Long id, @RequestHeader(\"X-Organization-ID\") Long org); }")
w(pb/"service/ProductService.java", """
package com.facilcomanda.productservice.service;
import com.facilcomanda.common.dto.*; import com.facilcomanda.common.event.EventPublisher; import com.facilcomanda.productservice.client.CategoryClient; import com.facilcomanda.productservice.entity.Product; import com.facilcomanda.productservice.repository.ProductRepository; import org.springframework.stereotype.Service; import org.springframework.transaction.annotation.Transactional; import java.util.*;
@Service public class ProductService { private final ProductRepository repo; private final CategoryClient categories; private final EventPublisher publisher; public ProductService(ProductRepository repo, CategoryClient categories, EventPublisher publisher){this.repo=repo;this.categories=categories;this.publisher=publisher;}
 public ProductResponse createProduct(ProductRequest request, Long org){Product p=new Product(); p.setOrganizationId(org); map(request,p,org); Product saved=repo.save(p); ProductResponse res=toResponse(saved,org); audit("CREATE",saved.getId(),null,res); return res;}
 public List<ProductResponse> getAllProducts(Long org){return repo.findByOrganizationId(org).stream().map(p -> toResponse(p,org)).toList();}
 public ProductResponse getProductById(Long id,Long org){return toResponse(fetch(id,org),org);}
 public ProductSnapshot getProductSnapshot(Long id,Long org){Product p=fetch(id,org); return new ProductSnapshot(p.getId(),p.getName(),p.getUnitPrice(),p.getDiscount(),p.getStock());}
 public ProductResponse updateProduct(Long id,ProductRequest r,Long org){Product p=fetch(id,org); ProductResponse old=toResponse(p,org); map(r,p,org); ProductResponse res=toResponse(repo.save(p),org); audit("UPDATE",id,old,res); return res;}
 public void deleteProduct(Long id,Long org){Product p=fetch(id,org); ProductResponse old=toResponse(p,org); repo.delete(p); audit("DELETE",id,old,null);}
 @Transactional public ProductSnapshot reserveStock(Long id, Integer quantity, Long org){Product p=fetch(id,org); if(p.getStock()<quantity) throw new RuntimeException("Insufficient stock for product: "+p.getName()); p.setStock(p.getStock()-quantity); repo.save(p); publisher.publishAudit("product-service","Product",id,"UPDATE_STOCK",null,getProductSnapshot(id,org),null,null,null,null); return getProductSnapshot(id,org);}
 private Product fetch(Long id,Long org){return repo.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("Product not found or access denied"));}
 private void map(ProductRequest r,Product p,Long org){p.setName(r.name()); p.setDescription(r.description()); p.setStock(r.stock()); p.setUnitPrice(r.unitPrice()); p.setDiscount(r.discount()); p.setExpirationDate(r.expirationDate()); Set<Long> ids=new HashSet<>(); if(r.categoryIds()!=null) for(Long id:r.categoryIds()){categories.getCategory(id,org); ids.add(id);} p.setCategoryIds(ids);}
 private ProductResponse toResponse(Product p,Long org){List<Long> ids=p.getCategoryIds()==null?List.of():new ArrayList<>(p.getCategoryIds()); List<String> names=ids.stream().map(id -> categories.getCategory(id,org).name()).toList(); return new ProductResponse(p.getId(),p.getName(),p.getDescription(),p.getStock(),p.getUnitPrice(),p.getDiscount(),p.getExpirationDate(),ids,names);}
 private void audit(String op,Object id,Object old,Object val){publisher.publishAudit("product-service","Product",id,op,old,val,null,null,null,null);}
}
""")
w(pb/"controller/ProductController.java", """
package com.facilcomanda.productservice.controller; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import com.facilcomanda.productservice.service.ProductService; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/products") public class ProductController { private final ProductService service; public ProductController(ProductService service){this.service=service;}
 @PostMapping public ResponseEntity<ProductResponse> createProduct(@Valid @RequestBody ProductRequest request, Authentication auth){return new ResponseEntity<>(service.createProduct(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<ProductResponse>> getAllProducts(Authentication auth){return ResponseEntity.ok(service.getAllProducts(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<ProductResponse> getProductById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getProductById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<ProductResponse> updateProduct(@PathVariable Long id,@Valid @RequestBody ProductRequest request, Authentication auth){return ResponseEntity.ok(service.updateProduct(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteProduct(@PathVariable Long id, Authentication auth){service.deleteProduct(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
 @GetMapping("/internal/{id}") public ProductSnapshot internalProduct(@PathVariable Long id, @RequestHeader("X-Organization-ID") Long org){return service.getProductSnapshot(id,org);}
 @PostMapping("/internal/{id}/reserve") public ProductSnapshot reserve(@PathVariable Long id, @RequestParam Integer quantity, @RequestHeader("X-Organization-ID") Long org){return service.reserveStock(id,quantity,org);}
}
""")

# Table service
tb=java_base("table-service")
w(tb/"entity/RestaurantTable.java", "package com.facilcomanda.tableservice.entity; import com.facilcomanda.common.enums.TableState; import jakarta.persistence.*; @Entity @Table(name=\"restaurant_tables\", indexes=@Index(name=\"idx_table_org\", columnList=\"organization_id\")) public class RestaurantTable { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; private Long organizationId; private String name; private String description; @Enumerated(EnumType.STRING) private TableState state; private Integer chairs; @Column(name=\"floor_id\") private Long floorId; public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;} public String getName(){return name;} public void setName(String name){this.name=name;} public String getDescription(){return description;} public void setDescription(String description){this.description=description;} public TableState getState(){return state;} public void setState(TableState state){this.state=state;} public Integer getChairs(){return chairs;} public void setChairs(Integer chairs){this.chairs=chairs;} public Long getFloorId(){return floorId;} public void setFloorId(Long floorId){this.floorId=floorId;} }")
w(tb/"repository/RestaurantTableRepository.java", "package com.facilcomanda.tableservice.repository; import com.facilcomanda.tableservice.entity.RestaurantTable; import org.springframework.data.jpa.repository.JpaRepository; import java.util.*; public interface RestaurantTableRepository extends JpaRepository<RestaurantTable,Long>{ Optional<RestaurantTable> findByIdAndOrganizationId(Long id,Long org); List<RestaurantTable> findByOrganizationId(Long org); List<RestaurantTable> findByFloorIdAndOrganizationId(Long floorId,Long org); }")
w(tb/"client/FloorClient.java", "package com.facilcomanda.tableservice.client; import com.facilcomanda.common.config.FeignConfig; import com.facilcomanda.common.dto.RestaurantFloorResponse; import org.springframework.cloud.openfeign.FeignClient; import org.springframework.web.bind.annotation.*; @FeignClient(name=\"restaurant-service\", configuration=FeignConfig.class) public interface FloorClient { @GetMapping(\"/api/restaurant-floors/internal/{id}\") RestaurantFloorResponse getFloor(@PathVariable Long id, @RequestHeader(\"X-Organization-ID\") Long org); }")
w(tb/"service/TableService.java", """
package com.facilcomanda.tableservice.service; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.enums.TableState; import com.facilcomanda.common.event.EventPublisher; import com.facilcomanda.tableservice.client.FloorClient; import com.facilcomanda.tableservice.entity.RestaurantTable; import com.facilcomanda.tableservice.repository.RestaurantTableRepository; import org.springframework.stereotype.Service; import java.util.List;
@Service public class TableService { private final RestaurantTableRepository repo; private final FloorClient floors; private final EventPublisher publisher; public TableService(RestaurantTableRepository repo, FloorClient floors, EventPublisher publisher){this.repo=repo;this.floors=floors;this.publisher=publisher;}
 public TableResponse createTable(TableRequest r,Long org){floors.getFloor(r.floorId(),org); RestaurantTable t=new RestaurantTable(); t.setOrganizationId(org); map(r,t); TableResponse res=toResponse(repo.save(t),org); audit("CREATE",res.id(),null,res); return res;}
 public List<TableResponse> getAllTables(Long org){return repo.findByOrganizationId(org).stream().map(t -> toResponse(t,org)).toList();}
 public List<TableResponse> getTablesByFloorAndOrganization(Long floorId,Long org){return repo.findByFloorIdAndOrganizationId(floorId,org).stream().map(t -> toResponse(t,org)).toList();}
 public TableResponse getTableById(Long id,Long org){return toResponse(fetch(id,org),org);}
 public TableResponse updateTable(Long id,TableRequest r,Long org){floors.getFloor(r.floorId(),org); RestaurantTable t=fetch(id,org); TableResponse old=toResponse(t,org); map(r,t); TableResponse res=toResponse(repo.save(t),org); audit("UPDATE",id,old,res); return res;}
 public void deleteTable(Long id,Long org){RestaurantTable t=fetch(id,org); TableResponse old=toResponse(t,org); repo.delete(t); audit("DELETE",id,old,null);}
 public TableResponse occupy(Long id,Long org){RestaurantTable t=fetch(id,org); t.setState(TableState.OCCUPIED); TableResponse res=toResponse(repo.save(t),org); audit("STATE_CHANGE",id,null,res); return res;}
 private RestaurantTable fetch(Long id,Long org){return repo.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("Table not found or unauthorized"));}
 private void map(TableRequest r,RestaurantTable t){t.setName(r.name()); t.setDescription(r.description()); t.setState(r.state()); t.setChairs(r.chairs()); t.setFloorId(r.floorId());}
 private TableResponse toResponse(RestaurantTable t,Long org){RestaurantFloorResponse f=floors.getFloor(t.getFloorId(),org); return new TableResponse(t.getId(),t.getName(),t.getDescription(),t.getState(),t.getChairs(),t.getOrganizationId(),t.getFloorId(),f.name());}
 private void audit(String op,Object id,Object old,Object val){publisher.publishAudit("table-service","RestaurantTable",id,op,old,val,null,null,null,null);}
}
""")
w(tb/"controller/TableController.java", """
package com.facilcomanda.tableservice.controller; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import com.facilcomanda.tableservice.service.TableService; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/tables") public class TableController { private final TableService service; public TableController(TableService service){this.service=service;}
 @PostMapping public ResponseEntity<TableResponse> createTable(@Valid @RequestBody TableRequest request, Authentication auth){return new ResponseEntity<>(service.createTable(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<TableResponse>> getAllTables(Authentication auth){return ResponseEntity.ok(service.getAllTables(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<TableResponse> getTableById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getTableById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<TableResponse> updateTable(@PathVariable Long id,@Valid @RequestBody TableRequest request, Authentication auth){return ResponseEntity.ok(service.updateTable(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteTable(@PathVariable Long id, Authentication auth){service.deleteTable(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
 @GetMapping("/floor/{floorId}") public ResponseEntity<List<TableResponse>> getTablesByFloorId(@PathVariable Long floorId, Authentication auth){return ResponseEntity.ok(service.getTablesByFloorAndOrganization(floorId, AuthContext.organizationId(auth)));}
 @PostMapping("/internal/{id}/occupy") public TableResponse occupy(@PathVariable Long id, @RequestHeader("X-Organization-ID") Long org){ return service.occupy(id,org); }
 @GetMapping("/internal/{id}") public TableResponse internal(@PathVariable Long id, @RequestHeader("X-Organization-ID") Long org){ return service.getTableById(id,org); }
}
""")

# Order service
ob=java_base("order-service")
w(ob/"entity/Order.java", "package com.facilcomanda.orderservice.entity; import com.facilcomanda.common.enums.OrderStatus; import jakarta.persistence.*; import java.math.BigDecimal; import java.time.LocalDateTime; import java.util.*; @Entity @Table(name=\"orders\", indexes=@Index(name=\"idx_order_org\", columnList=\"organization_id\"), uniqueConstraints=@UniqueConstraint(columnNames={\"organization_id\",\"idempotency_key\"})) public class Order { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; @Column(name=\"organization_id\") private Long organizationId; private LocalDateTime orderDate; private String type; private String comments; @Column(name=\"idempotency_key\") private String idempotencyKey; @Enumerated(EnumType.STRING) private OrderStatus status; @Column(name=\"restaurant_table_id\") private Long restaurantTableId; @Column(name=\"user_id\") private Long userId; @OneToMany(mappedBy=\"order\", cascade=CascadeType.ALL, orphanRemoval=true) private List<OrderItem> orderItems=new ArrayList<>(); private BigDecimal total; @Version private Long version=0L; public void addOrderItem(OrderItem item){orderItems.add(item); item.setOrder(this);} public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;} public LocalDateTime getOrderDate(){return orderDate;} public void setOrderDate(LocalDateTime orderDate){this.orderDate=orderDate;} public String getType(){return type;} public void setType(String type){this.type=type;} public String getComments(){return comments;} public void setComments(String comments){this.comments=comments;} public String getIdempotencyKey(){return idempotencyKey;} public void setIdempotencyKey(String idempotencyKey){this.idempotencyKey=idempotencyKey;} public OrderStatus getStatus(){return status;} public void setStatus(OrderStatus status){this.status=status;} public Long getRestaurantTableId(){return restaurantTableId;} public void setRestaurantTableId(Long restaurantTableId){this.restaurantTableId=restaurantTableId;} public Long getUserId(){return userId;} public void setUserId(Long userId){this.userId=userId;} public List<OrderItem> getOrderItems(){return orderItems;} public void setOrderItems(List<OrderItem> orderItems){this.orderItems=orderItems;} public BigDecimal getTotal(){return total;} public void setTotal(BigDecimal total){this.total=total;} public Long getVersion(){return version;} public void setVersion(Long version){this.version=version;} }")
w(ob/"entity/OrderItem.java", "package com.facilcomanda.orderservice.entity; import jakarta.persistence.*; import java.math.BigDecimal; @Entity @Table(name=\"order_items\", indexes=@Index(name=\"idx_order_item_org\", columnList=\"organization_id\")) public class OrderItem { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; @Column(name=\"organization_id\") private Long organizationId; @ManyToOne @JoinColumn(name=\"order_id\") private Order order; @Column(name=\"product_id\") private Long productId; private String productName; private Integer quantity; private BigDecimal subtotal; private String comments; public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;} public Order getOrder(){return order;} public void setOrder(Order order){this.order=order;} public Long getProductId(){return productId;} public void setProductId(Long productId){this.productId=productId;} public String getProductName(){return productName;} public void setProductName(String productName){this.productName=productName;} public Integer getQuantity(){return quantity;} public void setQuantity(Integer quantity){this.quantity=quantity;} public BigDecimal getSubtotal(){return subtotal;} public void setSubtotal(BigDecimal subtotal){this.subtotal=subtotal;} public String getComments(){return comments;} public void setComments(String comments){this.comments=comments;} }")
w(ob/"repository/OrderRepository.java", "package com.facilcomanda.orderservice.repository; import com.facilcomanda.orderservice.entity.Order; import org.springframework.data.jpa.repository.JpaRepository; import java.util.*; public interface OrderRepository extends JpaRepository<Order,Long>{ Optional<Order> findByIdAndOrganizationId(Long id,Long org); List<Order> findByOrganizationId(Long org); boolean existsByIdempotencyKeyAndOrganizationId(String key,Long org); }")
w(ob/"client/ProductClient.java", "package com.facilcomanda.orderservice.client; import com.facilcomanda.common.config.FeignConfig; import com.facilcomanda.common.dto.ProductSnapshot; import org.springframework.cloud.openfeign.FeignClient; import org.springframework.web.bind.annotation.*; @FeignClient(name=\"product-service\", configuration=FeignConfig.class) public interface ProductClient { @PostMapping(\"/api/products/internal/{id}/reserve\") ProductSnapshot reserve(@PathVariable Long id, @RequestParam Integer quantity, @RequestHeader(\"X-Organization-ID\") Long org); }")
w(ob/"client/TableClient.java", "package com.facilcomanda.orderservice.client; import com.facilcomanda.common.config.FeignConfig; import com.facilcomanda.common.dto.TableResponse; import org.springframework.cloud.openfeign.FeignClient; import org.springframework.web.bind.annotation.*; @FeignClient(name=\"table-service\", configuration=FeignConfig.class) public interface TableClient { @PostMapping(\"/api/tables/internal/{id}/occupy\") TableResponse occupy(@PathVariable Long id, @RequestHeader(\"X-Organization-ID\") Long org); @GetMapping(\"/api/tables/internal/{id}\") TableResponse get(@PathVariable Long id, @RequestHeader(\"X-Organization-ID\") Long org); }")
w(ob/"client/UserClient.java", "package com.facilcomanda.orderservice.client; import com.facilcomanda.common.config.FeignConfig; import com.facilcomanda.common.dto.UserSnapshot; import org.springframework.cloud.openfeign.FeignClient; import org.springframework.web.bind.annotation.*; @FeignClient(name=\"user-service\", configuration=FeignConfig.class) public interface UserClient { @GetMapping(\"/api/users/internal/by-email/{email}\") UserSnapshot byEmail(@PathVariable String email); }")
w(ob/"service/OrderService.java", """
package com.facilcomanda.orderservice.service; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.enums.OrderStatus; import com.facilcomanda.common.event.EventPublisher; import com.facilcomanda.orderservice.client.*; import com.facilcomanda.orderservice.entity.*; import com.facilcomanda.orderservice.repository.OrderRepository; import org.springframework.stereotype.Service; import org.springframework.transaction.annotation.Transactional; import java.math.BigDecimal; import java.time.LocalDateTime; import java.util.List;
@Service public class OrderService { private final OrderRepository repo; private final TableClient tables; private final ProductClient products; private final UserClient users; private final EventPublisher publisher; public OrderService(OrderRepository repo,TableClient tables,ProductClient products,UserClient users,EventPublisher publisher){this.repo=repo;this.tables=tables;this.products=products;this.users=users;this.publisher=publisher;}
 @Transactional(rollbackFor=Exception.class) public OrderResponse createOrder(OrderRequest r, Long org, String email){ if(repo.existsByIdempotencyKeyAndOrganizationId(r.idempotencyKey(),org)) throw new RuntimeException("Order already processed"); UserSnapshot user=users.byEmail(email); TableResponse table=null; if(r.restaurantTableId()!=null) table=tables.occupy(r.restaurantTableId(),org); Order order=new Order(); order.setOrganizationId(org); order.setRestaurantTableId(r.restaurantTableId()); order.setUserId(user.id()); order.setStatus(OrderStatus.PENDING); order.setType(r.type()); order.setOrderDate(LocalDateTime.now()); order.setIdempotencyKey(r.idempotencyKey()); BigDecimal total=BigDecimal.ZERO; for(OrderItemRequest item:r.items()){ ProductSnapshot product=products.reserve(item.productId(),item.quantity(),org); BigDecimal price=product.unitPrice(); if(product.discount()!=null) price=price.subtract(product.discount()); BigDecimal subtotal=price.multiply(BigDecimal.valueOf(item.quantity())); OrderItem oi=new OrderItem(); oi.setOrganizationId(org); oi.setProductId(product.id()); oi.setProductName(product.name()); oi.setQuantity(item.quantity()); oi.setComments(item.comments()); oi.setSubtotal(subtotal); order.addOrderItem(oi); total=total.add(subtotal);} order.setTotal(total); Order saved=repo.save(order); OrderResponse res=toResponse(saved,table,org); publisher.publishAudit("order-service","Order",saved.getId(),"CREATE",null,res,email,null,null,null); return res; }
 public List<OrderResponse> getActiveOrders(Long org){ return repo.findByOrganizationId(org).stream().map(o -> toResponse(o, o.getRestaurantTableId()==null?null:tables.get(o.getRestaurantTableId(),org), org)).toList(); }
 private OrderResponse toResponse(Order o, TableResponse table, Long org){ List<OrderItemResponse> items=o.getOrderItems().stream().map(i -> new OrderItemResponse(i.getId(),i.getProductId(),i.getProductName(),i.getQuantity(),i.getSubtotal(),i.getComments())).toList(); return new OrderResponse(o.getId(), o.getRestaurantTableId(), table!=null?table.name():null, table!=null?table.floorName():null, o.getType(), o.getStatus(), o.getTotal(), o.getOrderDate(), items); }
}
""")
w(ob/"controller/OrderController.java", """
package com.facilcomanda.orderservice.controller; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import com.facilcomanda.orderservice.service.OrderService; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/orders") public class OrderController { private final OrderService service; public OrderController(OrderService service){this.service=service;}
 @PostMapping public ResponseEntity<OrderResponse> createOrder(@Valid @RequestBody OrderRequest request, Authentication auth){return new ResponseEntity<>(service.createOrder(request, AuthContext.organizationId(auth), auth.getName()), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<OrderResponse>> getActiveOrders(Authentication auth){return ResponseEntity.ok(service.getActiveOrders(AuthContext.organizationId(auth)));}
}
""")

# Audit service
aub=java_base("audit-service")
w(aub/"entity/AuditLog.java", """
package com.facilcomanda.auditservice.entity; import jakarta.persistence.*; import java.time.Instant;
@Entity @Table(name="audit_logs", indexes={@Index(name="idx_audit_entity", columnList="entityName,entityId"), @Index(name="idx_audit_user", columnList="performedBy")})
public class AuditLog { @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id; private String serviceName; private String entityName; private String entityId; private String operation; @Column(columnDefinition="TEXT") private String oldValues; @Column(columnDefinition="TEXT") private String newValues; private String performedBy; private String requestIp; private String correlationId; private String traceId; private Instant createdAt; public Long getId(){return id;} public void setId(Long id){this.id=id;} public String getServiceName(){return serviceName;} public void setServiceName(String serviceName){this.serviceName=serviceName;} public String getEntityName(){return entityName;} public void setEntityName(String entityName){this.entityName=entityName;} public String getEntityId(){return entityId;} public void setEntityId(String entityId){this.entityId=entityId;} public String getOperation(){return operation;} public void setOperation(String operation){this.operation=operation;} public String getOldValues(){return oldValues;} public void setOldValues(String oldValues){this.oldValues=oldValues;} public String getNewValues(){return newValues;} public void setNewValues(String newValues){this.newValues=newValues;} public String getPerformedBy(){return performedBy;} public void setPerformedBy(String performedBy){this.performedBy=performedBy;} public String getRequestIp(){return requestIp;} public void setRequestIp(String requestIp){this.requestIp=requestIp;} public String getCorrelationId(){return correlationId;} public void setCorrelationId(String correlationId){this.correlationId=correlationId;} public String getTraceId(){return traceId;} public void setTraceId(String traceId){this.traceId=traceId;} public Instant getCreatedAt(){return createdAt;} public void setCreatedAt(Instant createdAt){this.createdAt=createdAt;} }
""")
w(aub/"repository/AuditLogRepository.java", "package com.facilcomanda.auditservice.repository; import com.facilcomanda.auditservice.entity.AuditLog; import org.springframework.data.jpa.repository.JpaRepository; import java.util.*; public interface AuditLogRepository extends JpaRepository<AuditLog,Long>{ List<AuditLog> findByEntityNameAndEntityId(String entityName,String entityId); List<AuditLog> findByPerformedBy(String performedBy); }")
w(aub/"service/AuditService.java", """
package com.facilcomanda.auditservice.service; import com.facilcomanda.auditservice.entity.AuditLog; import com.facilcomanda.auditservice.repository.AuditLogRepository; import com.facilcomanda.common.event.AuditEvent; import org.springframework.amqp.rabbit.annotation.RabbitListener; import org.springframework.stereotype.Service; import java.util.List;
@Service public class AuditService { private final AuditLogRepository repo; public AuditService(AuditLogRepository repo){this.repo=repo;}
 @RabbitListener(queues="audit.queue") public void consume(AuditEvent e){ AuditLog l=new AuditLog(); l.setServiceName(e.serviceName()); l.setEntityName(e.entityName()); l.setEntityId(e.entityId()); l.setOperation(e.operation()); l.setOldValues(e.oldValues()); l.setNewValues(e.newValues()); l.setPerformedBy(e.performedBy()); l.setRequestIp(e.requestIp()); l.setCorrelationId(e.correlationId()); l.setTraceId(e.traceId()); l.setCreatedAt(e.createdAt()); repo.save(l); }
 public List<AuditLog> all(){return repo.findAll();} public AuditLog byId(Long id){return repo.findById(id).orElseThrow(() -> new RuntimeException("Audit log not found"));} public List<AuditLog> byEntity(String entity,String id){return repo.findByEntityNameAndEntityId(entity,id);} public List<AuditLog> byUser(String user){return repo.findByPerformedBy(user);}
}
""")
w(aub/"controller/AuditController.java", "package com.facilcomanda.auditservice.controller; import com.facilcomanda.auditservice.entity.AuditLog; import com.facilcomanda.auditservice.service.AuditService; import org.springframework.web.bind.annotation.*; import java.util.List; @RestController @RequestMapping(\"/api/audit\") public class AuditController { private final AuditService service; public AuditController(AuditService service){this.service=service;} @GetMapping public List<AuditLog> all(){return service.all();} @GetMapping(\"/{id}\") public AuditLog byId(@PathVariable Long id){return service.byId(id);} @GetMapping(\"/entity/{entityName}/{entityId}\") public List<AuditLog> byEntity(@PathVariable String entityName,@PathVariable String entityId){return service.byEntity(entityName,entityId);} @GetMapping(\"/user/{userId}\") public List<AuditLog> byUser(@PathVariable String userId){return service.byUser(userId);} }")

# Docker and docs
w("Dockerfile", """
FROM maven:3.9.8-eclipse-temurin-17 AS build
WORKDIR /workspace
COPY . .
ARG SERVICE
RUN mvn -pl ${SERVICE} -am -DskipTests package
FROM eclipse-temurin:17-jre
WORKDIR /app
ARG SERVICE
COPY --from=build /workspace/${SERVICE}/target/*.jar app.jar
ENTRYPOINT ["java","-jar","/app/app.jar"]
""")

compose_services = []
for module, port in ports.items():
    compose_services.append(f"""
  {module}:
    build:
      context: .
      args:
        SERVICE: {module}
    environment:
      CONFIG_SERVER_URL: http://config-server:8888
      EUREKA_DEFAULT_ZONE: http://discovery-server:8761/eureka
      DB_URL: jdbc:postgresql://postgres:5432/{module.replace('-', '_')}
      DB_USER: postgres
      DB_PASSWORD: postgres
      RABBITMQ_HOST: rabbitmq
    depends_on:
      - config-server
      - discovery-server
      - rabbitmq
      - postgres
    ports:
      - "{port}:{port}"
""")
w("docker-compose.yml", """
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: facilcomanda
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init:/docker-entrypoint-initdb.d:ro
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
  discovery-server:
    build:
      context: .
      args:
        SERVICE: discovery-server
    ports:
      - "8761:8761"
  config-server:
    build:
      context: .
      args:
        SERVICE: config-server
    environment:
      EUREKA_DEFAULT_ZONE: http://discovery-server:8761/eureka
    depends_on:
      - discovery-server
    ports:
      - "8888:8888"
  api-gateway:
    build:
      context: .
      args:
        SERVICE: api-gateway
    environment:
      CONFIG_SERVER_URL: http://config-server:8888
      EUREKA_DEFAULT_ZONE: http://discovery-server:8761/eureka
    depends_on:
      - config-server
      - discovery-server
    ports:
      - "8080:8080"
""" + "".join(compose_services) + """
volumes:
  postgres_data:
""")

w("docker/postgres/init/01-create-databases.sql", """
CREATE DATABASE auth_service;
CREATE DATABASE audit_service;
CREATE DATABASE user_service;
CREATE DATABASE category_service;
CREATE DATABASE product_service;
CREATE DATABASE restaurant_service;
CREATE DATABASE table_service;
CREATE DATABASE order_service;
""")

w("README.md", """
# FacilComanda Microservices

Migrated Spring Boot microservices workspace for the former `FacilComanda` monolith.

## Requirements

- Java 17
- Maven 3.9+
- Docker
- Docker Compose

## Build

```bash
mvn clean install
```

## Run Infrastructure

```bash
docker compose up -d rabbitmq postgres discovery-server config-server api-gateway
```

PostgreSQL initialization creates one database per data-owning service using `docker/postgres/init/01-create-databases.sql`.

## Run All Services

```bash
docker compose up --build
```

## Useful URLs

- Eureka Dashboard: http://localhost:8761
- RabbitMQ Dashboard: http://localhost:15672
- API Gateway: http://localhost:8080
- Auth Swagger: http://localhost:8081/swagger-ui.html
- User Swagger: http://localhost:8082/swagger-ui.html
- Category Swagger: http://localhost:8083/swagger-ui.html
- Product Swagger: http://localhost:8084/swagger-ui.html
- Restaurant Swagger: http://localhost:8085/swagger-ui.html
- Table Swagger: http://localhost:8086/swagger-ui.html
- Order Swagger: http://localhost:8087/swagger-ui.html
- Audit Swagger: http://localhost:8088/swagger-ui.html
- Actuator health: `/actuator/health` on every service

## Environment Variables

- `CONFIG_SERVER_URL`
- `EUREKA_DEFAULT_ZONE`
- `DB_URL`
- `DB_USER`
- `DB_PASSWORD`
- `DB_DDL_AUTO`
- `RABBITMQ_HOST`
- `RABBITMQ_PORT`
- `RABBITMQ_USER`
- `RABBITMQ_PASSWORD`
- `JWT_SECRET`
- `JWT_EXPIRATION`

## Gateway Routes

- `/api/auth/**` -> auth-service
- `/api/users/**`, `/api/roles/**` -> user-service
- `/api/categories/**` -> category-service
- `/api/products/**` -> product-service
- `/api/organizations/**`, `/api/restaurant-floors/**` -> restaurant-service
- `/api/tables/**` -> table-service
- `/api/orders/**` -> order-service
- `/api/audit/**` -> audit-service
""")

w(".gitignore", """
target/
.idea/
.vscode/
*.iml
*.log
.env
""")

w("docs/01-monolith-analysis.md", """
# 01 - Monolith Analysis

## Current Architecture Summary

The source backend is a Maven Spring Boot monolith (`com.facilcomanda.erp`) using Spring Boot 3.2.5 and Java 17. It exposes REST APIs under `/api/**`, persists data with Spring Data JPA and PostgreSQL, validates request records with Jakarta Validation, and secures requests with a stateless JWT filter.

The application package is organized by technical layer: `controller`, `service`, `repository`, `model`, `model.enums`, `dto`, and `security`.

## Main Dependencies

- Spring Boot Starter Web
- Spring Boot Starter Data JPA
- Spring Boot Starter Security
- Spring Boot Starter Validation
- PostgreSQL driver
- JJWT 0.12.5
- OpenPDF 1.3.30
- Spring Boot Test and Spring Security Test

## Database Configuration

The monolith uses PostgreSQL from `application.yml`, loading optional `.env` values. Hibernate uses `ddl-auto: validate`, `PostgreSQLDialect`, and tenant filtering is implemented with Hibernate filters using `organization_id`.

## Security And Authentication

- `POST /api/auth/login` and `POST /api/auth/register` are public.
- Other `/api/**` routes require authentication.
- JWT contains `organizationId` and `role` claims.
- `AuthenticationFilter` extracts the JWT and creates `CustomAuthentication`.
- `TenantFilterEnabler` enables Hibernate `tenantFilter` based on `organizationId`.
- Passwords use BCrypt.

## Detected Domains

- Auth: login, register, JWT creation and validation.
- User and role management: users, roles, password encoding.
- Organization/restaurant: organizations and floors.
- Table management: restaurant tables and table state.
- Catalog: categories and products.
- Ordering: orders, order items, table occupancy, stock deduction.

## Entities

- `Organization`: restaurant/company owner data.
- `Role`: role per organization.
- `User`: user account tied to role and organization.
- `Category`: product category with optional parent category.
- `Product`: stock, pricing, discount, expiration, many-to-many categories.
- `RestaurantFloor`: floor/area in a restaurant.
- `RestaurantTable`: table with state, chairs, and floor.
- `Order`: idempotent order, status, table, user, total, optimistic version.
- `OrderItem`: ordered product, quantity, subtotal, comments.

## API Endpoints

- `POST /api/auth/login`
- `POST /api/auth/register`
- `POST /api/categories`
- `GET /api/categories`
- `GET /api/categories/{id}`
- `PUT /api/categories/{id}`
- `DELETE /api/categories/{id}`
- `POST /api/products`
- `GET /api/products`
- `GET /api/products/{id}`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`
- `POST /api/organizations`
- `GET /api/organizations/my`
- `PUT /api/organizations/my`
- `POST /api/restaurant-floors`
- `GET /api/restaurant-floors`
- `GET /api/restaurant-floors/{id}`
- `PUT /api/restaurant-floors/{id}`
- `DELETE /api/restaurant-floors/{id}`
- `POST /api/roles`
- `GET /api/roles`
- `GET /api/roles/{id}`
- `PUT /api/roles/{id}`
- `DELETE /api/roles/{id}`
- `POST /api/tables`
- `GET /api/tables`
- `GET /api/tables/{id}`
- `PUT /api/tables/{id}`
- `DELETE /api/tables/{id}`
- `GET /api/tables/floor/{floorId}`
- `POST /api/users`
- `GET /api/users`
- `GET /api/users/{id}`
- `PUT /api/users/{id}`
- `DELETE /api/users/{id}`
- `POST /api/orders`
- `GET /api/orders`

## Main Relationships

- `User` belongs to an organization and role.
- `Role` belongs to an organization.
- `Category` belongs to an organization and may have a parent category.
- `Product` belongs to an organization and has many categories.
- `RestaurantTable` belongs to a floor and organization.
- `Order` belongs to an organization, optional table, and user.
- `OrderItem` belongs to an order and product.

## Transaction Boundaries

The main explicit transaction is order creation. It checks idempotency, loads the authenticated user, occupies the selected table, validates and deducts product stock, calculates item subtotals and total, and persists the order with cascading order items.

## Risks And Assumptions

- The monolith enum contains Spanish role names, while organization authorization checks mention `WEB_OWNER` and `ORG_MASTER`; the migration keeps both sets as compatible role values.
- The generated microservices remove cross-service JPA relationships and replace them with IDs and Feign calls.
- Product category names now require category-service availability.
- Order creation is no longer a single local database transaction across products, tables, and orders; it uses synchronous service calls and audit events.
- Hibernate tenant filters were replaced by explicit `organizationId` repository filters per service.
""")

w("docs/02-microservices-boundaries.md", """
# 02 - Microservices Boundaries

## Final Service List

- `api-gateway`
- `discovery-server`
- `config-server`
- `shared-common`
- `auth-service`
- `user-service`
- `category-service`
- `product-service`
- `restaurant-service`
- `table-service`
- `order-service`
- `audit-service`

## Responsibilities And Owned Data

| Service | Responsibility | Owned entities |
| --- | --- | --- |
| `auth-service` | Login, registration, JWT issuance | Auth projection of users, roles, organizations |
| `user-service` | User and role CRUD | `User`, `Role` |
| `category-service` | Category CRUD and category lookup | `Category` |
| `product-service` | Product CRUD, category association IDs, stock reservation | `Product` |
| `restaurant-service` | Organization profile and restaurant floors | `Organization`, `RestaurantFloor` |
| `table-service` | Restaurant table CRUD and table state | `RestaurantTable` |
| `order-service` | Order creation/listing, idempotency, total calculation | `Order`, `OrderItem` |
| `audit-service` | Central audit event consumption and querying | `AuditLog` |
| `shared-common` | DTOs, enums, JWT/security utilities, events, Feign/Rabbit config | No business tables |

## API Endpoints Per Service

- `auth-service`: `/api/auth/login`, `/api/auth/register`
- `user-service`: `/api/users/**`, `/api/roles/**`
- `category-service`: `/api/categories/**`
- `product-service`: `/api/products/**`
- `restaurant-service`: `/api/organizations/**`, `/api/restaurant-floors/**`
- `table-service`: `/api/tables/**`
- `order-service`: `/api/orders/**`
- `audit-service`: `/api/audit/**`

## Required Feign Clients

- `product-service` -> `category-service` for validating category IDs and resolving names.
- `table-service` -> `restaurant-service` for validating floors and resolving floor names.
- `order-service` -> `user-service` for resolving authenticated user by email.
- `order-service` -> `table-service` for table occupancy and table details.
- `order-service` -> `product-service` for stock reservation and product snapshots.

## RabbitMQ Events

Exchanges:

- `domain.events.exchange`
- `audit.events.exchange`

Audit queue:

- `audit.queue` bound to `audit.created`

Routing keys planned for domain events:

- `user.created`
- `user.updated`
- `product.created`
- `product.updated`
- `product.deleted`
- `category.created`
- `category.updated`
- `category.deleted`
- `order.created`
- `order.updated`
- `order.paid`
- `order.cancelled`
- `audit.created`

The current implementation publishes audit events for create/update/delete/state-change operations and provides common domain event contracts for further asynchronous consumers.

## Shared Code Candidates

- DTO records from the monolith.
- Enums: `RoleName`, `OrderStatus`, `TableState`.
- JWT generation and validation.
- Custom authentication.
- Security filter chain defaults.
- Global exception handling.
- Correlation ID filter.
- RabbitMQ event contracts and configuration.
- Feign header propagation.

## Database Strategy

Each service is designed to own its tables logically. For local development, Docker Compose provisions a shared PostgreSQL instance with service-specific database URLs. Cross-service JPA relationships were replaced with scalar IDs:

- `Product.categoryIds`
- `RestaurantTable.floorId`
- `Order.restaurantTableId`
- `Order.userId`
- `OrderItem.productId`

This keeps the migration scalable while preserving the external API contracts.
""")

print("Generated microservices workspace")
