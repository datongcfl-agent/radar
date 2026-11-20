# 自动化

## 一键扫描

```bash
./scripts/scan_all.sh
```

- 对 `weak-current` / `video-kb` / `data-center-ops` / `pet-hospital` 各跑一次 `scan`；
- 使用 `--verify-quotes --require-web-verify`；
- 第一次以 `runs/<pack>-demo` 为 base；
- 之后把本次 out 路径写入 `runs/<pack>-last.txt`，下次读这个指针文件；
- 不使用符号链接：Windows/Git Bash 不需要管理员权限；
- 输出写入 `runs/<pack>-scan-<timestamp>/`；
- 退出码：任一 pack 失败为 **1**（优先），否则有变化为 **2**，无变化为 0。

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
| 1 | 至少一个 pack 运行失败（优先于 2） |
| 2 | 有新增/移除/字段变化（产物已写完） |

`scan` 的 `changes.md` / `changes.json` 记录来源级变化，`diff.md` 记录覆盖变化。  
`scan_all.sh` 结束时会打印每个 pack 的退出码，便于定位失败项。
