-- ============================================================
-- 广软广播站点歌与投稿系统 数据库建库建表脚本（MySQL 8.0）
-- 数据库：broadcast_db_demo
-- 引擎：InnoDB    字符集：utf8mb4    排序规则：utf8mb4_0900_ai_ci
-- 命名规范：全小写 + 下划线，表名/字段名一律使用单数
-- 说明：表间关联采用“逻辑外键 + 普通索引”实现（关联列建索引，
--       不建立数据库级 FOREIGN KEY 约束），原因见实验报告物理结构设计一节；
--       脚本末尾以注释形式给出等价的物理外键语句，供需要强一致时启用。
-- ============================================================

CREATE DATABASE IF NOT EXISTS broadcast_db_demo
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE broadcast_db_demo;

-- 为保证脚本可重复执行，按“子表 -> 父表”顺序删除
DROP TABLE IF EXISTS song_request;
DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS audio;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS program_schedule;
DROP TABLE IF EXISTS `user`;

-- ------------------------------------------------------------
-- 1. 用户表 user（学生、广播站成员、教师统一由 role 字段区分）
-- ------------------------------------------------------------
CREATE TABLE `user` (
    `id`          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '用户ID，主键',
    `username`    VARCHAR(50)  NOT NULL COMMENT '用户名（登录账号）',
    `password`    VARCHAR(255) NOT NULL COMMENT '密码（MD5加密存储，32位密文）',
    `real_name`   VARCHAR(50)  DEFAULT NULL COMMENT '真实姓名',
    `student_id`  VARCHAR(20)  DEFAULT NULL COMMENT '学号',
    `role`        VARCHAR(20)  NOT NULL COMMENT '角色：student学生/staff广播站成员/teacher教师',
    `phone`       VARCHAR(20)  DEFAULT NULL COMMENT '联系电话',
    `email`       VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    `status`      INT          NOT NULL DEFAULT 1 COMMENT '状态：0禁用 1启用',
    `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    KEY `idx_role` (`role`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户表';

-- ------------------------------------------------------------
-- 2. 点歌单表 song_request（学生点歌申请）
-- ------------------------------------------------------------
CREATE TABLE `song_request` (
    `id`          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '点歌单ID，主键',
    `student_id`  BIGINT       NOT NULL COMMENT '点歌学生，逻辑外键 -> user.id',
    `song_name`   VARCHAR(100) NOT NULL COMMENT '歌曲名称',
    `singer`      VARCHAR(50)  NOT NULL COMMENT '歌手',
    `message`     VARCHAR(500) DEFAULT NULL COMMENT '点歌留言',
    `status`      VARCHAR(20)  NOT NULL DEFAULT 'pending' COMMENT '状态：pending待审核/approved通过/rejected驳回',
    `audit_time`  DATETIME     DEFAULT NULL COMMENT '审核时间',
    `play_time`   DATETIME     DEFAULT NULL COMMENT '播放时间',
    `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
    PRIMARY KEY (`id`),
    KEY `idx_student_id` (`student_id`),
    KEY `idx_status` (`status`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '点歌单表';

-- ------------------------------------------------------------
-- 3. 投稿文章表 article（学生投稿：新闻/故事/诗歌）
-- ------------------------------------------------------------
CREATE TABLE `article` (
    `id`          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '稿件ID，主键',
    `student_id`  BIGINT       NOT NULL COMMENT '投稿学生，逻辑外键 -> user.id',
    `title`       VARCHAR(200) NOT NULL COMMENT '标题',
    `content`     TEXT         NOT NULL COMMENT '正文内容',
    `type`        VARCHAR(20)  NOT NULL COMMENT '类型：news新闻/story故事/poem诗歌',
    `status`      VARCHAR(20)  NOT NULL DEFAULT 'pending' COMMENT '状态：pending待审核/approved通过/rejected驳回',
    `audit_time`  DATETIME     DEFAULT NULL COMMENT '审核时间',
    `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '投稿时间',
    PRIMARY KEY (`id`),
    KEY `idx_student_id` (`student_id`),
    KEY `idx_status` (`status`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '投稿文章表';

-- ------------------------------------------------------------
-- 4. 音频表 audio（广播站成员上传的节目音频）
-- ------------------------------------------------------------
CREATE TABLE `audio` (
    `id`          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '音频ID，主键',
    `staff_id`    BIGINT       NOT NULL COMMENT '上传成员，逻辑外键 -> user.id',
    `title`       VARCHAR(100) NOT NULL COMMENT '音频标题',
    `file_path`   VARCHAR(255) NOT NULL COMMENT '文件存储路径',
    `file_size`   BIGINT       DEFAULT NULL COMMENT '文件大小（字节）',
    `duration`    INT          DEFAULT NULL COMMENT '时长（秒）',
    `play_count`  INT          NOT NULL DEFAULT 0 COMMENT '播放次数，默认0',
    `status`      INT          NOT NULL DEFAULT 1 COMMENT '状态：0下线 1上线',
    `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
    PRIMARY KEY (`id`),
    KEY `idx_staff_id` (`staff_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '音频表';

-- ------------------------------------------------------------
-- 5. 留言表 message（师生留言与广播站回复）
-- ------------------------------------------------------------
CREATE TABLE `message` (
    `id`          BIGINT       NOT NULL AUTO_INCREMENT COMMENT '留言ID，主键',
    `user_id`     BIGINT       NOT NULL COMMENT '留言用户，逻辑外键 -> user.id',
    `content`     VARCHAR(500) NOT NULL COMMENT '留言内容',
    `reply`       VARCHAR(500) DEFAULT NULL COMMENT '回复内容',
    `status`      INT          NOT NULL DEFAULT 1 COMMENT '状态：0隐藏 1显示',
    `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '留言时间',
    PRIMARY KEY (`id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '留言表';

-- ------------------------------------------------------------
-- 6. 节目单表 program_schedule（广播站成员编排的每日节目单）
-- ------------------------------------------------------------
CREATE TABLE `program_schedule` (
    `id`           BIGINT       NOT NULL AUTO_INCREMENT COMMENT '节目单ID，主键',
    `staff_id`     BIGINT       NOT NULL COMMENT '编排成员，逻辑外键 -> user.id',
    `date`         DATE         NOT NULL COMMENT '节目日期',
    `time_slot`    VARCHAR(20)  NOT NULL COMMENT '时间段，如12:00-12:30',
    `program_name` VARCHAR(100) NOT NULL COMMENT '节目名称',
    `content`      TEXT         COMMENT '节目内容',
    `songs`        TEXT         COMMENT '播放歌单（播出时点歌单的快照文本）',
    `status`       VARCHAR(20)  NOT NULL DEFAULT 'draft' COMMENT '状态：draft草稿/published已发布',
    `publish_time` DATETIME     DEFAULT NULL COMMENT '发布时间',
    `create_time`  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `idx_staff_id` (`staff_id`),
    KEY `idx_date` (`date`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '节目单表';

-- ============================================================
-- 测试数据
-- ============================================================
-- 用户：2名学生、1名广播站成员、1名教师（密码均为 MD5 加密后的 123456）
INSERT INTO `user` (id, username, password, real_name, student_id, role, phone, email, status) VALUES
(1, 'student1', 'e10adc3949ba59abbe56e057f20f883e', '张一', '2024001', 'student', '13800000001', 'student1@example.com', 1),
(2, 'student2', 'e10adc3949ba59abbe56e057f20f883e', '李二', '2024002', 'student', '13800000002', 'student2@example.com', 1),
(3, 'staff1',   'e10adc3949ba59abbe56e057f20f883e', '王广播', NULL,       'staff',   '13800000003', 'staff1@example.com',   1),
(4, 'teacher1', 'e10adc3949ba59abbe56e057f20f883e', '陈老师', NULL,       'teacher', '13800000004', 'teacher1@example.com', 1);

-- 点歌单
INSERT INTO song_request (id, student_id, song_name, singer, message, status, audit_time, play_time) VALUES
(1, 1, '晴天',   '周杰伦', '午间时段播放，谢谢广播站！',           'approved', '2026-09-20 09:10:00', '2026-09-21 12:05:00'),
(2, 1, '稻香',   '周杰伦', '送给正在军训的新生。',                 'pending',  NULL,                  NULL),
(3, 2, '起风了', '买辣椒也用券', '送给即将毕业的学长学姐。',         'pending',  NULL,                  NULL),
(4, 2, '夜曲',   '周杰伦', NULL,                                  'rejected', '2026-09-20 10:00:00', NULL);

-- 投稿文章
INSERT INTO article (id, student_id, title, content, type, status, audit_time) VALUES
(1, 1, '青春飞扬，梦想起航', '正文：九月，我们怀揣梦想走进广软校园……', 'poem',  'approved', '2026-09-19 16:00:00'),
(2, 2, '校园晨读：让书香伴随晨光', '正文：清晨的图书馆前，朗朗书声……', 'story', 'pending',  NULL),
(3, 1, '运动会加油稿（示例）', '正文：运动场上，每一滴汗水……',       'news',  'rejected', '2026-09-20 11:00:00');

-- 音频
INSERT INTO audio (id, staff_id, title, file_path, file_size, duration, play_count, status) VALUES
(1, 3, '晴天', '/uploads/aaa111.mp3', 4194304, 269, 35, 1),
(2, 3, '稻香', '/uploads/bbb222.mp3', 3670016, 223, 18, 1);

-- 留言
INSERT INTO message (id, user_id, content, reply, status) VALUES
(1, 1, '广播站的节目越来越精彩了！希望能多放一些流行歌曲。', '感谢支持，本周午间时段已安排流行音乐专场。', 1),
(2, 2, '点一首《起风了》送给即将毕业的学长学姐们。', NULL, 1),
(3, 4, '建议增加英语听力类节目。', NULL, 1);

-- 节目单
INSERT INTO program_schedule (id, staff_id, `date`, time_slot, program_name, content, songs, status, publish_time) VALUES
(1, 3, '2026-09-21', '12:00-12:30', '音乐午高峰', '流行音乐点播与祝福放送。', '晴天；夜曲；兰亭序', 'published', '2026-09-20 18:00:00'),
(2, 3, '2026-09-22', '17:30-18:00', '书香校园',   '优秀投稿文章朗读。',       NULL,                'published', '2026-09-21 18:00:00'),
(3, 3, '2026-09-23', '12:00-12:30', '广软心声',   '师生留言互动与点歌放送。', '起风了；稻香',       'draft',     NULL);

-- ============================================================
-- 可选：物理外键约束（项目默认不启用，需要数据库层强一致时执行）
-- ALTER TABLE song_request    ADD CONSTRAINT fk_song_user    FOREIGN KEY (student_id) REFERENCES `user`(id);
-- ALTER TABLE article         ADD CONSTRAINT fk_article_user FOREIGN KEY (student_id) REFERENCES `user`(id);
-- ALTER TABLE audio           ADD CONSTRAINT fk_audio_user   FOREIGN KEY (staff_id)   REFERENCES `user`(id);
-- ALTER TABLE message         ADD CONSTRAINT fk_message_user FOREIGN KEY (user_id)    REFERENCES `user`(id);
-- ALTER TABLE program_schedule ADD CONSTRAINT fk_program_user FOREIGN KEY (staff_id)  REFERENCES `user`(id);
-- ============================================================
