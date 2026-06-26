package com.facilcomanda.userservice.repository;
import com.facilcomanda.userservice.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.*;
public interface UserRepository extends JpaRepository<User, Long> {
 Optional<User> findByEmail(String email); Optional<User> findByIdAndOrganizationId(Long id, Long organizationId); List<User> findByOrganizationId(Long organizationId);
}
