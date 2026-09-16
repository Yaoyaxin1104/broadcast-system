package com.grbroadcast.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;
@Data
@TableName("song_request")
public class SongRequest {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long studentId;
    private String songName;
    private String singer;
    private String message;
    private String status;
    private LocalDateTime auditTime;
    private LocalDateTime playTime;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    // 关联字段（非数据库字段）
    @TableField(exist = false)
    private String studentName;
    @TableField(exist = false)
    private String studentNo;
}