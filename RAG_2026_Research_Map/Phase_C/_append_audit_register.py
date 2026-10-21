import csv
from pathlib import Path

root=Path(__file__).parent
core=list(csv.DictReader((root.parent/'rag_core_papers.csv').open(encoding='utf-8-sig',newline='')))
assert len(core)==61 and all(r['年份']=='2026' for r in core)
path=root/'classification_audit.md'
base=path.read_text(encoding='utf-8').split('\n## 61 篇逐条书目审计索引')[0]
lines=[base,'## 61 篇逐条书目审计索引','',
       '下表列出全部核心记录的 2026 年份、主类和可复核论文页。`原核验记录` 是 Phase A/B 原表字段；除本轮入选 27 篇及另行查证的 SIGIR QPP 外，本轮没有重新精读其余论文全文。`官方/出版社页` 指原阶段已记录相应链接，不能代替重新打开出版社全文。','',
       '|ID|主类|2026 渠道|原核验记录|来源|','|---|---|---|---|---|']
for r in core:
    status=r['发表信息核验状态']
    label='DOI＋作者版；出版社正文不可达' if 'inaccessible' in status else '官方/出版社页（Phase A/B）'
    lines.append(f"|{r['论文ID']}|{r['主要方向代码']}|{r['发表渠道']}|{label}|[记录]({r['官方论文地址']})|")
path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('appended',len(core))
