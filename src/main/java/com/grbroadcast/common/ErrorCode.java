package com.grbroadcast.common;

/**
 * 统一错误码枚举
 * 定义系统通用错误码与提示信息，供 Result、BizException 使用
 */
public enum ErrorCode {

    SUCCESS(200, "操作成功"),
    PARAM_ERROR(400, "参数错误"),
    UNAUTHORIZED(401, "未登录或登录已过期"),
    FORBIDDEN(403, "无权限访问"),
    NOT_FOUND(404, "请求的资源不存在"),
    DUPLICATE(409, "数据已存在"),
    SYSTEM_ERROR(500, "系统繁忙，请稍后重试"),
    BUSINESS_ERROR(1001, "业务处理失败");

    private final int code;
    private final String msg;

    ErrorCode(int code, String msg) {
        this.code = code;
        this.msg = msg;
    }

    public int getCode() {
        return code;
    }

    public String getMsg() {
        return msg;
    }
}
