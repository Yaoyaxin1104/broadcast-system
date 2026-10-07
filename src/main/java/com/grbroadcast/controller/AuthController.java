package com.grbroadcast.controller;

import com.grbroadcast.common.Result;
import com.grbroadcast.security.LoginUser;
import com.grbroadcast.utils.JwtUtil;
import com.grbroadcast.utils.RedisUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 认证控制器：登录（签发 JWT）、退出（删除缓存）、当前用户信息
 */
@RestController
@RequestMapping("/auth")
public class AuthController {

    private static final String CACHE_PREFIX = "login:user:";

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private RedisUtil redisUtil;

    @Autowired
    private JwtUtil jwtUtil;

    /** 登录 */
    @PostMapping("/login")
    public Result login(@RequestBody Map<String, String> body) {
        String username = body.get("username");
        String password = body.get("password");
        // 1. 基本格式校验
        if (!StringUtils.hasText(username) || !StringUtils.hasText(password)) {
            return Result.error("请输入账号和密码");
        }
        // 2/3. 构造认证请求并交由认证管理器完成认证
        Authentication authentication;
        try {
            authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(username, password));
        } catch (AuthenticationException e) {
            // 统一提示，避免通过提示差异探测账号
            return Result.error("账号或密码错误");
        }
        // 4. 取出已装配角色与权限的用户详情
        LoginUser loginUser = (LoginUser) authentication.getPrincipal();
        // 5. 以用户 ID 为键写入 Redis，过期时间与令牌有效期一致
        redisUtil.set(CACHE_PREFIX + loginUser.getUserId(), loginUser, jwtUtil.getExpire());
        // 6. 签发令牌，载荷中只放用户 ID
        String token = jwtUtil.create(loginUser.getUserId());
        // 7. 组装响应
        Map<String, Object> info = new HashMap<>();
        info.put("token", token);
        info.put("expire", jwtUtil.getExpire());
        Map<String, Object> userInfo = new HashMap<>();
        userInfo.put("userId", loginUser.getUserId());
        userInfo.put("username", loginUser.getUsername());
        userInfo.put("roles", loginUser.getRoles());
        userInfo.put("permissions", loginUser.getPermissions());
        info.put("user", userInfo);
        return Result.success("登录成功", info);
    }

    /** 退出登录：删除 Redis 缓存并清空安全上下文 */
    @PostMapping("/logout")
    public Result logout() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null && authentication.getPrincipal() instanceof LoginUser) {
            LoginUser loginUser = (LoginUser) authentication.getPrincipal();
            redisUtil.delete(CACHE_PREFIX + loginUser.getUserId());
        }
        SecurityContextHolder.clearContext();
        return Result.success("退出成功");
    }

    /** 获取当前登录用户信息 */
    @GetMapping("/info")
    public Result info() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !(authentication.getPrincipal() instanceof LoginUser)) {
            return Result.error(401, "未登录");
        }
        LoginUser loginUser = (LoginUser) authentication.getPrincipal();
        Map<String, Object> userInfo = new HashMap<>();
        userInfo.put("userId", loginUser.getUserId());
        userInfo.put("username", loginUser.getUsername());
        List<String> perms = new ArrayList<>(loginUser.getPermissions());
        userInfo.put("permissions", perms);
        return Result.success(userInfo);
    }
}
