# rumla 1.12.2 逐层还原：Release 说明与真实 SD 文件对照

研究基线：`AMS1.12.2-Stable-v261112.7z`，原作者 `rumla3434`，SHA256 `55a9a927b1552584c603ca4756e40fc59e1c7d20d4a7635a4acf795e89ac1338`。

> 区分三个概念：原版镜像完全相同；独立整合器从组件作者获取二进制；真机兼容性需要另外验证。本文只研究第二种。

## 从压缩包恢复的事实

- 整个 7z 有 352 条文件路径记录，其中安装目录有 **277 个文件**，另外是说明与辅助目录。
- 安装目录主要有 `atmosphere/` 175、`switch/` 36、`bootloader/` 32、`config/` 21、`warmboot_mariko/` 7，以及根目录文件。
- 有 **155 个 IPS**，并非 Atmosphère 官方 ZIP 自带。这部分是独立重建缺失最多的类别。
- 提取了 **47 个原版文本配置**，可在 `reference/config-reference/` 查看。
- 具体文件的路径、字节长度和 SHA256 在 `reference/manifest.json`，不是凭 Release 文字推断。

## Release 说明交叉核对：整合步骤的顺序

1. **基础固件**：Atmosphère 1.12.2 官方 ZIP + 官方 fusee.bin。和原版对照可逐个校验 `package3`、`stratosphere.romfs`、`hbl.nsp` 等。
2. **Hekate**：官方 v6.5.5 Nyx 1.9.5 → easyworld 汉化 ZIP。保留官方英文 `bootloader/sys/nyx.bin.en`。原版中文/英文 Nyx 均有准确 SHA。
3. **整合补丁**：外部 ES、FS、NIM、NFIM IPS，加上 `bootloader/patches.ini`；它们需要版本匹配的可信独立发布或可重现生成脚本。不能用官方 AMS ZIP 假装已包含。
4. **Tesla 基础**：Z 大的 ovlloader、Ultrahand、ovl-sysmodules、EdiZon、sys-clk、StatusMonitor，选定常驻模块极少。保留普通 sys-clk，**不加入极限超频 loader.kip**。
5. **相册工具**：按 Release 说明中固定列表独立下载，包括 Awoo、Checkpoint、DBI、Ascent Toolbox、EdiZon、Goldleaf、JKSV、linkalho、NX-Activity-Log、sphaira、switch-time、Tencent switcher、Tinwoo、wiliwili、N-Xplorer。原版还包括 Atmosphère 自带的 daybreak/haze。
6. **引导工具**：CommonProblemResolver、Lockpick_RCM、TegraExplorer、hwfly、DowngradeFixer、Warmboot_Extractor，附加原版专有启动资源。
7. **配置收口**：`hekate_ipl.ini` 三模式启动项、`more.ini`、`system_settings.ini`、`exosphere.ini`、DNS hosts、Tesla 快捷键/禁用后台、语言资源。
8. **校验与打包**：生成新 7z，保存每一个组件的下载 SHA256，按原版 manifest 做逐路径 SHA256 比对；缺失/不同必须留证据。

## 核实到的原版设置

| 文件 | 实际设置/规则 |
|---|---|
| `bootloader/hekate_ipl.ini` | CFW-SYSNAND、CFW-EMUNAND、OFW-SYSNAND；通过 `pkg3=atmosphere/package3` 引导，使用选定图标 |
| `bootloader/ini/more.ini` | Fusee 入口被注释；附 Lakka、Ubuntu 启动入口 |
| `config/tesla/config.ini` | `key_combo=L+DDOWN` |
| `atmosphere/config/system_settings.ini` | 关闭多项下载/报告相关行为，配置 DNS MITM、作弊默认禁用等 |
| `exosphere.ini` | 设置 `blank_prodinfo_sysmmc=1`、`blank_prodinfo_emummc=1`；操作前应理解其联机风险和兼容性 |
| `atmosphere/hosts/emummc.txt` | Nintendo 域名保护列表及网络连接测试地址 |
| `bootloader/patches.ini` | 原版存在，但独立补丁来源尚未完成，重建器不会拿作者原版直接复制 |

这些配置对应 1.12.2 基线，不应不经测试就覆盖到任意将来的 Atmosphère 系统版本。

## 当前独立构建的精度

- 第一轮：从 33 项上游组件下载生成 130 个文件，92 个 SHA256 与原版完全一致，178 缺失，7 同路径不同。
- 第二轮：修正 `atmosphere/reboot_payload.bin` ← `bootloader/update.bin`、`switch/sys-clk-manager.nro` ← 上游 `switch/sys-clk/sys-clk.nro`，增加 N-Xplorer 组件，清理上游自带而原版不存在的附加文件。
- 第二轮通过结果：**101 个重建文件，94 个 SHA256 一致，7 个相同路径不同，176 个缺失，0 个额外文件**（33.94% 精确覆盖）。第三轮已生成两个零字节 emuMMC 示例标记，正式验收 **103 个重建文件，96 个完全一致，7 个不同，174 个缺失，0 个额外文件（34.66%）**。
- 所有组件下载均成功并留下 `SOURCE_LOCK.json`，不可把组件下载成功误当成包完整复刻。

## 差异消除清单与开发优先级

**P0：影响启动/系统稳定**

- 155 个 IPS 与 `bootloader/patches.ini`：追踪对应 1.12.2 / HOS 23.5.0 的可信来源，校验每个 IPS 的 Build ID 与哈希；不允许拿 1.12.0 的旧补丁冒充适配 1.12.2。
- `warmboot_mariko/wb_13..19.bin`：明确固件熔断版本映射与合法来源，避免睡眠/唤醒故障。
- Hekate 启动图标 `bootloader/res/*.bmp`、`bootloader/bootlogo.bmp` 及对应配置引用：找到可再分发源文件，或改用不引用缺失文件的安全默认配置。

**P1：功能完整性**

- `boot.dat` 和 `sdloader.enc`：确认 SX/HWFLY 引导来源与授权，无法确认则保持排除。
- `hbmenu.nsp`：寻找可信可编译的通用前端项目或生成方案，区分 NSP 前端与 hbmenu.nro。
- `picofly_toolbox.bin`：确认原版对应源码/正式发布资产。
- 6 个二进制哈希差异：`ovlmenu.ovl`、DBI、DeepSeaToolbox、EdiZon、reboot_to_payload、Tencent switcher；检查发行日期和具体编译变种。另有 `hekate_ipl.ini` 因缺少补丁而被主动调整，不能按原版原样使用。

**P2：持续维护**

- 每日监控 34 个源资产的最新 Tag 与锁定 Tag 是否分歧。
- 上游有新版本时先生成待升级清单和候选构建，避免未经真机验证自动将其标为 Stable。
- 建立 Erista/Mariko、HOS 23.0/23.5、sysNAND/emuMMC、启动与休眠、NRO、联网保护的回归矩阵；通过后才考虑提升 Release 状态。

## 工作流链接

- [原版拆包研究](../../actions/workflows/rumla-rebuild-audit.yml)
- [从上游组件独立整合](../../actions/workflows/rumla-rebuild.yml)
- [配置来源清单](../profiles/rumla-1.12.2.json)
- [最新逐文件对比](../reports/LATEST_PARITY.md)
- [最新构建来源报告](../reports/LATEST_SOURCE_LOCK.json)

**禁止**把完全一致的镜像 SHA256 结果当成这套独立构建的验收结果。两条链路是独立的。
