package com.grbroadcast.controller;

import com.grbroadcast.common.Result;
import com.grbroadcast.service.MenuService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 菜单与角色授权接口
 */
@RestController
@RequestMapping("/menu")
public class MenuController {

    @Autowired
    private MenuService menuService;

    /** 全部菜单（平铺） */
    @GetMapping("/list")
    @PreAuthorize("@ss.hasPermi('menu:list')")
    public Result list() {
        return Result.success(menuService.listAll());
    }

    /** 全部菜单树 */
    @GetMapping("/tree")
    @PreAuthorize("@ss.hasPermi('menu:list')")
    public Result tree() {
        return Result.success(menuService.treeAll());
    }

    /** 角色列表，携带各自菜单ID */
    @GetMapping("/roles")
    @PreAuthorize("@ss.hasPermi('menu:list')")
    public Result roles() {
        return Result.success(menuService.listRolesWithMenus());
    }

    /** 查询指定角色的菜单树 */
    @GetMapping("/role/{roleCode}")
    @PreAuthorize("@ss.hasPermi('menu:list')")
    public Result roleMenus(@PathVariable String roleCode) {
        return Result.success(menuService.treeByRole(roleCode));
    }

    /** 给指定角色授权菜单（先删后插、事务保护、父级目录补全） */
    @PutMapping("/role/{roleCode}")
    @PreAuthorize("@ss.hasPermi('menu:grant')")
    public Result grant(@PathVariable String roleCode,
                        @RequestBody Map<String, List<Long>> body) {
        menuService.grantRoleMenus(roleCode, body.get("menuIds"));
        return Result.success("授权成功");
    }
}
