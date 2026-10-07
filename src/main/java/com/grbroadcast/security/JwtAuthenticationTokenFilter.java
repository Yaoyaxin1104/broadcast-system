package com.grbroadcast.security;

import com.grbroadcast.utils.JwtUtil;
import com.grbroadcast.utils.RedisUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * JWT 认证过滤器：解析令牌 -> 从 Redis 取回用户详情 -> 写入安全上下文
 */
@Component
public class JwtAuthenticationTokenFilter extends OncePerRequestFilter {

    private static final String CACHE_PREFIX = "login:user:";

    @Autowired
    private RedisUtil redisUtil;

    @Autowired
    private JwtUtil jwtUtil;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        // 1. 从请求头取出令牌（兼容带 Bearer 前缀与不带前缀）
        String token = request.getHeader("Authorization");
        if (StringUtils.hasText(token) && token.startsWith("Bearer ")) {
            token = token.substring(7);
        }
        // 2. 无令牌直接放行，交由授权环节统一处理
        if (!StringUtils.hasText(token)) {
            chain.doFilter(request, response);
            return;
        }
        // 3. 校验令牌签名与有效期
        if (!jwtUtil.verify(token)) {
            chain.doFilter(request, response);
            return;
        }
        // 4. 解析用户 ID
        Long userId = jwtUtil.getUserId(token);
        // 5. 从 Redis 取回用户详情
        LoginUser loginUser = (LoginUser) redisUtil.get(CACHE_PREFIX + userId);
        // 6. 缓存中不存在则放行
        if (loginUser == null) {
            chain.doFilter(request, response);
            return;
        }
        // 7. 二次校验账号状态
        if (!loginUser.isEnabled()) {
            chain.doFilter(request, response);
            return;
        }
        // 8. 上下文为空或为匿名身份时，构造已认证对象写入安全上下文
        org.springframework.security.core.Authentication existing =
                SecurityContextHolder.getContext().getAuthentication();
        if (existing != null && !(existing instanceof AnonymousAuthenticationToken)) {
            chain.doFilter(request, response);
            return;
        }
        UsernamePasswordAuthenticationToken authentication =
                new UsernamePasswordAuthenticationToken(loginUser, null, loginUser.getAuthorities());
        authentication.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
        SecurityContextHolder.getContext().setAuthentication(authentication);
        chain.doFilter(request, response);
    }
}
