package com.facilcomanda.authservice.controller;
import com.facilcomanda.authservice.service.AuthService; import com.facilcomanda.common.dto.*; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.web.bind.annotation.*;
@RestController @RequestMapping("/api/auth")
public class AuthController {
 private final AuthService service; public AuthController(AuthService service){this.service=service;}
 @PostMapping("/login") public LoginResponse login(@Valid @RequestBody LoginRequest request){ return service.login(request); }
 @PostMapping("/register") public ResponseEntity<UserAuthDTO> register(@Valid @RequestBody RegisterRequest request){ return new ResponseEntity<>(service.register(request), HttpStatus.CREATED); }
}
