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
