# 投资研究文档：首版正文恢复与历史备份

**请优先阅读下方恢复的首版完整正文。此前的删减重建版已保留为历史，不再作为阅读主版本。**

恢复日期：2026-11-04（UTC+8）。本次按聊天中首次写入文件的完整正文恢复，没有概括、删减或添加投资结论。

## 首版完整文件

| 文件 | 恢复与核验情况 | 阅读入口 |
|---|---|---|
| 中长线投资方法提炼 v0.1 | 41,609 字节，SHA-256 与首次历史记录完全一致 | [打开全文](archive/restored-originals/中长线投资方法提炼-v0.1.md) |
| 中长线投资方法提炼 v0.2 | 70,802 字节，27,507 字符，SHA-256 与首次历史记录完全一致；完整独立正文，包含第 0—19 节 | [打开全文](archive/restored-originals/中长线投资方法提炼-v0.2.md) |
| 宏观补充 00：股债汇商品与对冲 | 按首版写入正文恢复，6,741 字符，与历史字符数一致；此前没有记录可比对的 SHA-256 | [打开全文](archive/restored-originals/宏观补充00-股债汇商品与对冲的底层关系.md) |
| 宏观补充 01：美国经济与全球传导 | 按首版写入正文恢复，10,452 字符，与历史字符数一致；此前没有记录可比对的 SHA-256 | [打开全文](archive/restored-originals/宏观补充01-美国经济的运行与全球传导.md) |

**[下载首版全文 ZIP 包](downloads/stock-research-first-editions-restored-2026-11-04.zip)**。打开文件页面后选择 **Download raw file**；单份 Markdown 页面也可通过该按钮下载。私有仓库需登录有权限的 GitHub 账号。

也可使用仓库首页 **Code → Download ZIP** 下载全部当前文件，包含历史重建版。

## 阅读顺序与冻结约定

- 学习顺序：宏观补充 00 → 宏观补充 01 → 投资方法报告。
- v0.2 是独立完整报告，阅读它不依赖删减重建版或另一本报告。
- v0.1、v0.2 作为历史原文冻结保存，包括原文当时的状态说明；新理解、纠错与扩展另建章节或新版本。
- 宏观章节为教学机制，不是当前行情或近期日历的实时核验。
- 后续不以“优化表达”“重建”等理由删减已冻结成果。
- 本仓库没有后台自动同步；后续处理文件时通过明确的 Git 提交备份。

## 核验依据

- [恢复清单与完整性检查](restoration-manifest.json)
- [首次记录的历史校验值](archive/restored-originals/历史版本校验记录.json)
- [全部当前正文校验](SHA256SUMS)
- [恢复包校验](downloads/first-editions-SHA256SUMS)
- [恢复包构建脚本](scripts/build_restored_archive.py)

两份投资报告已达到历史字节级一致；宏观两篇没有历史哈希，只声明聊天正文恢复及字符数一致，不把本次新计算的哈希冒充历史核验。

原上传 PDF/Word 及原始提取文本和图片尚未恢复，不在本次包内。恢复正文不等于重新读取原附件，也不等于外部事实核验或回测通过。

## 此前删减重建版（历史留存）

以下文件和旧 ZIP 内容保持不变，供追溯，不代替上面的首版全文：

- [v0.1 删减重建版](reports/01-investment-framework-v0.1-reconstructed.md)
- [v0.2 删减重建版](reports/02-investment-framework-v0.2-reconstructed.md)
- [宏观 00 删减重建版](reports/03-macro-00-assets-and-hedging-reconstructed.md)
- [宏观 01 删减重建版](reports/04-macro-01-us-economy-reconstructed.md)
- [旧重建版 ZIP](downloads/stock-research-reconstructed-2026-11-04.zip)
- [旧重建时的清单](reconstruction-manifest.json)，其中“原件未恢复”为当时状态；当前状态以上方恢复清单为准。

旧脚本 `scripts/build_archive.py` 仅用于旧重建包，会重写旧产物，不适用于更新首版恢复包。首版恢复包使用 `python3 scripts/build_restored_archive.py`。
