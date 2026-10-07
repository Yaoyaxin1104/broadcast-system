package com.grbroadcast.security;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.alibaba.fastjson.annotation.JSONField;
import lombok.Data;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.HashSet;
import java.util.Set;

/**
 * 登录用户详情模型（同时作为 Redis 缓存对象，必须提供无参构造方法）
 */
@Data
public class LoginUser implements UserDetails {

    private static final long serialVersionUID = 1L;

    /** 用户 ID */
    private Long userId;

    /** 登录账号 */
    private String username;

    /** 密码（BCrypt 密文） */
    private String password;

    /** 账号状态：0 禁用 1 启用 */
    private Integer status;

    /** 角色编码集合 */
    private Set<String> roles = new HashSet<>();

    /** 权限标识集合 */
    private Set<String> permissions = new HashSet<>();

    public LoginUser() {
    }

    @JsonIgnore
    @JSONField(serialize = false)
    @Override
    public Set<GrantedAuthority> getAuthorities() {
        Set<GrantedAuthority> authorities = new HashSet<>();
        for (String role : roles) {
            authorities.add(new SimpleGrantedAuthority("ROLE_" + role));
        }
        for (String permission : permissions) {
            authorities.add(new SimpleGrantedAuthority(permission));
        }
        return authorities;
    }

    @JsonIgnore
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @JsonIgnore
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @JsonIgnore
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @JsonIgnore
    @Override
    public boolean isEnabled() {
        return status != null && status == 1;
    }
}
