package com.grbroadcast.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.grbroadcast.common.Result;
import com.grbroadcast.entity.SongRequest;
import com.grbroadcast.entity.User;
import com.grbroadcast.service.SongService;
import com.grbroadcast.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*", allowCredentials = "false")
@RestController
@RequestMapping("/song")
public class SongController {

    @Autowired
    private SongService songService;

    @Autowired
    private UserService userService;

    // ========== 学生端 - 新增点歌 ==========
    @PostMapping("/add")
    @PreAuthorize("@ss.hasPermi('song:add')")
    public Result addSong(@RequestBody SongRequest songRequest, @RequestParam Long userId) {
        User user = userService.getById(userId);
        if (user == null || !"student".equals(user.getRole())) {
            return Result.error("请先登录学生账号");
        }
        songRequest.setStudentId(user.getId());
        //调用service处理业务
        return songService.addSong(songRequest) ? Result.success("提交成功") : Result.error("提交失败");
    }
    // ========== 学生端 - 查询我的点歌 ==========
    @GetMapping("/my")
    public Result getMySongs(@RequestParam Long userId) {
        User user = userService.getById(userId);
        if (user == null) {
            return Result.error("未登录");
        }
        return Result.success(songService.lambdaQuery().eq(SongRequest::getStudentId, user.getId()).list());
    }

    // ========== 管理端 - 查询所有点歌 ==========
    @GetMapping("/list")
    public Result listAll() {
        return Result.success(songService.getAllWithStudent());
    }

    // ========== 管理端 - 查询点歌详情 ==========
    @GetMapping("/detail/{id}")
    public Result getDetail(@PathVariable Long id) {
        return Result.success(songService.getSongDetail(id));
    }

    // ========== 管理端 - 查询待审核点歌 ==========
    @GetMapping("/pending")
    @PreAuthorize("@ss.hasPermi('song:audit')")
    public Result getPending() {
        return Result.success(songService.lambdaQuery()
                .eq(SongRequest::getStatus, "pending").list());
    }

    // ========== 管理端 - 审核点歌 ==========
    @PutMapping("/audit/{id}")
    @PreAuthorize("@ss.hasPermi('song:audit')")
    public Result auditSong(@PathVariable Long id,
                            @RequestParam String status,
                            @RequestParam Long userId) {
        User user = userService.getById(userId);
        if (user == null || !"staff".equals(user.getRole())) {
            return Result.error("无权限，需要广播站成员身份");
        }
        //调用service处理业务
        return songService.auditSong(id, status) ? Result.success("审核完成") : Result.error("审核失败");
    }

    // ========== 管理端 - 删除点歌 ==========
    @DeleteMapping("/delete/{id}")
    @PreAuthorize("@ss.hasPermi('song:delete')")
    public Result deleteSong(@PathVariable Long id) {
        return songService.deleteSong(id) ? Result.success("删除成功") : Result.error("删除失败");
    }

    // ========== 修改点歌 ==========
    @PutMapping("/update")
    @PreAuthorize("@ss.hasPermi('song:edit')")
    public Result updateSong(@RequestBody SongRequest songRequest) {
        return songService.updateById(songRequest) ? Result.success("修改成功") : Result.error("修改失败");
    }
    // ========== 搜索点歌 ==========
    @GetMapping("/search")
    public Result searchSongs(@RequestParam(required = false) String keyword,
                              @RequestParam(required = false) String status) {
        LambdaQueryWrapper<SongRequest> wrapper = new LambdaQueryWrapper<>();
        if (keyword != null && !keyword.isEmpty()) {
            wrapper.and(w -> w
                    .like(SongRequest::getSongName, keyword)
                    .or()
                    .like(SongRequest::getSinger, keyword)
            );
        }
        if (status != null && !status.isEmpty()) {
            wrapper.eq(SongRequest::getStatus, status);
        }
        wrapper.orderByDesc(SongRequest::getCreateTime);
        return Result.success(songService.list(wrapper));
    }


}