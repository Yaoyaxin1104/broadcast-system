package com.grbroadcast.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.grbroadcast.dao.ArticleMapper;
import com.grbroadcast.entity.Article;
import com.grbroadcast.service.ArticleService;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class ArticleServiceImpl extends ServiceImpl<ArticleMapper, Article> implements ArticleService {

    @Override
    public boolean addArticle(Article article) {
        article.setStatus("pending");
        article.setCreateTime(LocalDateTime.now());
        return save(article);
    }

    @Override
    public boolean auditArticle(Long id, String status) {
        Article article = getById(id);
        if (article != null) {
            article.setStatus(status);
            article.setAuditTime(LocalDateTime.now());
            return updateById(article);
        }
        return false;
    }

    @Override
    public List<Article> getPending() {
        return baseMapper.findPending();
    }
}