package com.grbroadcast;

import com.grbroadcast.entity.User;
import com.grbroadcast.service.UserService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class UserServiceTest {
    @Autowired
    private UserService userService;
    @Test
    public void testRegister() {
        User user = new User();
        user.setUsername("test001");
        user.setPassword("123456");
        user.setRealName("测试用户");
        user.setRole("student");
        User result = userService.register(user);
        System.out.println("注册结果: " + (result != null ? "成功" : "失败"));
        assert result != null;
    }
    @Test
    public void testLogin() {
        User user = userService.login("student1", "123456");
        System.out.println("登录结果: " + (user != null ? "成功 - " + user.getRealName() : "失败"));
        assert user != null;
    }
    @Test
    public void testFindByUsername() {
        User user = userService.findByUsername("student1");
        System.out.println("查询结果: " + (user != null ? user.getRealName() : "未找到"));
        assert user != null;
    }
}