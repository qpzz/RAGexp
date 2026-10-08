import concurrent.futures
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
spec=importlib.util.spec_from_file_location('downloads',str(Path(__file__).with_name('download_papers_2026-09-30.py')))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
TEMP=m.OUT/'下载临时分段'; TEMP.mkdir(exist_ok=True)
targets=[8,10,19,20,37,56]
manifest_name='retry4_manifest.json'
if '--only51' in sys.argv:
    targets=[51]
    manifest_name='retry5_manifest.json'
override={8:'https://arxiv.org/pdf/2405.20539',32:'https://arxiv.org/pdf/2403.02691',37:'https://arxiv.org/pdf/2601.04566',51:'https://arxiv.org/pdf/2508.10991'}

def run(args,limit=100):
    return subprocess.run(['curl.exe','--fail','--location','--silent','--show-error','--connect-timeout','15']+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=limit)

def worker(row):
    dest=m.OUT/('%02d_%s.pdf'%(row['number'],row['name']))
    if dest.exists(): return None
    url=override.get(row['number'],row['candidate_pdf_urls'][0])
    head=run(['--head','--max-time','40',url],50)
    lengths=re.findall(rb'(?im)^content-length:\s*(\d+)',head.stdout)
    if not lengths:
        return {'number':row['number'],'status':'failed','errors':[{'url':url,'error':'No content length for ranged download'}]}
    total=int(lengths[-1]); chunk_size=512*1024
    jobs=[(start,min(start+chunk_size,total)-1) for start in range(0,total,chunk_size)]
    def chunk(bounds):
        start,end=bounds; part=TEMP/('%02d_%010d.part'%(row['number'],start)); need=end-start+1
        data=part.read_bytes() if part.exists() else b''
        if len(data)==need:return data
        for attempt in range(4):
            rr=run(['--range','%d-%d'%(start+len(data),end),'--max-time','75',url],85)
            if len(rr.stdout)==total and rr.stdout.startswith(b'%PDF-'):
                data=rr.stdout[start:end+1]
            elif rr.stdout:
                data+=rr.stdout
            if len(data)>need: raise ValueError('Server did not honor range')
            if data:part.write_bytes(data)
            if len(data)==need:return data
        raise ValueError('Incomplete range '+str(bounds))
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            data=b''.join(pool.map(chunk,jobs))
        assert len(data)==total and data.startswith(b'%PDF-') and b'%%EOF' in data[-4096:]
        dest.write_bytes(data)
        row.update(status='downloaded',file=dest.name,download_url=url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        print('COMPLETE %02d %s %d bytes'%(row['number'],row['name'],len(data)),flush=True)
        return row
    except Exception as e:
        print('FAILED %02d %s'%(row['number'],e),flush=True)
        row.update(status='failed',errors=[{'url':url,'error':str(e)}]); return row

if __name__=='__main__':
    selected=[r for r in m.records if r['number'] in targets]
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(worker,r) for r in selected]
        for future in concurrent.futures.as_completed(futures):
            result=future.result()
            if result:results.append(result)
            (m.OUT/manifest_name).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
