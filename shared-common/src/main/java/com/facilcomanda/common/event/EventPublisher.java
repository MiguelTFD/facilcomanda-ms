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
