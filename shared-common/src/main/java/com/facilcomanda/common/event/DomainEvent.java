package com.facilcomanda.common.event;
import java.time.Instant;
public record DomainEvent(String serviceName, String entityName, String entityId, String eventType, Object payload,
                          String correlationId, String traceId, Instant createdAt) {}
