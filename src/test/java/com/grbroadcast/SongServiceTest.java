package com.grbroadcast;

import com.grbroadcast.entity.SongRequest;
import com.grbroadcast.service.SongService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import java.util.List;
import java.util.Map;

@SpringBootTest
public class SongServiceTest {

    @Autowired
    private SongService songService;

    // 测试1：新增点歌（增）
    @Test
    public void testAddSong() {
        SongRequest song = new SongRequest();
        song.setStudentId(1L);
        song.setSongName("稻香");
        song.setSinger("周杰伦");
        song.setMessage("送给全体同学");

        boolean result = songService.addSong(song);  // 改为 addSong
        System.out.println("新增结果: " + (result ? "成功 ✓" : "失败 ✗"));
    }

    // 测试2：多表关联查询所有点歌（查）
    @Test
    public void testGetAllWithStudent() {
        List<Map<String, Object>> list = songService.getAllWithStudent();  // 改为 getAllWithStudent
        System.out.println("=== 点歌记录（含学生信息） ===");
        if (list != null) {
            for (Map<String, Object> item : list) {
                System.out.println("ID: " + item.get("id") +
                        " | 歌曲: " + item.get("song_name") +
                        " | 学生: " + item.get("student_name") +
                        " | 状态: " + item.get("status"));
            }
            System.out.println("总数: " + list.size());
        }
    }

    // 测试3：修改点歌状态（改）
    @Test
    public void testUpdateStatus() {
        boolean result = songService.auditSong(1L, "approved");  // 改为 auditSong
        System.out.println("修改状态结果: " + (result ? "成功 ✓" : "失败 ✗"));
    }

    // 测试4：删除点歌（删）
    @Test
    public void testDeleteSong() {
        boolean result = songService.deleteSong(4L);  // 改为 deleteSong
        System.out.println("删除结果: " + (result ? "成功 ✓" : "失败 ✗"));
    }
}