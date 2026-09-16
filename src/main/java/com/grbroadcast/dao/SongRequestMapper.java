package com.grbroadcast.dao;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grbroadcast.entity.SongRequest;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import java.util.List;
import java.util.Map;

@Mapper
public interface SongRequestMapper extends BaseMapper<SongRequest> {

    // 多表关联查询：点歌记录 + 学生信息
    @Select("SELECT sr.*, u.real_name as student_name, u.student_id as student_no " +
            "FROM song_request sr " +
            "LEFT JOIN user u ON sr.student_id = u.id " +
            "WHERE sr.id = #{id}")
    Map<String, Object> getSongRequestWithStudent(@Param("id") Long id);
    // 查询所有点歌记录（带学生信息）
    @Select("SELECT sr.*, u.real_name as student_name, u.student_id as student_no " +
            "FROM song_request sr " +
            "LEFT JOIN user u ON sr.student_id = u.id " +
            "ORDER BY sr.create_time DESC")
    List<Map<String, Object>> getAllWithStudent();
    // 根据学生ID查询（带学生信息）
    @Select("SELECT sr.*, u.real_name as student_name, u.student_id as student_no " +
            "FROM song_request sr " +
            "LEFT JOIN user u ON sr.student_id = u.id " +
            "WHERE sr.student_id = #{studentId} " +
            "ORDER BY sr.create_time DESC")
    List<Map<String, Object>> getByStudentIdWithInfo(@Param("studentId") Long studentId);
    // 根据状态查询（带学生信息）
    @Select("SELECT sr.*, u.real_name as student_name, u.student_id as student_no " +
            "FROM song_request sr " +
            "LEFT JOIN user u ON sr.student_id = u.id " +
            "WHERE sr.status = #{status} " +
            "ORDER BY sr.create_time DESC")
    List<Map<String, Object>> getByStatusWithInfo(@Param("status") String status);
    // mapper执行歌曲审核更新
    @Update("UPDATE song_request SET status = #{status}, audit_time = NOW() WHERE id = #{id}")
    int updateStatus(@Param("id") Long id, @Param("status") String status);
    // 删除前检查是否存在
    @Select("SELECT COUNT(*) FROM song_request WHERE id = #{id}")
    int existsById(@Param("id") Long id);
}