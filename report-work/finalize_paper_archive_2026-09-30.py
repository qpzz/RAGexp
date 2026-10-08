import csv
import hashlib
import html
import importlib.util
import json
import re
from pathlib import Path

spec=importlib.util.spec_from_file_location('downloads',str(Path(__file__).with_name('download_papers_2026-09-30.py')))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
out=m.OUT
rows=json.loads((out/'download_manifest.json').read_text(encoding='utf-8'))
for manifest in sorted(out.glob('retry*_manifest.json')):
    for new in json.loads(manifest.read_text(encoding='utf-8')):
        if new['status']=='downloaded':
            rows=[new if x['number']==new['number'] else x for x in rows]
checks={x['file']:x for x in json.loads((out/'PDF核验记录.json').read_text(encoding='utf-8'))}
for row in rows:
    name='%02d_%s.pdf'%(row['number'],row['name'])
    path=out/name
    if path.exists():
        row.update(status='downloaded',file=name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        row['pages']=checks.get(name,{}).get('pages')
        row['parse_ok']=checks.get(name,{}).get('parse_ok',False)
        if not row.get('download_url'): row['download_url']=row['candidate_pdf_urls'][0]
    if row['number']==18:
        row['bibliographic_note']='原报告的 MINJA 题名为简称；PDF 正式题名：Memory Injection Attacks on LLM Agents via Query-Only Interaction。'
    if row['number']==1:
        row['bibliographic_note']='保存的是 2019 年 arXiv 预印本；对应后续 DAC 2020 工作，预印本与正式版题名不同。'
(out/'download_manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'下载清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
    fields=['number','name','status','file','pages','bytes','download_url','bibliographic_note','citation']
    writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); writer.writeheader(); writer.writerows(rows)
good=sum(x['status']=='downloaded' for x in rows)
failed=[x for x in rows if x['status']=='failed']
lines=['# 论文 PDF 下载清单与方向索引','',
       '保存日期：2026-09-30。对应原开题调研报告的 56 个参考条目：54 篇论文、2 项非论文网页。',
       '本目录包含七类方向的直接近邻、相关防御，以及调研所用历史脉络和基础论文。',
       '已保存 %d 篇 PDF；未下载成功 %d 篇；非论文网页 2 项。'%(good,len(failed)),
       '文件编号对应原报告参考文献编号。会议正式版、作者公开版本和 arXiv 预印本均可能采用；具体版本以下载链接和 PDF 首页为准。',
       '已下载文件的 PDF 结构、页数及前两页文本核验记录保存在 PDF核验记录.json；下载来源、文件校验值与状态见 download_manifest.json。',
       'MINJA 的正式题名为 Memory Injection Attacks on LLM Agents via Query-Only Interaction，原报告中的 MINJA: Memory Injection Attack on LLM Agents 是不准确的简写，引用时应使用正式题名。','',
       '## 七类方向对应的重点阅读编号','']
for group,ids in m.GROUPS.items():
    links=[]
    for i in ids:
        row=next(x for x in rows if x['number']==i)
        links.append('[%02d %s](./%s)'%(i,row['name'],row['file']) if row['status']=='downloaded' else '%02d %s（未下载）'%(i,row['name']))
    lines.append('- '+group+'：'+'；'.join(links))
lines.extend(['','## 完整清单','','| 编号 | 名称 | 状态 | PDF | 页数 |','| --- | --- | --- | --- | --- |'])
body=[]
for row in rows:
    state={'downloaded':'已下载','failed':'未下载成功','non-paper':'非论文网页'}[row['status']]
    link='[打开](./%s)'%row['file'] if row['status']=='downloaded' else '；'.join(row['source_urls'])
    lines.append('| %02d | %s | %s | %s | %s |'%(row['number'],row['name'],state,link,row.get('pages','')))
    hlink='<a href="'+html.escape(row['file'])+'">打开 PDF</a>' if row['status']=='downloaded' else '<a href="'+html.escape(row['source_urls'][0])+'">原始网页</a>'
    body.append('<tr><td>%02d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(row['number'],html.escape(row['name']),state,hlink,row.get('pages','')))
lines.extend(['','## 原始著录与下载来源',''])
for row in rows:
    lines.extend(['[%d] %s'%(row['number'],row['citation']), ''])
    if row.get('download_url'): lines.extend(['实际下载链接：'+row['download_url'],''])
    if row.get('bibliographic_note'): lines.extend(['著录说明：'+row['bibliographic_note'],''])
    if row['status']=='failed': lines.extend(['未下载成功：'+json.dumps(row.get('errors',[]),ensure_ascii=False),''])
(out/'下载清单与方向索引.md').write_text('\n'.join(lines),encoding='utf-8-sig')
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>论文 PDF 索引</title><style>body{font-family:Segoe UI,Microsoft YaHei,sans-serif;max-width:1100px;margin:36px auto;line-height:1.6}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:8px;text-align:left}th{background:#eef3f8}a{color:#1252a0}</style><h1>Agent 后门攻击论文 PDF 索引</h1><p>已保存 '+str(good)+' 篇；未下载成功 '+str(len(failed))+' 篇。编号对应原报告参考文献。</p><p>七类方向的阅读映射和著录修正见同目录“下载清单与方向索引.md”。</p><table><tr><th>编号</th><th>名称</th><th>状态</th><th>文件</th><th>页数</th></tr>'+''.join(body)+'</table></html>'
(out/'打开论文索引.html').write_text(page,encoding='utf-8')
print(json.dumps({'downloaded':good,'failed':[(x['number'],x['name']) for x in failed],'parse_errors':[x['file'] for x in rows if x['status']=='downloaded' and not x.get('parse_ok')]},ensure_ascii=False))
