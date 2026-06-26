package com.facilcomanda.userservice.controller;
import com.facilcomanda.common.dto.*;
import com.facilcomanda.common.web.AuthContext;
import com.facilcomanda.userservice.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/users")
public class UserController {
 private final UserService service; public UserController(UserService service){this.service=service;}
 @PostMapping public ResponseEntity<UserResponse> createUser(@Valid @RequestBody UserRequest request, Authentication auth){return new ResponseEntity<>(service.createUser(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<UserResponse>> getAllUsers(Authentication auth){return ResponseEntity.ok(service.getAllUsers(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<UserResponse> getUserById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getUserById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<UserResponse> updateUser(@PathVariable Long id,@Valid @RequestBody UserRequest request, Authentication auth){return ResponseEntity.ok(service.updateUser(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteUser(@PathVariable Long id, Authentication auth){service.deleteUser(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
 @GetMapping("/internal/by-email/{email}") public UserSnapshot findByEmail(@PathVariable String email){ return service.findByEmail(email); }
}
