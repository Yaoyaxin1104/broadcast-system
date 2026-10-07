package com.grbroadcast.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * 菜单权限实体：目录 / 菜单 / 按钮
 */
@Data
@TableName("menu")
public class Menu {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String menuName;

    private Long parentId;

    /** M 目录 C 菜单 F 按钮 */
    private String menuType;

    private String path;

    private String component;

    /** 权限标识：模块:操作 */
    private String perms;

    private String icon;

    private Integer orderNum;

    private Integer visible;

    private Integer status;

    private LocalDateTime createTime;

    /** 子菜单（非数据库字段） */
    @TableField(exist = false)
    private List<Menu> children = new ArrayList<>();
}
