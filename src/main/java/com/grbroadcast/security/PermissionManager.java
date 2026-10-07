package com.grbroadcast.security;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.authorization.AuthorizationDecision;
import org.springframework.security.authorization.AuthorizationManager;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.access.intercept.RequestAuthorizationContext;
import org.springframework.stereotype.Component;

import java.util.function.Supplier;

/**
 * 自定义权限管理器：基于请求方法与路径解析所需权限标识并比对
 */
@Component
public class PermissionManager implements AuthorizationManager<RequestAuthorizationContext> {

    private static final Logger log = LoggerFactory.getLogger(PermissionManager.class);

    @Autowired
    private PermissionService permissionService;

    @Override
    public AuthorizationDecision check(Supplier<Authentication> authentication,
                                       RequestAuthorizationContext context) {
        // 1. 取出认证信息
        Authentication auth = authentication.get();
        // 2. 未认证或匿名用户，拒绝
        if (auth == null || !auth.isAuthenticated()
                || auth instanceof AnonymousAuthenticationToken) {
            return new AuthorizationDecision(false);
        }
        // 3. 超级管理员直接通过
        if (permissionService.isAdmin()) {
            return new AuthorizationDecision(true);
        }
        // 4. 解析请求所需权限标识
        String requiredPermission = resolvePermission(context);
        if (requiredPermission == null) {
            // 该路径没有配置权限要求，放行
            return new AuthorizationDecision(true);
        }
        boolean granted = permissionService.hasPermi(requiredPermission);
        if (!granted) {
            log.warn("授权失败：用户[{}]访问[{} {}]，缺少权限[{}]",
                    auth.getName(), context.getRequest().getMethod(),
                    context.getRequest().getRequestURI(), requiredPermission);
        }
        return new AuthorizationDecision(granted);
    }

    /**
     * 路径与权限对应关系，集中在一处维护
     */
    private String resolvePermission(RequestAuthorizationContext context) {
        String method = context.getRequest().getMethod();
        String uri = context.getRequest().getRequestURI();
        // 去掉上下文路径
        String path = uri.replace("/api", "");
        if ("GET".equals(method) && path.equals("/song/pending")) {
            return "song:audit";
        }
        if ("GET".equals(method) && path.equals("/article/pending")) {
            return "article:audit";
        }
        if ("POST".equals(method) && path.equals("/audio/upload")) {
            return "audio:upload";
        }
        if ("DELETE".equals(method) && path.startsWith("/audio/delete")) {
            return "audio:delete";
        }
        if ("PUT".equals(method) && path.startsWith("/message/reply")) {
            return "message:reply";
        }
        if ("POST".equals(method) && path.equals("/program/publish")) {
            return "program:publish";
        }
        if ("PUT".equals(method) && path.equals("/program/update")) {
            return "program:edit";
        }
        if ("DELETE".equals(method) && path.startsWith("/program/delete")) {
            return "program:delete";
        }
        if ("GET".equals(method) && path.startsWith("/menu")) {
            return "menu:list";
        }
        // 其余路径无专门权限要求
        return null;
    }
}
