package com.grbroadcast.common;

import lombok.Data;

@Data
public class Result {
    private int code;
    private String msg;
    private Object data;
    public Result() {}

    public Result(int code, String msg, Object data) {
        this.code = code;
        this.msg = msg;
        this.data = data;
    }
    public static Result success(Object data) {
        return new Result(200, "success", data);
    }
    public static Result success(String msg, Object data) {
        return new Result(200, msg, data);
    }
    public static Result success(String msg) {
        return new Result(200, msg, null);
    }
    public static Result error(String msg) {
        return new Result(500, msg, null);
    }
    public static Result error(int code, String msg) {
        return new Result(code, msg, null);
    }
}