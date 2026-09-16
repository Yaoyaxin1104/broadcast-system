package com.grbroadcast.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.grbroadcast.dao.MessageMapper;
import com.grbroadcast.entity.Message;
import com.grbroadcast.service.MessageService;
import org.springframework.stereotype.Service;

@Service
public class MessageServiceImpl extends ServiceImpl<MessageMapper, Message> implements MessageService {

    @Override
    public boolean replyMessage(Long id, String reply) {
        Message message = getById(id);
        if (message != null) {
            message.setReply(reply);
            return updateById(message);
        }
        return false;
    }
}