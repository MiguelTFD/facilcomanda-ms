package com.facilcomanda.common.security;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import java.util.Collection;
public class CustomAuthentication implements Authentication {
    private final String email; private final Collection<? extends GrantedAuthority> authorities; private final Long organizationId;
    private Object details; private boolean authenticated = true;
    public CustomAuthentication(String email, Collection<? extends GrantedAuthority> authorities, Long organizationId) { this.email = email; this.authorities = authorities; this.organizationId = organizationId; }
    public Collection<? extends GrantedAuthority> getAuthorities() { return authorities; }
    public Object getCredentials() { return null; }
    public Object getDetails() { return details; }
    public void setDetails(Object details) { this.details = details; }
    public Object getPrincipal() { return email; }
    public boolean isAuthenticated() { return authenticated; }
    public void setAuthenticated(boolean authenticated) throws IllegalArgumentException { this.authenticated = authenticated; }
    public String getName() { return email; }
    public Long getOrganizationId() { return organizationId; }
}
