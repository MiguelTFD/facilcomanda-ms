package com.facilcomanda.common.dto;
import com.facilcomanda.common.enums.OrderStatus; import jakarta.validation.constraints.NotNull; public record OrderStatusRequest(@NotNull OrderStatus status) {}
