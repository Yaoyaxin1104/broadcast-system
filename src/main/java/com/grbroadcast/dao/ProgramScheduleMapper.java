package com.grbroadcast.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grbroadcast.entity.ProgramSchedule;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface ProgramScheduleMapper extends BaseMapper<ProgramSchedule> {

    @Select("SELECT * FROM program_schedule WHERE status = 'published' ORDER BY date DESC")
    List<ProgramSchedule> findPublished();
}