package com.grbroadcast.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.grbroadcast.entity.Message;

public interface MessageService extends IService<Message> {
    boolean replyMessage(Long id, String reply);
}