param([Parameter(Mandatory=$true)][string]$Scn)
chcp 65001 > $null
[Console]::OutputEncoding = New-Object Text.UTF8Encoding($false)
$OutputEncoding = New-Object Text.UTF8Encoding($false)
$base = 'http://localhost:8089/api'
$cli  = 'F:\Redis服务器-x64-5.0.10\redis-cli.exe'

function Get-Token($u) {
    $body = @{ username=$u; password='123456' } | ConvertTo-Json -Compress
    $resp = Invoke-RestMethod -Method Post "$base/auth/login" -ContentType 'application/json' -Body $body
    return $resp.data.token
}
function Cmd($c){ Write-Host "PS> $c" -ForegroundColor DarkYellow }
function Pretty($r){ ($r | ConvertFrom-Json) | ConvertTo-Json -Depth 8 }
function Esc($b){ return $b.Replace('"','\"') }

switch ($Scn) {
 'login' {
   Clear-Host
   Write-Host '===== 场景1：调用登录接口，认证成功返回令牌 =====' -ForegroundColor Cyan
   $body = '{"username":"staff1","password":"123456"}'
   Cmd "curl.exe -X POST $base/auth/login -H `"Content-Type:application/json`" -d '$body'"
   $r = curl.exe -s -X POST "$base/auth/login" -H 'Content-Type: application/json' --data (Esc $body)
   Pretty $r
 }
 'info' {
   Clear-Host
   Write-Host '===== 场景2：携带令牌访问 /auth/info =====' -ForegroundColor Cyan
   $t = Get-Token 'staff1'
   Cmd "curl.exe $base/auth/info -H `"Authorization: Bearer $t`""
   $r = curl.exe -s "$base/auth/info" -H "Authorization: Bearer $t"
   Pretty $r
 }
 '403' {
   Clear-Host
   Write-Host '===== 场景3：学生令牌访问广播站成员接口，返回 403 =====' -ForegroundColor Cyan
   $t = Get-Token 'student1'
   Cmd "curl.exe $base/song/pending -H `"Authorization: Bearer $t`""
   curl.exe -s -w "`nHTTP_STATUS:%{http_code}" "$base/song/pending" -H "Authorization: Bearer $t"
 }
 '401' {
   Clear-Host
   Write-Host '===== 场景4：不带令牌访问受控接口，返回 401 =====' -ForegroundColor Cyan
   Cmd "curl.exe $base/song/pending"
   curl.exe -s -w "`nHTTP_STATUS:%{http_code}" "$base/song/pending"
 }
 'logout' {
   Clear-Host
   Write-Host '===== 场景5：退出登录后，原令牌立即失效返回 401 =====' -ForegroundColor Cyan
   $t = Get-Token 'staff1'
   Cmd "curl.exe -X POST $base/auth/logout -H `"Authorization: Bearer $t`""
   curl.exe -s -X POST "$base/auth/logout" -H "Authorization: Bearer $t"
   Write-Host ''
   Cmd "curl.exe $base/auth/info -H `"Authorization: Bearer <原令牌>`""
   curl.exe -s -w "`nHTTP_STATUS:%{http_code}" "$base/auth/info" -H "Authorization: Bearer $t"
 }
 'redis' {
   Clear-Host
   Write-Host '===== 场景6：Redis 中查看登录缓存 =====' -ForegroundColor Cyan
   $null = Get-Token 'staff1'
   Cmd 'redis-cli keys "login:user:*"'
   & $cli keys 'login:user:*'
   Write-Host ''
   Cmd 'redis-cli get login:user:5'
   & $cli get 'login:user:5'
 }
 'jwt' {
   Clear-Host
   Write-Host '===== 场景7：解开令牌，载荷仅含 userId/iat/exp =====' -ForegroundColor Cyan
   $t = Get-Token 'staff1'
   Cmd 'JWT ='
   Write-Host $t
   $p = $t.Split('.')[1].Replace('-','+').Replace('_','/')
   switch ($p.Length % 4) { 2 { $p += '==' } 3 { $p += '=' } }
   $j = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($p)) | ConvertFrom-Json
   Cmd '解码后的载荷：'
   $j | ConvertTo-Json
 }
}
