package com.grbroadcast.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grbroadcast.entity.Message;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface MessageMapper extends BaseMapper<Message> {
}