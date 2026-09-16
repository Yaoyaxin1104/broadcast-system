package com.grbroadcast.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.grbroadcast.entity.User;

public interface UserService extends IService<User> {
    User login(String username, String password);
    User register(User user);
    User findByUsername(String username);
}
