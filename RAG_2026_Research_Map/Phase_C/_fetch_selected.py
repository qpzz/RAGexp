import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

root=Path(r"E:\AgentBackdoorAttack\RAG_2026_Research_Map\Phase_C")
pdfdir=root/"source_pdfs"
pdfdir.mkdir(exist_ok=True)
manifest=root/"selected_papers.csv"
with manifest.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
columns=list(rows[0])
curl=r"C:\ProgramData\Anaconda3\Library\bin\curl.exe"

def fetch(row):
    pid=row["论文ID"]; url=row["PDF地址"]
    if not url: return pid,"MISSING_URL",0,""
    target=pdfdir/(pid+".pdf"); part=pdfdir/(pid+".part")
    if target.exists() and target.stat().st_size>20000 and target.read_bytes()[:4]==b"%PDF":
        return pid,"DOWNLOADED",target.stat().st_size,"cached"
    cmd=[curl,"-C","-","-L","--fail","--silent","--show-error","--retry","1","--connect-timeout","15","--max-time","120",url,"-o",str(part)]
    run=subprocess.run(cmd,capture_output=True,text=True)
    if run.returncode==0 and part.exists() and part.stat().st_size>20000 and part.read_bytes()[:4]==b"%PDF":
        part.replace(target)
        return pid,"DOWNLOADED",target.stat().st_size,""
    return pid,"FAILED",part.stat().st_size if part.exists() else 0,(run.stderr or "")[:220].replace("\n"," ")

results={}
with ThreadPoolExecutor(max_workers=4) as ex:
    futures={ex.submit(fetch,row):row["论文ID"] for row in rows}
    for fut in as_completed(futures):
        pid,status,size,error=fut.result()
        results[pid]=(status,size,error)
        print(f"{pid}\t{status}\t{size}\t{error}",flush=True)
for row in rows:
    status,size,error=results[row["论文ID"]]
    row["PDF取得状态"]=status
    row["阅读状态"]="待阅读" if status=="DOWNLOADED" else "PDF未取得"
    if error: row["保留/替换说明"]="首轮入选；"+error
with manifest.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
print("DONE",sum(v[0]=="DOWNLOADED" for v in results.values()),"/",len(results),flush=True)
