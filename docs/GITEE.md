# Gitee adapter

## 为什么要 token

Gitee API v5 的公开读允许匿名访问，但有速率限制；搜索接口在匿名状态下经常返回空或不稳定。用个人访问令牌（PAT）后：

- 请求带 `Authorization: Bearer <token>`；
- 额度提高；
- 搜索更稳定。

## 创建 token

1. 打开 https://gitee.com/profile/personal_access_tokens/new
2. 最小权限：只读 `projects` / 仓库读取；不要给 `admin`、`hook` 等写权限；
3. 生成后只显示一次，复制保存。

## 配置

二选一，不要把 token 写进仓库：

```bash
# 环境变量
export GITEE_TOKEN=...

# 或文件（推荐给本地 agent）
mkdir -p ~/.config/radar
printf '%s\n' '...' > ~/.config/radar/gitee_token
chmod 600 ~/.config/radar/gitee_token
```

## 运行

```bash
python3 -m radar run --pack packs/weak-current/pack.json \
  --seeds seeds/weak-current.json --title "弱电管理系统" \
  --out runs/gitee-demo --gitee --limit 3 --max-queries 3
```

没有 token 时：

```text
Gitee 需要 GITEE_TOKEN；已跳过（不静默返回空）
```

## 实现约束

- token 只放 `Authorization: Bearer`，不拼进 URL、不写日志、不进 `state.json`；
- 只搜公开仓库，映射为 `platform=gitee`、`artifact_type=code`、`evidence_level=metadata`、`status=needs_review`；
- 许可证 Gitee 搜索结果常不提供，统一 `license=unknown`、`license_status=needs_review`；
- 不抓正文、不 clone、不加依赖；
- 出错只报告状态码/消息，不回显 token。

## 速率

匿名约 60 请求/分钟；token 提高额度，但仍要加 `--limit` / `--max-queries`，不要全量扫。
