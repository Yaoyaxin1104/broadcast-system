package com.grbroadcast.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.grbroadcast.entity.Audio;
import java.util.List;

public interface AudioService extends IService<Audio> {
    List<Audio> getOnlineList();
}