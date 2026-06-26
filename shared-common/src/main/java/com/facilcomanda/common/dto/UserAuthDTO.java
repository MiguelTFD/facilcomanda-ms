package com.facilcomanda.common.dto;
import com.facilcomanda.common.enums.RoleName; public record UserAuthDTO(Long id, String email, String firstName, String lastName, RoleName roleName, Long organizationId) {}
