package com.facilcomanda.authservice.entity;
import jakarta.persistence.*;
@Entity @Table(name = "organizations")
public class AuthOrganization { @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id; private String name; private String taxIdentificationType; private String taxIdentificationNumber; public Long getId(){return id;} public void setId(Long id){this.id=id;} }
