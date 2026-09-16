package com.grbroadcast.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.grbroadcast.entity.SongRequest;
import java.util.List;
import java.util.Map;

public interface SongService extends IService<SongRequest> {

    boolean addSong(SongRequest songRequest);
    boolean deleteSong(Long id);
    boolean auditSong(Long id, String status);
    List<Map<String, Object>> getAllWithStudent();
    Map<String, Object> getSongDetail(Long id);
}