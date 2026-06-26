package com.facilcomanda.userservice.controller;
import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import com.facilcomanda.userservice.service.UserService;
import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/roles")
public class RoleController {
 private final UserService service; public RoleController(UserService service){this.service=service;}
 @PostMapping public ResponseEntity<RoleResponse> createRole(@Valid @RequestBody RoleRequest request, Authentication auth){return new ResponseEntity<>(service.createRole(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<RoleResponse>> getAllRoles(Authentication auth){return ResponseEntity.ok(service.getAllRoles(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<RoleResponse> getRoleById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getRoleById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<RoleResponse> updateRole(@PathVariable Long id,@Valid @RequestBody RoleRequest request, Authentication auth){return ResponseEntity.ok(service.updateRole(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteRole(@PathVariable Long id, Authentication auth){service.deleteRole(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
}
