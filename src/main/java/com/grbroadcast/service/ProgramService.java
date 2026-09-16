package com.grbroadcast.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.grbroadcast.entity.ProgramSchedule;
import java.util.List;

public interface ProgramService extends IService<ProgramSchedule> {
    boolean publish(ProgramSchedule program);
    List<ProgramSchedule> getPublished();
}