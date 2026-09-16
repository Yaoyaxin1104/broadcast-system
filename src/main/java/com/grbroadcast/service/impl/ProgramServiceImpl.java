package com.grbroadcast.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.grbroadcast.dao.ProgramScheduleMapper;
import com.grbroadcast.entity.ProgramSchedule;
import com.grbroadcast.service.ProgramService;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class ProgramServiceImpl extends ServiceImpl<ProgramScheduleMapper, ProgramSchedule> implements ProgramService {

    @Override
    public boolean publish(ProgramSchedule program) {
        program.setStatus("published");
        program.setPublishTime(LocalDateTime.now());
        program.setCreateTime(LocalDateTime.now());
        return save(program);
    }

    @Override
    public List<ProgramSchedule> getPublished() {
        return baseMapper.findPublished();
    }
}