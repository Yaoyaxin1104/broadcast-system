package com.grbroadcast.service;

import com.grbroadcast.entity.Menu;

import java.util.List;
import java.util.Map;

public interface MenuService {

    /** 查询全部菜单（平铺） */
    List<Menu> listAll();

    /** 全部菜单树 */
    List<Menu> treeAll();

    /** 按角色查询菜单树 */
    List<Menu> treeByRole(String roleCode);

    /** 角色列表，每个角色携带其菜单ID集合 */
    List<Map<String, Object>> listRolesWithMenus();

    /** 角色菜单授权（先删后插，自动补全父级目录） */
    void grantRoleMenus(String roleCode, List<Long> menuIds);

    /** 两次遍历 + 映射表构建菜单树 */
    List<Menu> buildTree(List<Menu> menus);
}
