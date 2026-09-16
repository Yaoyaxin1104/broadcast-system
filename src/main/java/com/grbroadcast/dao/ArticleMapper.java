package com.grbroadcast.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grbroadcast.entity.Article;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import java.util.List;

@Mapper
public interface ArticleMapper extends BaseMapper<Article> {

    @Select("SELECT * FROM article WHERE status = 'pending' ORDER BY create_time DESC")
    List<Article> findPending();
}