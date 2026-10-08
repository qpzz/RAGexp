import concurrent.futures
import hashlib
import json
import re
import time
import subprocess
from pathlib import Path
import requests

ROOT = Path('E:/AgentBackdoorAttack')
OUT = ROOT / 'Agent后门攻击_七方向十二子方向_论文PDF_2026-09-30'
OUT.mkdir(exist_ok=True)
REPORT = ROOT / 'Agent后门攻击_2020-2026问题演进脉络与创新选题_开题调研报告_2026-09-29.md'
NAMES = ['TrojDRL','BACKDOORL','Temporal-Pattern-Backdoor','Weight-Poisoning-RIPPLe','BadPre','BadPrompt','Backdoor-In-Context-Learning','SleeperNets','Adversarial-Inception','Indirect-Prompt-Injection','RAG','ReAct','Reflexion','BadAgent','BadChain','AgentPoison','Watch-Out-for-Your-Agents','MINJA','MemoryGraft','MemMorph','OEP','MEMOREPAIR','TMA-NM','MemTX','MemSecBench','Revoked-but-Still-Authoritative','Forgetting-Without-Restarting','Prompt-Infection','Flooding-Manipulated-Knowledge','AiTM-Communication-Attacks','PlanFlip','InjecAgent','AgentDojo','MCPTox','MCP-ITP','GhostSplice','BackdoorAgent','ShieldMCP','Mandela-Effect','CAMA','CPB','Silence-Is-Endorsement','Authorization-Revocation','From-Approval-to-Execution','Verified-Tool-Calls','Microsoft-MCP-Docs','MemGPT','Sleeper-Agents','Spotlighting','CaMeL','MCP-Guard','MCP-SafetyBench','VSCode-Issue','Selective-Revalidation','Zombie-Agents','Sleeper-Memory-Poisoning']
OVERRIDES = {
  1: ['https://arxiv.org/pdf/1903.06638'],
  2: ['https://www.ijcai.org/proceedings/2021/0509.pdf'],
  9: ['https://proceedings.mlr.press/v267/rathbun25a/rathbun25a.pdf'],
  12:['https://openreview.net/pdf?id=WE_vluYUL-X','https://arxiv.org/pdf/2210.03629'],
  34:['https://ojs.aaai.org/index.php/AAAI/article/download/40895/44856']
}
GROUPS = {
 'D1 工具结果的多表示消费':[32,33,34,35,36,38,49,50,51,52,56],
 'D2 修复后再进入':[18,19,22,23,24,25,26,27,28,30,31,43,55],
 'D3 证据支持关系变化':[22,23,24,26,39,40,41,43,54],
 'D4 经验组合与迁移':[19,20,21,22,25,43,44],
 'D5 选择性修复':[22,23,24,25,26,27],
 'D6 非原子工具事件':[19,21,32,33,45],
 'D7 持久后门因果判定':[16,18,25,27,37,55,56]
}

def candidates(number, urls):
    if number in OVERRIDES:
        return OVERRIDES[number]
    result=[]
    for u in urls:
        if 'arxiv.org/abs/' in u: result.append(u.replace('/abs/','/pdf/'))
        elif 'aclanthology.org/' in u: result.append(u.rstrip('/')+'.pdf')
        elif '/hash/' in u and '-Abstract' in u:
            result.append(u.replace('/hash/','/file/').replace('-Abstract','-Paper').replace('.html','.pdf'))
        elif u.lower().endswith('.pdf'): result.append(u)
    return list(dict.fromkeys(result))

records=[]
for line in REPORT.read_text(encoding='utf-8-sig').splitlines():
    m=re.match(r'^\[(\d+)\] (.*)',line)
    if not m: continue
    number=int(m[1]); citation=m[2]
    urls=re.findall(r'https?://[^\s；]+', citation)
    records.append({'number':number,'name':NAMES[number-1],'citation':citation,'source_urls':urls,
                    'candidate_pdf_urls':candidates(number,urls),'status':'non-paper' if number in (46,53) else 'pending'})

def download(item):
    if item['status']=='non-paper': return item
    target=OUT / ('%02d_%s.pdf' % (item['number'],item['name']))
    item['file']=target.name
    if target.exists() and target.read_bytes().startswith(b'%PDF-'):
        item.update(status='downloaded',bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        return item
    errors=[]
    for url in item['candidate_pdf_urls']:
        try:
            r=subprocess.run(['curl.exe','--fail','--location','--silent','--show-error','--connect-timeout','15','--max-time','90',url],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=100)
            if r.returncode: raise ValueError(r.stderr.decode('utf-8',errors='replace').strip())
            data=r.stdout
            if not data.lstrip().startswith(b'%PDF-'): raise ValueError('Response is not a PDF')
            if b'%%EOF' not in data[-4096:]: raise ValueError('PDF ending marker missing')
            target.write_bytes(data)
            item.update(status='downloaded',download_url=url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
            print('%02d OK %s (%d bytes)'%(item['number'],item['name'],len(data)),flush=True)
            return item
        except Exception as e: errors.append({'url':url,'error':str(e)})
    item.update(status='failed',errors=errors)
    print('%02d FAILED %s'%(item['number'],item['name']),flush=True)
    return item

if __name__=='__main__':
    old=OUT/'download_manifest.json'
    if old.exists():
        prior={x['number']:x for x in json.loads(old.read_text(encoding='utf-8'))}
        for item in records:
            if item['number'] in prior and prior[item['number']]['status']=='downloaded': item.update(prior[item['number']])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results=list(executor.map(download,records))
    old.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 论文 PDF 下载清单','', '对应 2026-09-29 开题调研报告的参考文献编号；保存日期：2026-09-30。',
           '范围包含七类方向的直接近邻以及原调研中的历史脉络、基础与防御文献。官方网页资料不伪装成论文 PDF。',
           '文件名使用“原参考文献编号_简称”，同一篇仅保存一份；实际下载版本以链接及 PDF 首页为准。',
           '下载状态仅表示文件已获取；文献身份核查结果见随后生成的核验文件。','',
           '| 编号 | 简称 | 状态 | 文件或说明 |','| --- | --- | --- | --- |']
    for item in results:
        status={'downloaded':'已下载','failed':'下载失败','non-paper':'非论文网页'}[item['status']]
        desc=('[PDF](./'+item['file']+')') if item['status']=='downloaded' else ('；'.join(item['source_urls']))
        lines.append('| %02d | %s | %s | %s |'%(item['number'],item['name'],status,desc))
    lines.extend(['','# 七类方向对应的重点阅读编号',''])
    for group, nums in GROUPS.items(): lines.append('- '+group+'：'+', '.join('%02d'%n for n in nums))
    lines.extend(['','# 原始著录与下载来源',''])
    for item in results:
        lines.append('[%d] %s'%(item['number'],item['citation']))
        if item.get('download_url'): lines.append('下载链接：'+item['download_url'])
        if item.get('errors'): lines.append('失败记录：'+json.dumps(item['errors'],ensure_ascii=False))
        lines.append('')
    (OUT/'下载清单与方向索引.md').write_text('\n'.join(lines),encoding='utf-8-sig')
    print(json.dumps({'downloaded':sum(x['status']=='downloaded' for x in results),'failed':sum(x['status']=='failed' for x in results),'non-paper':2,'folder':str(OUT)},ensure_ascii=False),flush=True)
