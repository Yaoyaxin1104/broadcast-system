package com.grbroadcast.utils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

import java.util.concurrent.TimeUnit;

/**
 * 缓存操作工具类：写入（带过期时间）、读取、删除、续期
 */
@Component
public class RedisUtil {

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    /** 按键写入并设置过期时间（秒） */
    public void set(String key, Object value, long timeout) {
        redisTemplate.opsForValue().set(key, value, timeout, TimeUnit.SECONDS);
    }

    /** 按键读取 */
    public Object get(String key) {
        return redisTemplate.opsForValue().get(key);
    }

    /** 按键删除 */
    public Boolean delete(String key) {
        return redisTemplate.delete(key);
    }

    /** 为已存在的键续期（秒） */
    public Boolean expire(String key, long timeout) {
        return redisTemplate.expire(key, timeout, TimeUnit.SECONDS);
    }
}
