package com.facilcomanda.userservice.repository;
import com.facilcomanda.userservice.entity.Role;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
public interface RoleRepository extends JpaRepository<Role, Long> { Optional<Role> findByIdAndOrganizationId(Long id, Long organizationId); List<Role> findByOrganizationId(Long organizationId); }
