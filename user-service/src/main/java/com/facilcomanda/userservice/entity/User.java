package com.facilcomanda.userservice.entity;
import jakarta.persistence.*;
@Entity @Table(name = "users", indexes = @Index(name = "idx_user_org", columnList = "organization_id"))
public class User {
 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
 @Column(name = "organization_id") private Long organizationId;
 @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "role_id") private Role role;
 private String email; private String password; private String firstName; private String lastName; private String identityType; private String identityNumber; private String phone;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;}
 public Role getRole(){return role;} public void setRole(Role role){this.role=role;} public String getEmail(){return email;} public void setEmail(String email){this.email=email;} public String getPassword(){return password;} public void setPassword(String password){this.password=password;}
 public String getFirstName(){return firstName;} public void setFirstName(String firstName){this.firstName=firstName;} public String getLastName(){return lastName;} public void setLastName(String lastName){this.lastName=lastName;}
 public String getIdentityType(){return identityType;} public void setIdentityType(String identityType){this.identityType=identityType;} public String getIdentityNumber(){return identityNumber;} public void setIdentityNumber(String identityNumber){this.identityNumber=identityNumber;} public String getPhone(){return phone;} public void setPhone(String phone){this.phone=phone;}
}
