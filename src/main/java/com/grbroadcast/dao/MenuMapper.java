package com.grbroadcast.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grbroadcast.entity.Menu;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.Set;

@Mapper
public interface MenuMapper extends BaseMapper<Menu> {

    /** 按角色查询其拥有的菜单（目录/菜单/按钮） */
    @Select("SELECT DISTINCT m.* FROM menu m "
            + "JOIN role_menu rm ON m.id = rm.menu_id "
            + "WHERE rm.role_code = #{roleCode} AND m.status = 1 "
            + "ORDER BY m.parent_id, m.order_num")
    java.util.List<Menu> selectMenusByRole(String roleCode);

    /** 按角色查询权限标识集合 */
    @Select("SELECT DISTINCT m.perms FROM menu m "
            + "JOIN role_menu rm ON m.id = rm.menu_id "
            + "WHERE rm.role_code = #{roleCode} AND m.status = 1 "
            + "AND m.perms IS NOT NULL AND m.perms <> ''")
    Set<String> selectPermsByRole(String roleCode);

    /** 删除某角色的全部菜单关联 */
    @Delete("DELETE FROM role_menu WHERE role_code = #{roleCode}")
    int deleteRoleMenu(String roleCode);

    /** 插入一条角色菜单关联 */
    @Insert("INSERT INTO role_menu(role_code, menu_id) VALUES(#{roleCode}, #{menuId})")
    int insertRoleMenu(@Param("roleCode") String roleCode, @Param("menuId") Long menuId);
}
