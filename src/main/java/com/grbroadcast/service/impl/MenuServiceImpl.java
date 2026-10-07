package com.grbroadcast.service.impl;

import com.grbroadcast.dao.MenuMapper;
import com.grbroadcast.entity.Menu;
import com.grbroadcast.service.MenuService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
public class MenuServiceImpl implements MenuService {

    @Autowired
    private MenuMapper menuMapper;

    private static final List<String> ROLES = Arrays.asList("staff", "teacher", "student");

    @Override
    public List<Menu> listAll() {
        return menuMapper.selectList(null);
    }

    @Override
    public List<Menu> treeAll() {
        return buildTree(listAll());
    }

    @Override
    public List<Menu> treeByRole(String roleCode) {
        return buildTree(menuMapper.selectMenusByRole(roleCode));
    }

    @Override
    public List<Map<String, Object>> listRolesWithMenus() {
        List<Map<String, Object>> result = new ArrayList<>();
        for (String role : ROLES) {
            List<Menu> menus = menuMapper.selectMenusByRole(role);
            List<Long> ids = new ArrayList<>();
            for (Menu menu : menus) {
                ids.add(menu.getId());
            }
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("roleCode", role);
            item.put("menuIds", ids);
            result.add(item);
        }
        return result;
    }

    /**
     * 两次遍历 + 映射表构建菜单树：
     * 第一次遍历建立 id -> 菜单 映射并挂载子节点；
     * 第二次遍历收集根节点。
     * 不使用递归：构建过程为 O(n) 线性处理，避免递归深度限制与重复查找父节点，
     * 平铺结果集只需线性扫描即可完成父子挂载。
     */
    @Override
    public List<Menu> buildTree(List<Menu> menus) {
        // 第一次遍历：映射表 + 挂载子节点
        Map<Long, Menu> idMap = new HashMap<>();
        for (Menu menu : menus) {
            menu.setChildren(new ArrayList<>());
            idMap.put(menu.getId(), menu);
        }
        List<Menu> roots = new ArrayList<>();
        for (Menu menu : menus) {
            Long parentId = menu.getParentId();
            if (parentId != null && idMap.containsKey(parentId)) {
                idMap.get(parentId).getChildren().add(menu);
            } else {
                // 第二次（收集根节点，与挂载同遍历时即判定）
                roots.add(menu);
            }
        }
        return roots;
    }

    /**
     * 角色菜单授权：事务保护，先删后插；
     * 勾选子菜单时自动补全其全部父级目录
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void grantRoleMenus(String roleCode, List<Long> menuIds) {
        // 1. 先删除该角色的全部关联
        menuMapper.deleteRoleMenu(roleCode);
        if (menuIds == null || menuIds.isEmpty()) {
            return;
        }
        // 2. 建立全部菜单映射，用于回溯父级目录
        Map<Long, Menu> allMap = new HashMap<>();
        for (Menu menu : listAll()) {
            allMap.put(menu.getId(), menu);
        }
        // 3. 补全父级目录后去重
        Set<Long> toGrant = new HashSet<>(menuIds);
        for (Long menuId : menuIds) {
            Menu current = allMap.get(menuId);
            while (current != null && current.getParentId() != null
                    && current.getParentId() != 0L) {
                Menu parent = allMap.get(current.getParentId());
                if (parent == null) {
                    break;
                }
                toGrant.add(parent.getId());
                current = parent;
            }
        }
        // 4. 逐条插入
        for (Long menuId : toGrant) {
            menuMapper.insertRoleMenu(roleCode, menuId);
        }
    }
}
