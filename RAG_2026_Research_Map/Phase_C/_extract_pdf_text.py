import csv
import os
import sys
from pathlib import Path

root=Path(r"E:\AgentBackdoorAttack\RAG_2026_Research_Map\Phase_C")
sys.path.insert(0,str(root/".deps"))
from pypdf import PdfReader
textdir=root/"source_text"
textdir.mkdir(exist_ok=True)
with (root/"selected_papers.csv").open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
for row in rows:
    path=root/"source_pdfs"/(row["论文ID"]+".pdf")
    if not path.exists(): continue
    try:
        doc=PdfReader(str(path))
        sections=[]
        for index,page in enumerate(doc.pages):
            plain=page.extract_text() or ""
            layout=page.extract_text(extraction_mode="layout") or ""
            text=layout if len(layout)>=len(plain)*0.8 else plain
            sections.append(f"\n\n========== PDF PAGE {index+1} / {len(doc.pages)} ==========\n"+text)
        content="".join(sections)
        (textdir/(row["论文ID"]+".txt")).write_text(content,encoding="utf-8")
        print(row["论文ID"],len(doc.pages),len(content),flush=True)
    except Exception as error:
        print(row["论文ID"],"ERROR",str(error)[:150],flush=True)
