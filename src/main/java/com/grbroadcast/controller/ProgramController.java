package com.grbroadcast.controller;

import com.grbroadcast.common.Result;
import com.grbroadcast.entity.ProgramSchedule;
import com.grbroadcast.entity.User;
import com.grbroadcast.service.ProgramService;
import com.grbroadcast.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;

@CrossOrigin(origins = "*", allowCredentials = "false")
@RestController
@RequestMapping("/program")
public class ProgramController {

    @Autowired
    private ProgramService programService;

    @Autowired
    private UserService userService;
    // 发布节目（接收 userId 参数）
    @PostMapping("/publish")
    @PreAuthorize("@ss.hasPermi('program:publish')")
    public Result publish(@RequestBody ProgramSchedule program, @RequestParam Long userId) {
        User user = userService.getById(userId);
        if (user == null || (!"staff".equals(user.getRole()))) {
            return Result.error("无权限，需要广播站成员身份");
        }
        program.setStaffId(user.getId());
        program.setStatus("published");
        program.setPublishTime(LocalDateTime.now());
        program.setCreateTime(LocalDateTime.now());
        return programService.save(program) ? Result.success("发布成功") : Result.error("发布失败");
    }
    // 删除节目单
    @DeleteMapping("/delete/{id}")
    @PreAuthorize("@ss.hasPermi('program:delete')")
    public Result deleteProgram(@PathVariable Long id) {
        return programService.removeById(id) ? Result.success("删除成功") : Result.error("删除失败");
    }
    // 查询所有节目单
    @GetMapping("/list")
    public Result listAll() {
        return Result.success(programService.list());
    }

    // 修改节目单
    @PutMapping("/update")
    @PreAuthorize("@ss.hasPermi('program:edit')")
    public Result updateProgram(@RequestBody ProgramSchedule program) {
        return programService.updateById(program) ? Result.success("修改成功") : Result.error("修改失败");
    }
    // 节目单详情
    @GetMapping("/detail/{id}")
    public Result getProgramDetail(@PathVariable Long id) {
        return Result.success(programService.getById(id));
    }
    // 搜索节目单
    @GetMapping("/search")
    public Result searchPrograms(@RequestParam(required = false) String programName,
                                 @RequestParam(required = false) String date) {
        return Result.success(programService.lambdaQuery()
                .like(programName != null && !programName.isEmpty(), ProgramSchedule::getProgramName, programName)
                .eq(date != null && !date.isEmpty(), ProgramSchedule::getDate, date)
                .orderByDesc(ProgramSchedule::getDate)
                .list());
    }
}