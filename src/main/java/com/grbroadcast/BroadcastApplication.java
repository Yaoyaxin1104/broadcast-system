package com.grbroadcast;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;  // ① 导入

@SpringBootApplication
@EnableScheduling  // ② 开启定时任务
@MapperScan("com.grbroadcast.dao")
public class BroadcastApplication {
    public static void main(String[] args) {
        SpringApplication.run(BroadcastApplication.class, args);
        System.out.println("==   广软广播站点歌投稿系统启动成功   ==");
        System.out.println("==   API地址: http://localhost:8089/api ==");

    }
}