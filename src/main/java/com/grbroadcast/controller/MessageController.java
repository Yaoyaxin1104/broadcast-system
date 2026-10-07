package com.grbroadcast.controller;

import com.grbroadcast.common.Result;
import com.grbroadcast.entity.Message;
import com.grbroadcast.entity.User;
import com.grbroadcast.service.MessageService;
import com.grbroadcast.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDateTime;

@CrossOrigin(origins = "*", allowCredentials = "false")
@RestController
@RequestMapping("/message")
public class MessageController {

    @Autowired
    private MessageService messageService;

    @Autowired
    private UserService userService;

    // 学生端 - 发布留言
    @PostMapping("/add")
    @PreAuthorize("@ss.hasPermi('message:add')")
    public Result addMessage(@RequestBody Message message, @RequestParam Long userId) {
        User user = userService.getById(userId);
        if (user == null) {
            return Result.error("请先登录");
        }
        message.setUserId(user.getId());
        message.setStatus(1);
        message.setCreateTime(LocalDateTime.now());
        return messageService.save(message) ? Result.success("留言成功") : Result.error("留言失败");
    }

    // 管理端 - 删除留言
    @DeleteMapping("/delete/{id}")
    @PreAuthorize("@ss.hasPermi('message:reply')")
    public Result deleteMessage(@PathVariable Long id) {
        return messageService.removeById(id) ? Result.success("删除成功") : Result.error("删除失败");
    }

    // 管理端 - 回复留言（接收 userId 参数）
    @PutMapping("/reply/{id}")
    @PreAuthorize("@ss.hasPermi('message:reply')")
    public Result replyMessage(@PathVariable Long id,
                               @RequestParam String reply,
                               @RequestParam Long userId) {
        // 打印日志，方便调试
        System.out.println("=== 回复留言请求 ===");
        System.out.println("留言ID: " + id);
        System.out.println("回复内容: " + reply);
        System.out.println("操作人ID: " + userId);

        User user = userService.getById(userId);
        if (user == null) {
            System.out.println("用户不存在");
            return Result.error("用户不存在");
        }
        System.out.println("用户角色: " + user.getRole());

        if (!"staff".equals(user.getRole())) {
            System.out.println("无权限，需要 staff ");
            return Result.error("无权限，需要广播站成员身份");
        }

        boolean result = messageService.replyMessage(id, reply);
        System.out.println("回复结果: " + result);
        return result ? Result.success("回复成功") : Result.error("回复失败");
    }
    // 搜索留言
    @GetMapping("/search")
    public Result searchMessages(@RequestParam String content) {
        return Result.success(messageService.lambdaQuery()
                .like(Message::getContent, content)
                .eq(Message::getStatus, 1)
                .orderByDesc(Message::getCreateTime)
                .list());
    }

    // 查询所有留言
    @GetMapping("/list")
    public Result listAll() {
        return Result.success(messageService.lambdaQuery()
                .eq(Message::getStatus, 1)
                .orderByDesc(Message::getCreateTime)
                .list());
    }
}