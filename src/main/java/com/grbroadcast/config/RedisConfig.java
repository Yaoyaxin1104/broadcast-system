package com.grbroadcast.config;

import com.alibaba.fastjson.parser.ParserConfig;
import com.alibaba.fastjson.support.spring.GenericFastJsonRedisSerializer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.StringRedisSerializer;

/**
 * Redis 配置：键使用字符串序列化器，值使用 fastjson 序列化器
 * （序列化时写入类型信息，并配置可信包白名单）
 */
@Configuration
public class RedisConfig {

    static {
        // 可信包白名单：仅允许反序列化本项目包中的类
        ParserConfig.getGlobalInstance().addAccept("com.grbroadcast.");
    }

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        // 值序列化器：写入 @type 类型信息（白名单在静态块中配置）
        GenericFastJsonRedisSerializer jsonSerializer = new GenericFastJsonRedisSerializer();

        template.setKeySerializer(stringSerializer);
        template.setHashKeySerializer(stringSerializer);
        template.setValueSerializer(jsonSerializer);
        template.setHashValueSerializer(jsonSerializer);
        template.afterPropertiesSet();
        return template;
    }
}
