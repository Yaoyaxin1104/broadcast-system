package com.grbroadcast.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.grbroadcast.dao.SongRequestMapper;
import com.grbroadcast.entity.SongRequest;
import com.grbroadcast.service.SongService;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class SongServiceImpl extends ServiceImpl<SongRequestMapper, SongRequest> implements SongService {

    @Override
    public boolean addSong(SongRequest songRequest) {
        songRequest.setStatus("pending");
        songRequest.setCreateTime(LocalDateTime.now());
        return save(songRequest);
    }

    @Override
    public boolean deleteSong(Long id) {
        return removeById(id);
    }

    @Override
    public boolean auditSong(Long id, String status) {
        SongRequest song = getById(id);
        if (song != null) {
            song.setStatus(status);
            song.setAuditTime(LocalDateTime.now());
            return updateById(song);
        }
        return false;
    }

    @Override
    public List<Map<String, Object>> getAllWithStudent() {
        List<SongRequest> songs = list();
        List<Map<String, Object>> result = new ArrayList<>();

        for (SongRequest song : songs) {
            Map<String, Object> map = new HashMap<>();
            map.put("id", song.getId());
            map.put("student_id", song.getStudentId());
            map.put("song_name", song.getSongName());
            map.put("singer", song.getSinger());
            map.put("message", song.getMessage());
            map.put("status", song.getStatus());
            map.put("create_time", song.getCreateTime());
            map.put("student_name", "学生ID:" + song.getStudentId());
            result.add(map);
        }
        return result;
    }

    @Override
    public Map<String, Object> getSongDetail(Long id) {
        SongRequest song = getById(id);
        if (song == null) return null;

        Map<String, Object> map = new HashMap<>();
        map.put("id", song.getId());
        map.put("student_id", song.getStudentId());
        map.put("song_name", song.getSongName());
        map.put("singer", song.getSinger());
        map.put("message", song.getMessage());
        map.put("status", song.getStatus());
        map.put("create_time", song.getCreateTime());
        map.put("audit_time", song.getAuditTime());
        return map;
    }
}