package com.facilcomanda.userservice.entity;
import com.facilcomanda.common.enums.RoleName;
import jakarta.persistence.*;
@Entity @Table(name = "roles", indexes = @Index(name = "idx_role_org", columnList = "organization_id"))
public class Role {
 @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
 @Column(name = "organization_id") private Long organizationId;
 @Enumerated(EnumType.STRING) private RoleName name;
 private String description;
 public Long getId(){return id;} public void setId(Long id){this.id=id;} public Long getOrganizationId(){return organizationId;} public void setOrganizationId(Long organizationId){this.organizationId=organizationId;}
 public RoleName getName(){return name;} public void setName(RoleName name){this.name=name;} public String getDescription(){return description;} public void setDescription(String description){this.description=description;}
}
