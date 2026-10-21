from pathlib import Path
import re

root = Path(__file__).parent
outdir = root / "evidence_digests"
outdir.mkdir(exist_ok=True)

for path in sorted((root / "source_text").glob("*.txt")):
    data = path.read_text(encoding="utf-8", errors="replace")
    pages = re.split(r"\n========== PDF PAGE (\d+) / \d+ ==========\n", data)
    chunks = [(int(pages[i]), pages[i+1]) for i in range(1,len(pages)-1,2)]
    lines = []
    if chunks:
        lines.append(f"ID: {path.stem}; PAGES: {len(chunks)}")
        first = chunks[0][1]
        m = re.search(r"\bAbstract\b(.*?)(?:\n1\s+Introduction|\nIntroduction)",first,re.S|re.I)
        lines.append("ABSTRACT [PDF page 1]: " + re.sub(r"\s+"," ",m.group(1) if m else first[:2200])[:3000])
    for page,body in chunks:
        s = body.splitlines()
        for i,line in enumerate(s):
            clean = line.strip()
            if re.match(r"^(?:\d+(?:\.\d+)*\s+)?(?:Method|Approach|Our Method|Experiments?|Results|Conclusion|Limitations|Discussion)\b", clean,re.I):
                lines.append(f"SECTION [PDF p.{page}]: {clean}")
            if re.match(r"^(?:Figure|Fig\.|Table)\s+\d+[.:]",clean,re.I):
                snippet = " ".join(x.strip() for x in s[i:i+4])
                lines.append(f"CAPTION [PDF p.{page}]: {snippet[:420]}")
        if re.search(r"\bLimitations\b",body,re.I):
            for m in list(re.finditer(r"\bLimitations\b",body,re.I))[:2]:
                lines.append(f"LIMITATION [PDF p.{page}]: {re.sub(chr(10),' ',body[m.start():m.start()+1100])[:1100]}")
        if re.search(r"\b(?:outperform|improv|gain|achieve|significant)\b",body,re.I) and (re.search(r"\bExperiment",body,re.I) or re.search(r"\bResults",body,re.I)):
            for sent in re.split(r"(?<=[.!?])\s+",re.sub(r"\s+"," ",body)):
                if re.search(r"\b(?:outperform|improv|gain|achieve)\b",sent,re.I) and re.search(r"\d",sent):
                    lines.append(f"RESULT [PDF p.{page}]: {sent[:500]}")
                    if sum(x.startswith(f"RESULT [PDF p.{page}]") for x in lines)>=3: break
    (outdir/(path.stem+".txt")).write_text("\n".join(lines),encoding="utf-8")
    print(path.stem,len(lines))
