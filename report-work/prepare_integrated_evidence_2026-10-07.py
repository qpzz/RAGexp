from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).parent / 'vendor'))
from pypdf import PdfReader
root = Path('E:/AgentBackdoorAttack')
archive = root / 'Agent后门攻击_七方向十二子方向_论文PDF_2026-09-30'
out = root / 'report-work' / 'integration_evidence_2026-10-07'
out.mkdir(exist_ok=True)
selected = {8, 12, 13, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 32, 33, 34, 35, 36, 37, 38, 41, 45, 48, 54, 56}
manifest = json.loads((archive / 'download_manifest.json').read_text(encoding='utf-8-sig'))
entries = []
for row in manifest:
    if row['number'] not in selected:
        continue
    reader = PdfReader(str(archive / row['file']))
    body = '\n\n'.join(f'--- PAGE {i+1} ---\n{page.extract_text() or ""}' for i, page in enumerate(reader.pages))
    (out / (Path(row['file']).stem + '.txt')).write_text(body, encoding='utf-8')
    entries.append(row)
(out / 'selected_manifest.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
for row in entries:
    print(f"[{row['number']}] {row['citation']}")
