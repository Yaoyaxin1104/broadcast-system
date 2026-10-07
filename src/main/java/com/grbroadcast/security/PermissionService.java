package com.grbroadcast.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.Set;

/**
 * 权限判断服务，注册为名为 ss 的 Bean，
 * 路径级授权与方法级注解共用这一处判断逻辑
 */
@Service("ss")
public class PermissionService {

    private static final String ALL_PERMISSION = "*:*:*";

    /** 判断是否拥有指定权限 */
    public boolean hasPermi(String permission) {
        LoginUser loginUser = getLoginUser();
        if (loginUser == null || isEmpty(loginUser.getPermissions())) {
            return false;
        }
        if (loginUser.getPermissions().contains(ALL_PERMISSION)) {
            return true;
        }
        return loginUser.getPermissions().contains(permission);
    }

    /** 判断是否拥有任意一个权限 */
    public boolean hasAnyPermi(String[] permissions) {
        LoginUser loginUser = getLoginUser();
        if (loginUser == null || isEmpty(loginUser.getPermissions())) {
            return false;
        }
        if (loginUser.getPermissions().contains(ALL_PERMISSION)) {
            return true;
        }
        for (String permission : permissions) {
            if (loginUser.getPermissions().contains(permission)) {
                return true;
            }
        }
        return false;
    }

    /** 判断是否拥有指定角色 */
    public boolean hasRole(String role) {
        LoginUser loginUser = getLoginUser();
        return loginUser != null && !isEmpty(loginUser.getRoles())
                && loginUser.getRoles().contains(role);
    }

    /** 判断是否为超级管理员 */
    public boolean isAdmin() {
        LoginUser loginUser = getLoginUser();
        return loginUser != null && !isEmpty(loginUser.getPermissions())
                && loginUser.getPermissions().contains(ALL_PERMISSION);
    }

    private LoginUser getLoginUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated()) {
            return null;
        }
        Object principal = authentication.getPrincipal();
        return principal instanceof LoginUser ? (LoginUser) principal : null;
    }

    private boolean isEmpty(Set<?> set) {
        return set == null || set.isEmpty();
    }
}
