import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT=Path('E:/AgentBackdoorAttack')
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
OUT=ROOT/'Agent后门攻击_七方向十二子方向_论文PDF_2026-09-30'
VENDOR=ROOT/'report-work'/'vendor'

def fetch(url):
    r=subprocess.run(['curl.exe','--fail','--location','--silent','--show-error','--connect-timeout','15','--max-time','60',url],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=70)
    if r.returncode: raise RuntimeError(r.stderr.decode(errors='replace'))
    return r.stdout

def install_wheel(package,version):
    meta=json.loads(fetch('https://pypi.org/pypi/'+package+'/'+version+'/json'))
    wheel=next(x for x in meta['urls'] if x['filename'].endswith('.whl'))
    data=fetch(wheel['url'])
    import hashlib
    assert hashlib.sha256(data).hexdigest()==wheel['digests']['sha256']
    VENDOR.mkdir(exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in z.namelist():
            target=(VENDOR/name).resolve()
            if VENDOR.resolve() not in target.parents: raise ValueError('Unsafe wheel path')
        z.extractall(VENDOR)
if not (VENDOR/'pypdf').exists(): install_wheel('pypdf','5.9.0')
if not (VENDOR/'typing_extensions.py').exists(): install_wheel('typing_extensions','4.15.0')
sys.path.insert(0,str(VENDOR))
from pypdf import PdfReader
results=[]
cached_path=OUT/'PDF核验记录.json'
cached={x['file']:x for x in json.loads(cached_path.read_text(encoding='utf-8'))} if cached_path.exists() else {}
for path in sorted(OUT.glob('*.pdf')):
    previous=cached.get(path.name)
    if previous and previous.get('parse_ok') and previous.get('bytes')==path.stat().st_size:
        results.append(previous)
        continue
    try:
        reader=PdfReader(str(path))
        first='\n'.join((p.extract_text() or '') for p in reader.pages[:2])
        item={'file':path.name,'bytes':path.stat().st_size,'pages':len(reader.pages),'metadata_title':str((reader.metadata or {}).get('/Title','')),'first_pages_text':first[:13000],'parse_ok':True}
        print(path.name+' | '+str(item['pages'])+' pages | '+first[:220].replace('\n',' '),flush=True)
    except Exception as e: item={'file':path.name,'parse_ok':False,'error':str(e)}
    results.append(item)
(OUT/'PDF核验记录.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('PARSED',len(results),'ERRORS',sum(not x['parse_ok'] for x in results),flush=True)
