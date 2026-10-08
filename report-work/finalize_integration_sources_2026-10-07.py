from pathlib import Path
import json, re
root = Path('E:/AgentBackdoorAttack')
manuscript = root / 'Agent后门攻击_七大方向十二子方向_文献脉络与攻防问题整合稿_2026-10-07.md'
rows = json.loads((root / 'report-work/integration_evidence_2026-10-07/selected_manifest.json').read_text(encoding='utf-8'))
source = manuscript.read_text(encoding='utf-8')
marker = '\n## 10.1 引用论文\n'
source = source.split(marker)[0]
refs = []
for row in rows:
    citation = row['citation']
    if row['number'] == 34:
        citation += ' 本地保存的是 AAAI-26 正式 PDF，题名含 Tool Poisoning Attack，出版页面题名不含 Attack；按论文身份对应。'
    if row['number'] == 36:
        citation = 'Measuring and Exploiting Implicit Trust in LLM Tool-Calling Pipelines. 2026 预印本；相关公开攻击披露名为 GhostSplice，并非论文题名。https://arxiv.org/abs/2609.18217 作者官方披露：https://asset-group.github.io/disclosures/ghostsplice/ 作者代码：https://github.com/asset-group/ghostsplice'
    refs.append(f"[{row['number']}] {citation}\n\n本地文件：{row['file']}")
manuscript.write_text(source + marker + '\n' + '\n\n'.join(refs) + '\n', encoding='utf-8')
evidence = {
    'task': 'Integrate user-provided seven directions and twelve subdirections',
    'sources': [
        'D:/xiazaifile/Agent后门攻击_七大方向核心必读论文_按时间排序.docx',
        'E:/AgentBackdoorAttack/Agent后门攻击_七类候选研究方向整理_提问式格式_修订版_2026-09-30.docx',
        'User supplied detailed direction 2 and three embedded screenshots in current summary'
    ],
    'fulltext_directory': str(root / 'report-work/integration_evidence_2026-10-07'),
    'chapters': {'D1':[32,33,34,35,36,38], 'D2':[28,22,24,27,26], 'D3':[23,41,54,26], 'D4':[16,19,20,21,25,22], 'D5':[22,24,23], 'D6':[12,13,45], 'D7':[48,8,56,25,37]},
    'proposals_status': 'All proposed mechanisms, attacks, defenses and experiments are untested hypotheses, not findings.',
    'limitations': 'Integration and local fulltext verification; no new comprehensive literature novelty search.'
}
(root / 'report-work/integration_evidence_2026-10-07/evidence_map.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
used = set(map(int, re.findall(r'\[(\d+)\]', source)))
listed = {row['number'] for row in rows}
assert used == listed, (used - listed, listed - used)
print(f'Characters: {len(manuscript.read_text(encoding="utf-8"))}; references: {len(rows)}; subdirections: 12')
