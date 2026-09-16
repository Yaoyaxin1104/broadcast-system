package com.grbroadcast.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.grbroadcast.dao.AudioMapper;
import com.grbroadcast.entity.Audio;
import com.grbroadcast.service.AudioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class AudioServiceImpl extends ServiceImpl<AudioMapper, Audio> implements AudioService {

    @Autowired
    private AudioMapper audioMapper;

    @Override
    public List<Audio> getOnlineList() {
        return audioMapper.findOnline();
    }
}