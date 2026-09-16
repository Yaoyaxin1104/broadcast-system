package com.grbroadcast.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("program_schedule")
public class ProgramSchedule {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long staffId;
    private LocalDate date;
    private String timeSlot;
    private String programName;
    private String content;
    private String songs;
    private String status;
    private LocalDateTime publishTime;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
}