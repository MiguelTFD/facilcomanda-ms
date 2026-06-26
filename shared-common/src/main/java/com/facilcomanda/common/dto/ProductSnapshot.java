package com.facilcomanda.common.dto;
import java.math.BigDecimal; public record ProductSnapshot(Long id, String name, BigDecimal unitPrice, BigDecimal discount, Integer stock) {}
