package com.grbroadcast.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.grbroadcast.entity.Article;
import java.util.List;

public interface ArticleService extends IService<Article> {
    boolean addArticle(Article article);
    boolean auditArticle(Long id, String status);
    List<Article> getPending();
}