package com.grbroadcast.controller;

import com.grbroadcast.common.Result;
import com.grbroadcast.entity.User;
import com.grbroadcast.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpSession;

@CrossOrigin(origins = "*", allowCredentials = "false")
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    // ========== 注册 ==========
    @PostMapping("/register")
    public Result register(@RequestBody User user) {
        if (userService.findByUsername(user.getUsername()) != null) {
            return Result.error("用户名已存在");
        }
        userService.register(user);
        return Result.success("注册成功");
    }
    // ========== 登录 ==========
    @PostMapping("/login")
    public Result login(@RequestBody User user, HttpSession session) {
        User loginUser = userService.login(user.getUsername(), user.getPassword());
        if (loginUser != null) {
            session.setAttribute("user", loginUser);
            return Result.success(loginUser);
        }
        return Result.error("用户名或密码错误");
    }

    // ========== 获取当前用户信息 ==========
    @GetMapping("/info")
    public Result getUserInfo(HttpSession session) {
        User user = (User) session.getAttribute("user");
        return user == null ? Result.error("未登录") : Result.success(user);
    }

    // ========== 退出登录 ==========
    @PostMapping("/logout")
    public Result logout(HttpSession session) {
        session.removeAttribute("user");
        return Result.success("退出成功");
    }
}