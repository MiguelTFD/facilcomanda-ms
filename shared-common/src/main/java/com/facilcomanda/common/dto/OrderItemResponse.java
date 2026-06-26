package com.facilcomanda.common.dto;
import java.math.BigDecimal; public record OrderItemResponse(Long id, Long productId, String productName, Integer quantity, BigDecimal subtotal, String comments) {}
