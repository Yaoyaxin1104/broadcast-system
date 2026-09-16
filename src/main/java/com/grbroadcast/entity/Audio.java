package com.grbroadcast.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("audio")
public class Audio {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long staffId;
    private String title;
    private String filePath;
    private Long fileSize;
    private Integer duration;
    private Integer playCount;
    private Integer status;
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
}