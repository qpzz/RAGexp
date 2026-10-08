import zipfile
import xml.etree.ElementTree as E
from pathlib import Path
paths=[Path('D:/xiazaifile/Agent后门攻击_七大方向核心必读论文_按时间排序.docx'),Path('E:/AgentBackdoorAttack/Agent后门攻击_七类候选研究方向整理_提问式格式_修订版_2026-09-30.docx')]
for path in paths:
    print('\nDOCUMENT:',path.name)
    with zipfile.ZipFile(path) as z:
        root=E.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs=[]
    for p in root.findall('.//w:body//w:p',ns):
        t=''.join(x.text or '' for x in p.findall('.//w:t',ns))
        if t: paragraphs.append(t)
    target=Path('E:/AgentBackdoorAttack/report-work')/(path.stem+'_当前文本.txt')
    target.write_text('\n\n'.join(paragraphs),encoding='utf-8')
    for i,t in enumerate(paragraphs,1): print('[%s] %s'%(i,t))
    print('DRAWINGS:',len(root.findall('.//w:drawing',ns)))
