-- ============================================================
-- 实验4 安全管理：菜单表 + 角色菜单关联表 + 种子数据
-- 数据库：broadcast_db
-- ============================================================

-- 菜单表：一张表承载目录(M)、菜单(C)、按钮(F)三类数据
DROP TABLE IF EXISTS menu;
CREATE TABLE menu (
    id          BIGINT       PRIMARY KEY AUTO_INCREMENT COMMENT '菜单ID',
    menu_name   VARCHAR(50)  NOT NULL COMMENT '菜单名称',
    parent_id   BIGINT       NOT NULL DEFAULT 0 COMMENT '父菜单ID，0表示根目录',
    menu_type   CHAR(1)      NOT NULL COMMENT '菜单类型：M目录 C菜单 F按钮',
    path        VARCHAR(200) DEFAULT NULL COMMENT '前端路由路径',
    component   VARCHAR(255) DEFAULT NULL COMMENT '前端组件路径',
    perms       VARCHAR(100) DEFAULT NULL COMMENT '权限标识，规范为 模块:操作',
    icon        VARCHAR(100) DEFAULT NULL COMMENT '菜单图标',
    order_num   INT          NOT NULL DEFAULT 0 COMMENT '显示顺序',
    visible     INT          NOT NULL DEFAULT 1 COMMENT '是否可见：0隐藏 1显示',
    status      INT          NOT NULL DEFAULT 1 COMMENT '菜单状态：0停用 1正常',
    create_time DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) COMMENT '菜单权限表';

-- 角色菜单关联表：以角色编码关联（本系统角色固定为 student/staff/teacher）
DROP TABLE IF EXISTS role_menu;
CREATE TABLE role_menu (
    role_code VARCHAR(20) NOT NULL COMMENT '角色编码',
    menu_id   BIGINT      NOT NULL COMMENT '菜单ID',
    PRIMARY KEY (role_code, menu_id)
) COMMENT '角色菜单关联表';

-- ------------------------------------------------------------
-- 菜单种子数据
-- ------------------------------------------------------------
-- 一级目录
INSERT INTO menu(id,menu_name,parent_id,menu_type,perms,icon,order_num) VALUES
 (100,'用户与权限',0,'M',NULL,'user',1),
 (110,'点歌管理',0,'M',NULL,'music',2),
 (120,'投稿管理',0,'M',NULL,'edit',3),
 (130,'音频管理',0,'M',NULL,'headset',4),
 (140,'留言管理',0,'M',NULL,'message',5),
 (150,'节目单管理',0,'M',NULL,'calendar',6);

-- 用户与权限
INSERT INTO menu(id,menu_name,parent_id,menu_type,path,perms,order_num) VALUES
 (101,'菜单管理',100,'C','/menu','menu:list',1);
INSERT INTO menu(id,menu_name,parent_id,menu_type,perms,order_num) VALUES
 (102,'角色授权',100,'F','menu:grant',2);

-- 点歌管理
INSERT INTO menu(id,menu_name,parent_id,menu_type,path,perms,order_num) VALUES
 (111,'点歌审核',110,'C','/auditSong','song:audit',1),
 (113,'点歌大厅',110,'C','/allSong','song:list',2);
INSERT INTO menu(id,menu_name,parent_id,menu_type,perms,order_num) VALUES
 (112,'审核处理',110,'F','song:edit',3),
 (114,'我要点歌',110,'F','song:add',4),
 (115,'删除点歌',110,'F','song:delete',5);

-- 投稿管理
INSERT INTO menu(id,menu_name,parent_id,menu_type,path,perms,order_num) VALUES
 (121,'稿件审核',120,'C','/auditArticle','article:audit',1),
 (122,'投稿浏览',120,'C','/allArticle','article:list',2);
INSERT INTO menu(id,menu_name,parent_id,menu_type,perms,order_num) VALUES
 (123,'我要投稿',120,'F','article:add',3),
 (124,'编辑稿件',120,'F','article:edit',4),
 (125,'删除稿件',120,'F','article:delete',5);

-- 音频管理
INSERT INTO menu(id,menu_name,parent_id,menu_type,path,perms,order_num) VALUES
 (131,'在线音频库',130,'C','/audio','audio:list',1);
INSERT INTO menu(id,menu_name,parent_id,menu_type,perms,order_num) VALUES
 (132,'上传音频',130,'F','audio:upload',2),
 (133,'删除音频',130,'F','audio:delete',3);

-- 留言管理
INSERT INTO menu(id,menu_name,parent_id,menu_type,path,perms,order_num) VALUES
 (141,'留言板',140,'C','/message','message:list',1);
INSERT INTO menu(id,menu_name,parent_id,menu_type,perms,order_num) VALUES
 (142,'发表留言',140,'F','message:add',2),
 (143,'回复留言',140,'F','message:reply',3);

-- 节目单管理
INSERT INTO menu(id,menu_name,parent_id,menu_type,path,perms,order_num) VALUES
 (151,'节目单列表',150,'C','/program','program:list',1);
INSERT INTO menu(id,menu_name,parent_id,menu_type,perms,order_num) VALUES
 (152,'发布节目单',150,'F','program:publish',2),
 (153,'编辑节目单',150,'F','program:edit',3),
 (154,'删除节目单',150,'F','program:delete',4);

-- ------------------------------------------------------------
-- 角色菜单种子数据
-- ------------------------------------------------------------
-- 广播站成员：拥有全部菜单
INSERT INTO role_menu(role_code,menu_id)
SELECT 'staff', id FROM menu;

-- 学生：点歌、投稿、音频浏览、留言、节目单浏览及对应父级目录
INSERT INTO role_menu(role_code,menu_id) VALUES
 ('student',110),('student',113),('student',114),
 ('student',120),('student',122),('student',123),
 ('student',130),('student',131),
 ('student',140),('student',141),('student',142),
 ('student',150),('student',151);

-- 教师：浏览各类内容、留言建议
INSERT INTO role_menu(role_code,menu_id) VALUES
 ('teacher',110),('teacher',113),
 ('teacher',120),('teacher',122),
 ('teacher',130),('teacher',131),
 ('teacher',140),('teacher',141),('teacher',142),
 ('teacher',150),('teacher',151);

-- ------------------------------------------------------------
-- 现有测试账号密码改为 BCrypt（与安全配置的编码器一致）
-- 123456 的 BCrypt 密文由 BCryptPasswordEncoder 生成（docs/exp4/GenBcrypt.java）
-- ------------------------------------------------------------
UPDATE user SET password = '$2a$10$TWdjcyM1b.FMMjn1b09mTe13uyClC0NfYsULzb8j1GtzOsIF3i4Xe'
WHERE username IN ('student1', 'staff1', 'teacher1', 'yyx', 'test001');
