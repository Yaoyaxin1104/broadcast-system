package com.grbroadcast.utils;

import cn.hutool.jwt.JWT;
import cn.hutool.jwt.JWTUtil;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * JWT 工具类：签发令牌、校验令牌、解析用户 ID、读取有效期
 * 载荷只保留三项：userId、签发时间、过期时间
 */
@Component
public class JwtUtil {

    @Value("${jwt.secret}")
    private String secret;

    /** 令牌有效期（秒） */
    @Value("${jwt.expire}")
    private long expire;

    /** 签发令牌，载荷中只放用户 ID（Hutool 自动写入 iat；过期时间通过有效期校验） */
    public String create(Long userId) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("userId", userId);
        long now = System.currentTimeMillis();
        payload.put("iat", now / 1000);
        payload.put("exp", (now + expire * 1000) / 1000);
        return JWTUtil.createToken(payload, secret.getBytes(StandardCharsets.UTF_8));
    }

    /** 校验令牌签名与有效期 */
    public boolean verify(String token) {
        try {
            JWT jwt = JWT.of(token).setKey(secret.getBytes(StandardCharsets.UTF_8));
            if (!jwt.verify()) {
                return false;
            }
            Long exp = Long.valueOf(jwt.getPayload("exp").toString());
            return exp >= System.currentTimeMillis() / 1000;
        } catch (Exception e) {
            return false;
        }
    }

    /** 从令牌中解析用户 ID */
    public Long getUserId(String token) {
        Object userId = JWT.of(token).getPayload("userId");
        return Long.valueOf(userId.toString());
    }

    /** 读取令牌有效期秒数 */
    public long getExpire() {
        return expire;
    }
}
