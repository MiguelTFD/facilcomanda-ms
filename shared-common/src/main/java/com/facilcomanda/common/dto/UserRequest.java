package com.facilcomanda.common.dto;
import jakarta.validation.constraints.Email; import jakarta.validation.constraints.NotBlank; import jakarta.validation.constraints.NotNull; public record UserRequest(@NotBlank @Email String email, String password, @NotBlank String firstName, @NotBlank String lastName, @NotNull Long roleId) {}
