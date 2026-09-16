package com.grbroadcast.controller;

import com.grbroadcast.common.Result;
import com.grbroadcast.entity.Audio;
import com.grbroadcast.entity.User;
import com.grbroadcast.service.AudioService;
import com.grbroadcast.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.net.URLEncoder;
import java.nio.file.Files;
import java.time.LocalDateTime;
import java.util.UUID;

@CrossOrigin(origins = "*", allowCredentials = "false")
@RestController
@RequestMapping("/audio")
public class AudioController {

    @Autowired
    private AudioService audioService;

    @Autowired
    private UserService userService;

    @Value("${file.upload-path:D:/upload/}")
    private String uploadPath;

    // ========== 上传音频 ==========
    @PostMapping("/upload")
    public Result uploadAudio(@RequestParam("file") MultipartFile file,
                              @RequestParam("title") String title,
                              @RequestParam("userId") Long userId) {
        User user = userService.getById(userId);
        if (user == null || !"staff".equals(user.getRole())) {
            return Result.error("无权限，需要广播站成员身份");
        }

        try {
            File dir = new File(uploadPath);
            if (!dir.exists()) dir.mkdirs();

            String originalFilename = file.getOriginalFilename();
            String ext = originalFilename.substring(originalFilename.lastIndexOf("."));
            String newFilename = UUID.randomUUID().toString() + ext;
            String filePath = uploadPath + newFilename;
            file.transferTo(new File(filePath));

            Audio audio = new Audio();
            audio.setStaffId(user.getId());
            audio.setTitle(title);
            audio.setFilePath("/uploads/" + newFilename);
            audio.setFileSize(file.getSize());
            audio.setPlayCount(0);
            audio.setStatus(1);
            audio.setCreateTime(LocalDateTime.now());

            audioService.save(audio);
            return Result.success("上传成功");
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("上传失败：" + e.getMessage());
        }
    }

    // ========== 下载音频 ==========
    @GetMapping("/download/{id}")
    public ResponseEntity<?> downloadAudio(@PathVariable Long id) {
        try {
            // 1. 从数据库获取音频信息
            Audio audio = audioService.getById(id);
            if (audio == null) {
                return ResponseEntity.notFound().build();
            }

            // 2. 获取文件路径
            String fileName = audio.getFilePath().replace("/uploads/", "");
            String filePath = uploadPath + fileName;
            File file = new File(filePath);

            if (!file.exists()) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body("文件不存在：" + filePath);
            }

            // 3. 读取文件
            byte[] data = Files.readAllBytes(file.toPath());

            // 4. 设置响应头
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(org.springframework.http.MediaType.APPLICATION_OCTET_STREAM);
            headers.setContentDispositionFormData("attachment",
                    URLEncoder.encode(audio.getTitle() + ".mp3", "UTF-8"));

            return new ResponseEntity<>(data, headers, HttpStatus.OK);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("下载失败：" + e.getMessage());
        }
    }

    // ========== 获取音频列表 ==========
    @GetMapping("/list")
    public Result listAll() {
        return Result.success(audioService.lambdaQuery().eq(Audio::getStatus, 1).orderByDesc(Audio::getCreateTime).list());
    }

    // ========== 删除音频 ==========
    @DeleteMapping("/delete/{id}")
    public Result deleteAudio(@PathVariable Long id) {
        return audioService.removeById(id) ? Result.success("删除成功") : Result.error("删除失败");
    }
}