package com.grbroadcast.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.grbroadcast.common.Result;
import com.grbroadcast.entity.Article;
import com.grbroadcast.entity.User;
import com.grbroadcast.service.ArticleService;
import com.grbroadcast.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@CrossOrigin(origins = "*", allowCredentials = "false")
@RestController
@RequestMapping("/article")
public class ArticleController {

    @Autowired
    private ArticleService articleService;

    @Autowired
    private UserService userService;
    @PostMapping("/add")
    @PreAuthorize("@ss.hasPermi('article:add')")
    public Result addArticle(@RequestBody Article article, @RequestParam Long userId) {
        User user = userService.getById(userId);
        if (user == null || !"student".equals(user.getRole())) {
            return Result.error("请先登录学生账号");
        }
        article.setStudentId(user.getId());
        //service处理
        return articleService.addArticle(article) ? Result.success("投稿成功") : Result.error("投稿失败");
    }
    @GetMapping("/search")
    public Result searchArticles(@RequestParam(required = false) String title,
                                 @RequestParam(required = false) String status) {
        LambdaQueryWrapper<Article> wrapper = new LambdaQueryWrapper<>();
        if (title != null && !title.isEmpty()) {
            wrapper.like(Article::getTitle, title);
        }
        if (status != null && !status.isEmpty()) {
            wrapper.eq(Article::getStatus, status);
        }
        wrapper.orderByDesc(Article::getCreateTime);
        return Result.success(articleService.list(wrapper));
    }
    // 修改稿件
    @PutMapping("/update")
    @PreAuthorize("@ss.hasPermi('article:edit')")
    public Result updateArticle(@RequestBody Article article) {
        return articleService.updateById(article) ? Result.success("修改成功") : Result.error("修改失败");
    }
    // 稿件详情
    @GetMapping("/detail/{id}")
    public Result getArticleDetail(@PathVariable Long id) {
        return Result.success(articleService.getById(id));
    }
    @DeleteMapping("/delete/{id}")
    @PreAuthorize("@ss.hasPermi('article:delete')")
    public Result deleteArticle(@PathVariable Long id) {
        return articleService.removeById(id) ? Result.success("删除成功") : Result.error("删除失败");
    }
    @PutMapping("/audit/{id}")
    @PreAuthorize("@ss.hasPermi('article:audit')")
    public Result auditArticle(@PathVariable Long id,
                               @RequestParam String status,
                               @RequestParam Long userId) {
        System.out.println("审核请求: id=" + id + ", status=" + status + ", userId=" + userId);
        User user = userService.getById(userId);
        if (user == null || !"staff".equals(user.getRole())) {
            return Result.error("无权限，当前用户角色: " + (user != null ? user.getRole() : "null"));
        }
        boolean result = articleService.auditArticle(id, status);
        return result ? Result.success("审核完成") : Result.error("审核失败");
    }
    @GetMapping("/list")
    public Result listAll() {
        return Result.success(articleService.list());
    }
    @GetMapping("/pending")
    @PreAuthorize("@ss.hasPermi('article:audit')")
    public Result getPending() {
        return Result.success(articleService.getPending());

    }
}