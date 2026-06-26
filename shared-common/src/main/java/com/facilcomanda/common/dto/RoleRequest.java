package com.facilcomanda.common.dto;
import jakarta.validation.constraints.NotBlank; public record RoleRequest(@NotBlank String name, String description) {}
