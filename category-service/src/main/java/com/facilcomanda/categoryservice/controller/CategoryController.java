package com.facilcomanda.categoryservice.controller;
import com.facilcomanda.categoryservice.service.CategoryService; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.web.AuthContext; import jakarta.validation.Valid; import org.springframework.http.*; import org.springframework.security.core.Authentication; import org.springframework.web.bind.annotation.*; import java.util.List;
@RestController @RequestMapping("/api/categories") public class CategoryController { private final CategoryService service; public CategoryController(CategoryService service){this.service=service;}
 @PostMapping public ResponseEntity<CategoryResponse> createCategory(@Valid @RequestBody CategoryRequest request, Authentication auth){return new ResponseEntity<>(service.createCategory(request, AuthContext.organizationId(auth)), HttpStatus.CREATED);}
 @GetMapping public ResponseEntity<List<CategoryResponse>> getAllCategories(Authentication auth){return ResponseEntity.ok(service.getAllCategories(AuthContext.organizationId(auth)));}
 @GetMapping("/{id}") public ResponseEntity<CategoryResponse> getCategoryById(@PathVariable Long id, Authentication auth){return ResponseEntity.ok(service.getCategoryById(id, AuthContext.organizationId(auth)));}
 @PutMapping("/{id}") public ResponseEntity<CategoryResponse> updateCategory(@PathVariable Long id,@Valid @RequestBody CategoryRequest request, Authentication auth){return ResponseEntity.ok(service.updateCategory(id, request, AuthContext.organizationId(auth)));}
 @DeleteMapping("/{id}") public ResponseEntity<Void> deleteCategory(@PathVariable Long id, Authentication auth){service.deleteCategory(id, AuthContext.organizationId(auth)); return ResponseEntity.noContent().build();}
 @GetMapping("/internal/{id}") public CategoryResponse internalCategory(@PathVariable Long id, @RequestHeader("X-Organization-ID") Long org){ return service.getCategoryById(id, org); }
}
