package com.grbroadcast.task;

import com.grbroadcast.entity.SongRequest;
import com.grbroadcast.service.SongService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;

@Component
public class ScheduledTasks {

    @Autowired
    private SongService songService;

    // ========== 每天凌晨2点执行 ==========
    @Scheduled(cron = "0 0 2 * * ?")
    public void cleanPendingSongs() {
        System.out.println("=== 定时任务开始：清理超过7天的待审核点歌 ===");
        System.out.println("执行时间：" + LocalDateTime.now());

        try {
            // 查询所有待审核的点歌
            List<SongRequest> pendingList = songService.lambdaQuery()
                    .eq(SongRequest::getStatus, "pending")
                    .list();

            int count = 0;
            for (SongRequest song : pendingList) {
                // 如果创建时间超过7天，自动标记为已拒绝
                if (song.getCreateTime().isBefore(LocalDateTime.now().minusDays(7))) {
                    song.setStatus("rejected");
                    song.setAuditTime(LocalDateTime.now());
                    songService.updateById(song);
                    count++;
                    System.out.println("自动拒绝点歌ID：" + song.getId() + "，歌曲：" + song.getSongName());
                }
            }

            System.out.println("定时任务完成，共处理：" + count + " 条记录");

        } catch (Exception e) {
            System.err.println("定时任务执行失败：" + e.getMessage());
            e.printStackTrace();
        }
    }

    // ========== 每天凌晨3点执行：统计点歌数量 ==========
    @Scheduled(cron = "0 0 3 * * ?")
    public void countSongs() {
        System.out.println("=== 定时任务：统计点歌数据 ===");
        System.out.println("执行时间：" + LocalDateTime.now());

        long total = songService.count();
        long pending = songService.lambdaQuery().eq(SongRequest::getStatus, "pending").count();
        long approved = songService.lambdaQuery().eq(SongRequest::getStatus, "approved").count();
        long rejected = songService.lambdaQuery().eq(SongRequest::getStatus, "rejected").count();

        System.out.println("点歌统计结果：");
        System.out.println("  总点歌数：" + total);
        System.out.println("  待审核：" + pending);
        System.out.println("  已通过：" + approved);
        System.out.println("  已拒绝：" + rejected);
        System.out.println("=== 统计完成 ===");
    }
}