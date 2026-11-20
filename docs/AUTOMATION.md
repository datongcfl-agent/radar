# 自动化

## 一键扫描

```bash
./scripts/scan_all.sh
```

- 对 `weak-current` / `video-kb` / `pet-hospital` 各跑一次 `scan`；
- 使用 `--verify-quotes --require-web-verify`；
- 第一次以 `runs/<pack>-demo` 为 base，之后滚动到 `runs/<pack>-last`；
- 输出写入 `runs/<pack>-scan-<timestamp>/`；
- 有变化时脚本最终退出码为 **2**，无变化为 0，失败为 1。

## cron

```cron
0 8 * * 1 cd /path/to/radar && GITHUB_TOKEN=... ./scripts/scan_all.sh >> /tmp/radar-scan.log 2>&1
```

## DSH schedule

用 `schedule_create` 创建每周任务，prompt 示例：

```text
cd /path/to/radar && ./scripts/scan_all.sh
```

## 退出码

| 码 | 含义 |
| ---: | --- |
| 0 | 无变化 |
| 1 | 运行失败 |
| 2 | 有新增/移除/字段变化（产物已写完） |

`scan` 的 `changes.md` / `changes.json` 记录来源级变化，`diff.md` 记录覆盖变化。
