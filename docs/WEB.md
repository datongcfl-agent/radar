# --web：网页正文抽取 + 最小许可提示

## 做什么

- 对 `platform=web/docs` 的已选来源抓公开 HTML；
- 用 stdlib `html.parser` 提取 title / meta description / 正文 / 短引用；
- 从正文里做最小许可提示：MIT、Apache-2.0、GPL、AGPL、LGPL、MPL、BSD、Unlicense、CC0、proprietary；
- 更新 `quotes`、`license`、`license_status`、`web_text_chars`、`last_seen`；
- 默认不读 robots；加 `--respect-robots` 才检查。

```bash
python3 -m radar run --pack packs/weak-current/pack.json \
  --seeds seeds/weak-current.json --title "弱电管理系统" \
  --out runs/web-demo --web --web-limit 5 --respect-robots
```

需要本机有 `curl`；没有会在启动时直接报错，不会逐条伪装成 `web_error`。

## 不做什么

- 不执行 JS，不处理登录/付费/验证码；
- 不解析 PDF/图片（OCR 后续）；
- 许可识别是**提示**，不是法律结论；只认强信号（完整首句 / `licensed under` / `/license`），弱提及保持 `needs_review`；
- 不因为抓到正文就自动把来源升级成 `strong`；单源上限仍生效；
- 非 2xx 不写 200：404→`deleted`，401→`login_required`，403→`blocked`，并写 `web_error`。

## 失败处理

抓取失败保留原来源，写 `web_error` 并进 warning；不把失败当“0 结果”。
