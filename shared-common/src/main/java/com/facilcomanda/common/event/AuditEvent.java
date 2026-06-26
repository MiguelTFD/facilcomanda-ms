package com.facilcomanda.common.event;
import java.time.Instant;
public record AuditEvent(String serviceName, String entityName, String entityId, String operation, String oldValues,
                         String newValues, String performedBy, String requestIp, String correlationId,
                         String traceId, Instant createdAt) {}
