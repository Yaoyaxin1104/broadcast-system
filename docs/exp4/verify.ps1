$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$base = 'http://localhost:8089/api'
$out = 'C:\Users\yyxyz\IdeaProjects\broadcast-system\docs\exp4\verify_transcript.txt'

function W($s){ $s | Out-File -FilePath $out -Append -Encoding UTF8; Write-Host $s }

function Req($method, $url, $headers, $bodyObj) {
    try {
        $params = @{ Uri = $url; Method = $method; ContentType = 'application/json;charset=UTF-8' }
        if ($headers) { $params.Headers = $headers }
        if ($null -ne $bodyObj) { $params.Body = ($bodyObj | ConvertTo-Json -Compress -Depth 6) }
        $r = Invoke-RestMethod @params
        return [pscustomobject]@{ Status = 200; Body = ($r | ConvertTo-Json -Compress -Depth 8) }
    } catch {
        $resp = $_.Exception.Response
        $status = [int]$resp.StatusCode
        $b = $_.ErrorDetails.Message
        if (-not $b) {
            try {
                $reader = New-Object IO.StreamReader($resp.GetResponseStream())
                $b = $reader.ReadToEnd()
            } catch { $b = '' }
        }
        return [pscustomobject]@{ Status = $status; Body = $b }
    }
}

Set-Content $out '=========== 实验4 认证授权验证记录 ===========' -Encoding UTF8

W '--- 1. 无令牌访问 /auth/info（预期 401）---'
$r = Req 'GET' "$base/auth/info" $null $null
W ("HTTP " + $r.Status + "  " + $r.Body)

W '--- 2. staff1 登录（预期返回 token）---'
$r = Req 'POST' "$base/auth/login" $null ([pscustomobject]@{ username='staff1'; password='123456' })
W ("HTTP " + $r.Status + "  " + $r.Body)
$staffToken = ($r.Body | ConvertFrom-Json).data.token

W '--- 3. 携带 staff 令牌访问 /auth/info（预期 200）---'
$h = @{ Authorization = "Bearer $staffToken" }
$r = Req 'GET' "$base/auth/info" $h $null
W ("HTTP " + $r.Status + "  " + $r.Body)

W '--- 4. staff 查询菜单树 /menu/tree（预期 200）---'
$r = Req 'GET' "$base/menu/tree" $h $null
W ("HTTP " + $r.Status + "  " + ($r.Body).Substring(0, [Math]::Min(300, $r.Body.Length)))

W '--- 5. staff 访问待审核点歌 /song/pending（预期 200）---'
$r = Req 'GET' "$base/song/pending" $h $null
W ("HTTP " + $r.Status + "  " + $r.Body)

W '--- 6. Redis 中查看登录缓存键与值 ---'
$cli = 'F:\Redis服务器-x64-5.0.10\redis-cli.exe'
$keys = & $cli keys 'login:user:*'
W ("KEYS: " + ($keys -join ', '))
foreach ($k in $keys) { W ("VALUE " + $k + " = " + (& $cli get $k)) }

W '--- 7. 解开 JWT 令牌查看载荷（预期仅 userId/iat/exp）---'
$payloadPart = $staffToken.Split('.')[1].Replace('-', '+').Replace('_', '/')
switch ($payloadPart.Length % 4) { 2 { $payloadPart += '==' } 3 { $payloadPart += '=' } }
$payloadJson = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($payloadPart))
W ("PAYLOAD: " + $payloadJson)

W '--- 8. student1 登录 ---'
$r = Req 'POST' "$base/auth/login" $null ([pscustomobject]@{ username='student1'; password='123456' })
W ("HTTP " + $r.Status + "  " + $r.Body)
$stuToken = ($r.Body | ConvertFrom-Json).data.token

W '--- 9. student 访问待审核点歌 /song/pending（预期 403）---'
$sh = @{ Authorization = "Bearer $stuToken" }
$r = Req 'GET' "$base/song/pending" $sh $null
W ("HTTP " + $r.Status + "  " + $r.Body)

W '--- 10. student 提交点歌 /song/add?userId=4（预期 200）---'
$song = [pscustomobject]@{ songName='测试歌曲-实验4'; singer='测试歌手'; reason='实验4验证用' }
$r = Req 'POST' "$base/song/add?userId=4" $sh $song
W ("HTTP " + $r.Status + "  " + $r.Body)

W '--- 11. staff 退出登录 ---'
$r = Req 'POST' "$base/auth/logout" $h $null
W ("HTTP " + $r.Status + "  " + $r.Body)

W '--- 12. 退出后原令牌再访问 /auth/info（预期 401）---'
$r = Req 'GET' "$base/auth/info" $h $null
W ("HTTP " + $r.Status + "  " + $r.Body)

W '--- 13. 错误密码登录（预期 账号或密码错误）---'
$r = Req 'POST' "$base/auth/login" $null ([pscustomobject]@{ username='staff1'; password='wrongpwd' })
W ("HTTP " + $r.Status + "  " + $r.Body)

W '=========== 验证结束 ==========='
W ("STAFF_TOKEN=" + $staffToken)
W ("STUDENT_TOKEN=" + $stuToken)
