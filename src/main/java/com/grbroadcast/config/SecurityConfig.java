package com.grbroadcast.config;

import com.grbroadcast.security.AccessDeniedHandlerImpl;
import com.grbroadcast.security.AuthenticationEntryPointImpl;
import com.grbroadcast.security.JwtAuthenticationTokenFilter;
import com.grbroadcast.security.PermissionManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

/**
 * Spring Security 安全配置（Spring Boot 2.7 / Security 5.7）
 */
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig {

    /** 白名单路径 */
    private static final String[] WHITELIST = {
            "/auth/login", "/user/register", "/error"
    };

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration configuration)
            throws Exception {
        return configuration.getAuthenticationManager();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.addAllowedOriginPattern("*");
        configuration.addAllowedHeader("*");
        configuration.addAllowedMethod("*");
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http,
                                           JwtAuthenticationTokenFilter jwtAuthenticationTokenFilter,
                                           AuthenticationEntryPointImpl authenticationEntryPoint,
                                           AccessDeniedHandlerImpl accessDeniedHandler,
                                           PermissionManager permissionManager) throws Exception {
        http
                // 关闭 CSRF：前后端分离使用令牌认证
                .csrf().disable()
                // 跨域交由安全框架统一处理
                .cors().configurationSource(corsConfigurationSource())
                .and()
                // 关闭表单登录与 HTTP 基础认证
                .formLogin().disable()
                .httpBasic().disable()
                // 关闭框架自带退出接口，自行实现退出逻辑
                .logout().disable()
                // 不创建 HttpSession，无状态
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                // 401 与 403 分流处理
                .exceptionHandling()
                .authenticationEntryPoint(authenticationEntryPoint)
                .accessDeniedHandler(accessDeniedHandler)
                .and()
                .authorizeHttpRequests(auth -> auth
                        // 预检请求放行
                        .antMatchers(org.springframework.http.HttpMethod.OPTIONS, "/**").permitAll()
                        // 白名单放行
                        .antMatchers(WHITELIST).permitAll()
                        // 管理类路径走自定义权限管理器
                        .antMatchers("/song/pending", "/article/pending",
                                "/audio/upload", "/audio/delete/**",
                                "/message/reply/**",
                                "/program/publish", "/program/update", "/program/delete/**",
                                "/menu/**")
                        .access(permissionManager)
                        // 其余请求要求已认证
                        .anyRequest().authenticated())
                // JWT 过滤器置于用户名密码认证过滤器之前
                .addFilterBefore(jwtAuthenticationTokenFilter,
                        UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
}
