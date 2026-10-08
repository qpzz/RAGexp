import concurrent.futures
import json
import sys
import importlib.util
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
spec=importlib.util.spec_from_file_location('downloads',str(Path(__file__).with_name('download_papers_2026-09-30.py')))
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
alternatives={
8:['https://arxiv.org/pdf/2405.20539v2'],
10:['https://arxiv.org/pdf/2302.12173v2'],
19:['https://arxiv.org/pdf/2512.16962v1'],
20:['https://arxiv.org/pdf/2605.26154v1'],
25:['https://arxiv.org/pdf/2607.27080v1'],
28:['https://arxiv.org/pdf/2410.07283v1']
}
batch='retry2'
if '--batch3' in sys.argv:
    batch='retry3'
    alternatives={
      29:['https://arxiv.org/pdf/2407.07791v1'],
      32:['https://arxiv.org/pdf/2403.02691'],
      37:['https://arxiv.org/pdf/2601.04566'],
      51:['https://aclanthology.org/2026.findings-acl.240.pdf','https://arxiv.org/pdf/2508.10991'],
      56:['https://arxiv.org/pdf/2605.15338v2']
    }
items=[]
for row in mod.records:
    if row['number'] in alternatives:
        row['candidate_pdf_urls']=alternatives[row['number']]
        items.append(row)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(mod.download,items))
(mod.OUT/(batch+'_manifest.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
