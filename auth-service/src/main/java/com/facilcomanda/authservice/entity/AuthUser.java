package com.facilcomanda.authservice.entity;
import com.facilcomanda.common.enums.RoleName;
import jakarta.persistence.*;
@Entity @Table(name = "users")
public class AuthUser {
 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
 @Column(name = "organization_id") private Long organizationId;
 @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "role_id") private AuthRole role;
 private String email; private String password; private String firstName; private String lastName;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;}
 public AuthRole getRole(){return role;} public void setRole(AuthRole role){this.role=role;} public String getEmail(){return email;} public void setEmail(String email){this.email=email;} public String getPassword(){return password;} public void setPassword(String password){this.password=password;}
 public String getFirstName(){return firstName;} public void setFirstName(String firstName){this.firstName=firstName;} public String getLastName(){return lastName;} public void setLastName(String lastName){this.lastName=lastName;}
}
