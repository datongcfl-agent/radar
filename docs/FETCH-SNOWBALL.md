# --fetch 与 --snowball

## --fetch

抓公开 URL 的响应头和正文，更新来源状态：

- `http_status`、`last_seen`、`content_hash`、`etag`、`last_modified`；
- 401 → `login_required`，403 → `blocked`，404 → `deleted`；
- 失败保留原记录，写 `fetch_error`；
- `--fetch-limit N` 只抓 N 条，避免一次抓全部。

```bash
python3 -m radar run ... --fetch --fetch-limit 5
python3 -m radar scan ... --since runs/v1 --fetch
```

`--fetch` 用 `curl`，不引入 Python 依赖；不绕过登录/付费/验证码。

## --snowball

从已选 GitHub 来源取 **forks**，作为“谁从它派生”的 forward 信号：

```bash
GITHUB_TOKEN=... python3 -m radar run ... --snowball --snowball-per-source 2 --snowball-max 5
```

- fork 继承 parent 的 `covers`；
- `why_selected=forward: fork of <id>`；
- `evidence_level=metadata`、`status=needs_review`、`quotes=[]` → 最高 `mention`；
- 只读 metadata，不 clone/不读代码。

## 还没做

- GitHub dependents / 引用图；
- Gitee forks；
- 浏览器渲染（登录/JS 页面）。

这些是 v0.3/v0.4 的事，不在本 PR 里假装完成。
