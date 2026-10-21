from pathlib import Path
import re, sys

root=Path(__file__).parent/'source_text'
for pid in sys.argv[1:]:
    p=root/(pid+'.txt')
    if not p.exists():
        print('\n===== '+pid+' NO LOCAL PDF =====')
        continue
    text=p.read_text(encoding='utf-8',errors='replace')
    print('\n===== '+pid+' =====')
    for label,pat in [
      ('FIGURE',r'Figure\s+[12]\s*:'),
      ('DATASETS',r'(?:\d+(?:\.\d+)?\s+)?(?:Datasets?\s+and\s+Metrics|Dataset\s+Description|Experimental\s+Setup|Experiment\s+Setup|Evaluation\s+Setup|Datasets?\.)'),
      ('BASELINES',r'(?:Baselines?|Comparison Models|Compared Methods)\s*[.:]'),
      ('MAIN_TABLE',r'Table\s+1\s*:'),
      ('CONCLUSION',r'(?:\d+\s+)?Conclusions?\s*\n'),
      ('LIMITATIONS',r'(?:\d+\s+)?Limitations?\s*\n')]:
        ms=list(re.finditer(pat,text,re.I))
        if not ms:
            print(label+': UNKNOWN')
            continue
        m=ms[-1] if label in ('CONCLUSION','LIMITATIONS') else ms[0]
        before=text[:m.start()]
        pg=re.findall(r'PDF PAGE (\d+)',before)
        excerpt=re.sub(r'\s+',' ',text[m.start():m.start()+700])
        print(f'{label} [PDF p.{pg[-1] if pg else "?"}]: {excerpt[:700]}')
