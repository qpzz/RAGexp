import csv
import importlib.util
import re
from pathlib import Path

root = Path(__file__).parent
spec = importlib.util.spec_from_file_location('phase_c_cards', root / '_cards_data.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
cards = {x['id']: x for x in mod.CARDS}

manifest = root / 'selected_papers.csv'
with manifest.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == len(cards) == 27
assert {r['论文ID'] for r in rows} == set(cards)

alternate_pdfs = {
    'zhao26bk': 'https://arxiv.org/pdf/2605.00529',
    'sun26p': 'https://arxiv.org/pdf/2602.03689',
    'cui26i': 'https://arxiv.org/pdf/2508.19282',
    'hu26ac': 'https://arxiv.org/pdf/2602.05152',
    'www26-3792361': 'https://me.sage.org.ai/contents/research_papers/2026/2026_flowrag_www_2026.pdf',
}
for row in rows:
    pid = row['论文ID']
    pdf = root / 'source_pdfs' / (pid + '.pdf')
    text = root / 'source_text' / (pid + '.txt')
    assert pdf.exists() and pdf.stat().st_size > 20000 and pdf.read_bytes()[:4] == b'%PDF', pid
    assert text.exists() and len(text.read_text(encoding='utf-8')) > 15000, pid
    row['PDF取得状态'] = 'DOWNLOADED'
    row['阅读状态'] = '首轮全文核读；未证实字段标 UNKNOWN'
    row['实际阅读PDF地址'] = alternate_pdfs.get(pid, row['PDF地址'])
    row['实际PDF页数'] = str(len(re.findall(r'^========== PDF PAGE ', text.read_text(encoding='utf-8'), re.M)))
    if pid in alternate_pdfs:
        row['保留/替换说明'] = '正式发表由官方页确认；全文采用 arXiv/作者版阅读并核对首页标题' if pid != 'www26-3792361' else 'ACM 正式页确认；全文采用作者版阅读'
    elif pid == 'sigir26-3809631':
        row['保留/替换说明'] = 'DOI 与机构记录确认；全文为作者版；出版社正文未取得'
    else:
        row['保留/替换说明'] = '官方论文集 PDF 正文已读'
    row['正式发表核验'] = 'DOI/作者版；出版社正文未取得' if pid == 'sigir26-3809631' else '官方论文集或出版社条目已核验'

fields = list(rows[0])
with manifest.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

lines = [
    '# Phase C 代表论文首轮阅读卡',
    '',
    '日期：2026-10-14；仅分析 `selected_papers.csv` 中来自既有核心池的 27 篇。页码是本地 PDF 的顺序页码，不一定等于正式论文集连续页码。PMLR 部分全文采用标题一致的 arXiv 版本；CoRM-RAG 和 FlowRAG 使用作者版，版本差异风险见分类审计。',
    '',
    '阅读范围：摘要、引言、方法及框架图的图注与相邻解释、实验总表、结论、可定位的作者局限。`UNKNOWN` 表示本轮无法由已读正文可靠核实，不能解释为事实不存在。表中“相比变化”是对作者自述与其引用前人的比较，不构成创新性评价。',
    '',
]
current = None
for row in rows:
    group = row['方向代码']
    if group != current:
        lines += [f'## {group} 类', '']
        current = group
    pid = row['论文ID']
    c = cards[pid]
    pdf_link = f'source_pdfs/{pid}.pdf'
    lines += [
        f"### {row['标题']}（{row['发表渠道']}，{group}）",
        '',
        f"正式来源：[论文页]({row['官方论文地址']})；[本地 PDF]({pdf_link})。{row['保留/替换说明']}。",
        '',
        f"- **研究问题**：{c['problem']}",
        f"- **核心方法与框架图**：{c['method']} 技术路线：{c['route']}。",
        f"- **相对既有工作的变化**：{c['delta']}",
        f"- **实际数据集／指标**：{c['data']}；{c['metrics']}。",
        f"- **主要对比基线**：{c['baseline']}",
        f"- **主实验结论**：{c['result']}",
        f"- **作者承认的局限**：{c['limit']}",
        f"- **可追溯依据**：{c['evidence']}；[全文链接]({row['实际阅读PDF地址']})。",
        '',
    ]
(root / 'paper_reading_cards.md').write_text('\n'.join(lines), encoding='utf-8')

csv_fields = ['方向代码','论文ID','标题','发表渠道','技术路线','数据集','评价指标','最重要基线','主要实验结果','作者局限','证据位置','官方论文地址','本地PDF','全文版本']
with (root / 'datasets_metrics_baselines.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=csv_fields)
    writer.writeheader()
    for row in rows:
        pid = row['论文ID']; c = cards[pid]
        writer.writerow({
            '方向代码': row['方向代码'], '论文ID':pid, '标题':row['标题'], '发表渠道':row['发表渠道'],
            '技术路线':c['route'], '数据集':c['data'], '评价指标':c['metrics'], '最重要基线':c['baseline'],
            '主要实验结果':c['result'], '作者局限':c['limit'], '证据位置':c['evidence'],
            '官方论文地址':row['官方论文地址'], '本地PDF':f'source_pdfs/{pid}.pdf',
            '全文版本':'作者版' if pid.startswith('www26') or pid.startswith('sigir26') else ('arXiv 副本' if pid in alternate_pdfs else '正式论文集 PDF'),
        })
print('rendered', len(rows), 'cards; CSVs utf-8-sig')
