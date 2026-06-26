package com.facilcomanda.categoryservice.service;
import com.facilcomanda.categoryservice.entity.Category; import com.facilcomanda.categoryservice.repository.CategoryRepository; import com.facilcomanda.common.dto.*; import com.facilcomanda.common.event.EventPublisher; import org.springframework.stereotype.Service; import java.util.List;
@Service public class CategoryService { private final CategoryRepository repo; private final EventPublisher publisher; public CategoryService(CategoryRepository repo, EventPublisher publisher){this.repo=repo;this.publisher=publisher;}
 public CategoryResponse createCategory(CategoryRequest request, Long org){ Category c=new Category(); c.setOrganizationId(org); map(request,c,org); Category saved=repo.save(c); CategoryResponse res=toResponse(saved); audit("CREATE", saved.getId(), null, res); return res; }
 public List<CategoryResponse> getAllCategories(Long org){return repo.findByOrganizationId(org).stream().map(this::toResponse).toList();}
 public CategoryResponse getCategoryById(Long id, Long org){return toResponse(fetch(id,org));}
 public CategoryResponse updateCategory(Long id, CategoryRequest request, Long org){Category c=fetch(id,org); CategoryResponse old=toResponse(c); map(request,c,org); CategoryResponse res=toResponse(repo.save(c)); audit("UPDATE", id, old, res); return res;}
 public void deleteCategory(Long id, Long org){Category c=fetch(id,org); CategoryResponse old=toResponse(c); repo.delete(c); audit("DELETE", id, old, null);}
 private Category fetch(Long id,Long org){return repo.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("Category not found or unauthorized"));}
 private void map(CategoryRequest r, Category c, Long org){c.setName(r.name()); c.setDescription(r.description()); c.setParentCategory(r.parentCategoryId()==null?null:fetch(r.parentCategoryId(), org));}
 private CategoryResponse toResponse(Category c){return new CategoryResponse(c.getId(), c.getName(), c.getDescription(), c.getParentCategory()!=null?c.getParentCategory().getId():null);}
 private void audit(String op,Object id,Object old,Object val){publisher.publishAudit("category-service","Category",id,op,old,val,null,null,null,null);}
}
