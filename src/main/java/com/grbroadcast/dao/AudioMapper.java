package com.grbroadcast.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grbroadcast.entity.Audio;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface AudioMapper extends BaseMapper<Audio> {

    @Select("SELECT * FROM audio WHERE status = 1 ORDER BY create_time DESC")
    List<Audio> findOnline();
}