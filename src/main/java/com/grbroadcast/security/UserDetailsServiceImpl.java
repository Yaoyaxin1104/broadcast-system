package com.grbroadcast.security;

import com.grbroadcast.dao.MenuMapper;
import com.grbroadcast.dao.UserMapper;
import com.grbroadcast.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

/**
 * 用户详情服务：按账号查询用户、角色与权限，装配为 LoginUser
 */
@Service
public class UserDetailsServiceImpl implements org.springframework.security.core.userdetails.UserDetailsService {

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private MenuMapper menuMapper;

    @Override
    public LoginUser loadUserByUsername(String username) {
        // 1. 按登录账号查询用户
        User user = userMapper.findByUsername(username);
        // 2. 判断账号是否存在
        if (user == null) {
            throw new UsernameNotFoundException("用户不存在");
        }
        // 3. 判断账号是否被禁用
        if (user.getStatus() == null || user.getStatus() != 1) {
            throw new DisabledException("账号已被禁用");
        }
        // 4. 查询角色编码集合
        Set<String> roles = new HashSet<>(Collections.singletonList(user.getRole()));
        // 5. 超级管理员放入通配符，否则按角色查询权限标识集合
        Set<String> permissions;
        if (roles.contains("admin")) {
            permissions = new HashSet<>(Collections.singletonList("*:*:*"));
        } else {
            permissions = menuMapper.selectPermsByRole(user.getRole());
            if (permissions == null) {
                permissions = new HashSet<>();
            }
        }
        // 6. 装配用户详情对象
        LoginUser loginUser = new LoginUser();
        loginUser.setUserId(user.getId());
        loginUser.setUsername(user.getUsername());
        loginUser.setPassword(user.getPassword());
        loginUser.setStatus(user.getStatus());
        loginUser.setRoles(roles);
        loginUser.setPermissions(permissions);
        return loginUser;
    }
}
