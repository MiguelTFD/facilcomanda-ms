package com.facilcomanda.userservice.service;
import com.facilcomanda.common.dto.*;
import com.facilcomanda.common.enums.RoleName;
import com.facilcomanda.common.event.EventPublisher;
import com.facilcomanda.userservice.entity.*;
import com.facilcomanda.userservice.repository.*;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import java.util.List;
@Service
public class UserService {
 private final UserRepository users; private final RoleRepository roles; private final PasswordEncoder encoder; private final EventPublisher publisher;
 public UserService(UserRepository users, RoleRepository roles, PasswordEncoder encoder, EventPublisher publisher){this.users=users;this.roles=roles;this.encoder=encoder;this.publisher=publisher;}
 public UserResponse createUser(UserRequest request, Long organizationId){ if(request.password()==null||request.password().isBlank()) throw new IllegalArgumentException("Password is required for user creation"); User user=new User(); user.setOrganizationId(organizationId); user.setPassword(encoder.encode(request.password())); map(request,user,organizationId); User saved=users.save(user); UserResponse response=toResponse(saved); audit("CREATE", saved.getId(), null, response); return response; }
 public List<UserResponse> getAllUsers(Long organizationId){ return users.findByOrganizationId(organizationId).stream().map(this::toResponse).toList(); }
 public UserResponse getUserById(Long id, Long organizationId){ return toResponse(fetch(id,organizationId)); }
 public UserResponse updateUser(Long id, UserRequest request, Long organizationId){ User user=fetch(id,organizationId); UserResponse old=toResponse(user); if(request.password()!=null&&!request.password().isBlank()) user.setPassword(encoder.encode(request.password())); map(request,user,organizationId); User saved=users.save(user); UserResponse response=toResponse(saved); audit("UPDATE", id, old, response); return response; }
 public void deleteUser(Long id, Long organizationId){ User user=fetch(id,organizationId); UserResponse old=toResponse(user); users.delete(user); audit("DELETE", id, old, null); }
 public UserSnapshot findByEmail(String email){ return users.findByEmail(email).map(u -> new UserSnapshot(u.getId(), u.getEmail(), u.getFirstName(), u.getLastName(), u.getRole().getName().name(), u.getOrganizationId())).orElseThrow(() -> new RuntimeException("User not found")); }
 private void map(UserRequest request, User user, Long organizationId){ user.setEmail(request.email()); user.setFirstName(request.firstName()); user.setLastName(request.lastName()); Role role=roles.findByIdAndOrganizationId(request.roleId(), organizationId).orElseThrow(() -> new RuntimeException("Role not found or unauthorized")); user.setRole(role); }
 private User fetch(Long id, Long org){ return users.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("User not found or unauthorized")); }
 private UserResponse toResponse(User u){ return new UserResponse(u.getId(), u.getEmail(), u.getFirstName(), u.getLastName(), u.getRole()!=null?u.getRole().getName().name():null, u.getOrganizationId()); }
 private void audit(String op,Object id,Object old,Object val){ publisher.publishAudit("user-service","User",id,op,old,val,null,null,null,null); }
 public RoleResponse createRole(RoleRequest request, Long org){ Role r=new Role(); r.setOrganizationId(org); r.setName(RoleName.valueOf(request.name().toUpperCase())); r.setDescription(request.description()); Role saved=roles.save(r); RoleResponse res=toRole(saved); audit("CREATE", saved.getId(), null, res); return res; }
 public List<RoleResponse> getAllRoles(Long org){ return roles.findByOrganizationId(org).stream().map(this::toRole).toList(); }
 public RoleResponse getRoleById(Long id, Long org){ return toRole(fetchRole(id,org)); }
 public RoleResponse updateRole(Long id, RoleRequest request, Long org){ Role r=fetchRole(id,org); RoleResponse old=toRole(r); r.setName(RoleName.valueOf(request.name().toUpperCase())); r.setDescription(request.description()); RoleResponse res=toRole(roles.save(r)); audit("UPDATE", id, old, res); return res; }
 public void deleteRole(Long id, Long org){ Role r=fetchRole(id,org); RoleResponse old=toRole(r); roles.delete(r); audit("DELETE", id, old, null); }
 private Role fetchRole(Long id, Long org){ return roles.findByIdAndOrganizationId(id,org).orElseThrow(() -> new RuntimeException("Role not found or unauthorized")); }
 private RoleResponse toRole(Role r){ return new RoleResponse(r.getId(), r.getName().name(), r.getDescription(), r.getOrganizationId()); }
}
