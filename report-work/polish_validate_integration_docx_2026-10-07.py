from pathlib import Path
import json, re, zipfile
from xml.etree import ElementTree as ET

root = Path('E:/AgentBackdoorAttack')
stem = 'Agent后门攻击_七大方向十二子方向_文献脉络与攻防问题整合稿_2026-10-07'
docx = root / (stem + '.docx')
md = (root / (stem + '.md')).read_text(encoding='utf-8')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
DC = 'http://purl.org/dc/elements/1.1/'
ET.register_namespace('w', W)
ET.register_namespace('r', R)
def w(tag):
    return '{' + W + '}' + tag

with zipfile.ZipFile(docx) as z:
    parts = {name: z.read(name) for name in z.namelist()}
document = ET.fromstring(parts['word/document.xml'])
rels = ET.fromstring(parts['word/_rels/document.xml.rels'])
labels = ['具体机制。', '攻击者做什么。', '利用的系统薄弱点。', '能力边界。', '防御侧做什么。', '实验需要证明。', '实验定位。', '攻击场景。', '方法侧做什么。', '成果定位。', '可纳入的三个场景。']
link_count = 0
bold_count = 0
before = ''.join(node.text or '' for node in document.iter(w('t')))
for p in document.iter(w('p')):
    runs = p.findall(w('r'))
    if len(runs) != 1:
        continue
    run = runs[0]
    txt = run.find(w('t'))
    if txt is None:
        continue
    value = txt.text or ''
    label = next((label for label in labels if value.startswith(label)), None)
    if label:
        txt.text = value[len(label):]
        lead = ET.Element(w('r'))
        props = ET.SubElement(lead, w('rPr'))
        ET.SubElement(props, w('b'))
        ET.SubElement(lead, w('t')).text = label
        p.insert(list(p).index(run), lead)
        bold_count += 1
        continue
    matches = list(re.finditer(r'https?://[^\s；。]+', value))
    if not matches:
        continue
    p.remove(run)
    pos = 0
    for m in matches:
        if pos < m.start():
            plain = ET.SubElement(p, w('r'))
            ET.SubElement(plain, w('t'), {'{http://www.w3.org/XML/1998/namespace}space':'preserve'}).text = value[pos:m.start()]
        link_count += 1
        rid = 'integrationLink' + str(link_count)
        ET.SubElement(rels, '{' + PKG + '}Relationship', {'Id':rid, 'Type':R + '/hyperlink', 'Target':m.group(), 'TargetMode':'External'})
        hyper = ET.SubElement(p, w('hyperlink'), {'{' + R + '}id':rid})
        hyper_run = ET.SubElement(hyper, w('r'))
        props = ET.SubElement(hyper_run, w('rPr'))
        ET.SubElement(props, w('color'), {w('val'):'0563C1'})
        ET.SubElement(props, w('u'), {w('val'):'single'})
        ET.SubElement(hyper_run, w('t')).text = m.group()
        pos = m.end()
    if pos < len(value):
        tail = ET.SubElement(p, w('r'))
        ET.SubElement(tail, w('t'), {'{http://www.w3.org/XML/1998/namespace}space':'preserve'}).text = value[pos:]

for row in document.iter(w('tr')):
    props = row.find(w('trPr'))
    if props is None:
        props = ET.Element(w('trPr'))
        row.insert(0, props)
    ET.SubElement(props, w('cantSplit'))

core = ET.fromstring(parts['docProps/core.xml'])
core.find('{' + DC + '}title').text = 'Agent 后门攻击七大方向、十二子方向：文献脉络与攻防问题整合稿'
core.find('{' + DC + '}subject').text = '已有文献、具体机制、攻击侧与防御侧研究问题'
after = ''.join(node.text or '' for node in document.iter(w('t')))
assert before == after, 'Formatting changed text'
parts['word/document.xml'] = ET.tostring(document, encoding='utf-8', xml_declaration=True)
parts['word/_rels/document.xml.rels'] = ET.tostring(rels, encoding='utf-8', xml_declaration=True)
parts['docProps/core.xml'] = ET.tostring(core, encoding='utf-8', xml_declaration=True)
temporary = docx.with_name(docx.stem + '.formatting.tmp')
with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, data in parts.items():
        z.writestr(name, data)
temporary.replace(docx)

headings = []
paragraphs = []
for p in document.findall('.//' + w('p')):
    text = ''.join(node.text or '' for node in p.iter(w('t')))
    paragraphs.append(text)
    style = p.find(w('pPr') + '/' + w('pStyle'))
    if style is not None and style.attrib.get(w('val')) in ('Heading1', 'Heading2'):
        headings.append(text)
subdirections = [int(m.group(1)) for h in headings if (m := re.search(r'\bS(\d+)：', h))]
assert subdirections == list(range(1,13)), subdirections
direction_chapters = [h for h in headings if re.match(r'^[二三四五六七八]、方向', h)]
assert len(direction_chapters) == 7, direction_chapters
body, refs = md.split('\n## 10.1 引用论文\n')
used = set(re.findall(r'\[(\d+)\]', body))
listed = set(re.findall(r'^\[(\d+)\]', refs, flags=re.M))
assert used == listed and len(used) == 26
for line in md.splitlines():
    stripped = line.strip()
    if not stripped or stripped.startswith('|'):
        continue
    expected = re.sub(r'^#{1,2} ', '', stripped)
    assert expected in paragraphs, expected[:80]
for name, data in parts.items():
    if name.endswith('.xml') or name.endswith('.rels'):
        ET.fromstring(data)
with zipfile.ZipFile(docx) as z:
    assert z.testzip() is None
summary = {'file':str(docx), 'characters':len(md), 'seven_direction_chapters':len(direction_chapters), 'subdirections':subdirections, 'references':len(used), 'tables':len(document.findall('.//' + w('tbl'))), 'hyperlinks':link_count, 'bold_labels':bold_count, 'text_preserved':True, 'xml_and_zip_valid':True, 'rendered_page_check':False}
(root / 'report-work/integration_evidence_2026-10-07/document_validation.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
