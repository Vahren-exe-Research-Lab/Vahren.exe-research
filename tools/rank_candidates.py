#!/usr/bin/env python3
"""Read-only ranking of unregistered VA references using saved reports and native V9 evidence."""
import argparse,csv,re,sqlite3,math,collections
from pathlib import Path
KB=Path(__file__).resolve().parents[1]
ROOT=KB.parent
DEFAULT_DB=KB/"generated/research.sqlite"
DEFAULT_V9=ROOT/"rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite"
OUTPUT=KB/"generated/candidate_priorities.tsv"
PROTECTED=(0x5710C0,0x571500)
DOMAINS={
 "戦闘":r"戦闘|battle|combat|簡略戦闘|攻防|damage|unit",
 "技能":r"技能|スキル|skill|魔法|射程|ダメージ|回復|status.effect",
 "AI":r"(?<![a-z])ai(?![a-z])|cpu|思考|標的|目標|target",
 "経験値":r"経験値|exp|level|レベル|召喚|summon|spawn",
 "戦略":r"戦略|内政|territory|領地|陣営|勢力|マップ|雇用|recruit",
 "画面UI":r"画面|ui|gui|input|mouse|描画|選択|ウィンドウ|window|audio",
 "セーブ":r"save|load|セーブ|永続|変数|variable|serialize",
 "イベント":r"event|イベント|random|乱数|命令|script|expression",
}
PAT={k:re.compile(v,re.I) for k,v in DOMAINS.items()}
COLUMNS=["rank","va","tier","score","kind","domains","report_count","source_families",
 "mentions","native_call_sites","verified_native_calls","v9_function",
 "pseudocode","function_size","example_path","example_line","example_original_va","example_heading","reason"]
def ro(p):
 p=Path(p)
 if not p.is_file():raise FileNotFoundError(p)
 return sqlite3.connect(p.resolve().as_uri()+"?mode=ro&immutable=1",uri=True)
def family(p):
 if p.startswith("rea_lab/"):return "Ghidra"
 if p.startswith("dev_lab/"):return "Dev"
 if p.startswith("exp_research"):return "EXP"
 return p.split("/",1)[0]
def known():
 return {int(s.split("\t",1)[0],16) for s in (KB/"symbols.tsv").read_text(encoding="utf-8").splitlines() if s.startswith("0x")}
def v9_evidence(path):
 c=ro(path)
 funcs={int(a,16):(int(n or 0),bool(code and len(code)>50))
    for a,n,code in c.execute("SELECT entry_va,size_bytes,pseudoc FROM functions WHERE is_external=0")}
 calls=collections.defaultdict(lambda:[0,0])
 for va,op,verified in c.execute("SELECT target_va,opcode_kind,independently_verified_target FROM native_callsite"):
  if not va:continue
  try:a=int(va,16)
  except ValueError:continue
  calls[a][0]+=1
  if verified==1 and (str(op).upper().startswith("E8") or "CALL" in str(op).upper()):calls[a][1]+=1
 forbidden=set()
 for st,en,fn in c.execute("SELECT start_va,end_va,function_entry_va FROM function_range"):
  try:s,e,a=int(st,16),int(en,16),int(fn,16)
  except ValueError:continue
  if s<=PROTECTED[1] and e>=PROTECTED[0]:forbidden.add(a)
 c.close()
 return funcs,calls,forbidden
def rank(db=DEFAULT_DB,v9=DEFAULT_V9):
 seen=known()
 funcs,calls,forbidden=v9_evidence(v9)
 c=ro(db)
 grouped={}
 for va,original,kind,path,line,heading in c.execute("""
    SELECT m.normalized_va,m.va,m.kind,m.path,m.line_no,l.heading
    FROM mentions m JOIN doc_lines l ON l.id=m.line_id
    ORDER BY m.normalized_va,m.path,m.line_no"""):
  if (va in seen or va in forbidden or not 0x401000<=va<=0x8FFFFF
      or PROTECTED[0]<=va<=PROTECTED[1] or PROTECTED[0]<=original<=PROTECTED[1]):continue
  item=grouped.get(va)
  if item is None:
   item={"hits":0,"docs":set(),"families":set(),"kinds":set(),
         "domains":collections.defaultdict(set),"example":None}
   grouped[va]=item
  item["hits"]+=1;item["docs"].add(path);item["families"].add(family(path));item["kinds"].add(kind)
  if item["example"] is None or (item["example"][2]!=va and original==va):
   item["example"]=(path,line,original,heading)
  context=path+" "+str(heading)
  for category,pattern in PAT.items():
   if pattern.search(context):item["domains"][category].add(path)
 c.close()
 out=[]
 for va,item in grouped.items():
  count=len(item["docs"]);families=len(item["families"]);hits=item["hits"]
  native,verified=calls.get(va,[0,0])
  size,has_pcode=funcs.get(va,(0,False))
  kind="func" if va in funcs else "data" if va>=0x639000 else "code_candidate"
  score=min(100,round(7+10*min(families,4)+4*min(count,9)
      +8*min(math.log2(1+hits),5)/5 +12*(va in funcs)
      +5*min(math.log2(1+native),3)/3
      +9*min(math.log2(1+verified),3)/3+4*bool(item["domains"])))
  tier="UNRANKED"
  domains=sorted(item["domains"],key=lambda d:(-len(item["domains"][d]),d))
  path,line,original,heading=item["example"]
  why=f"資料系統{families};独立文書{count};V9関数先頭{int(va in funcs)};検証CALL{verified}/{native}"
  out.append(dict(va=f"0x{va:06X}",tier=tier,score=score,kind=kind,
      domains=",".join(domains),report_count=count,source_families=families,
      mentions=hits,native_call_sites=native,verified_native_calls=verified,
      v9_function=int(va in funcs),pseudocode=int(has_pcode),function_size=size,
      example_path=path,example_line=line,example_original_va=f"0x{original:06X}",
      example_heading=str(heading).replace("\t"," ")[:100],reason=why))
 out.sort(key=lambda x:(-x["score"],-x["verified_native_calls"],
    -x["source_families"],-x["report_count"],int(x["va"],16)))
 # Tiers are bounded review queues, NOT an inferred probability of correctness.
 for position,row in enumerate(out,1):
  row["rank"]=position
  row["tier"]="P0" if position<=100 else "P1" if position<=500 else "P2" if position<=2000 else "P3"
 return out
def write_tsv(items,p=OUTPUT):
 p.parent.mkdir(parents=True,exist_ok=True)
 temp=p.with_suffix(".tsv.tmp")
 with temp.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=COLUMNS,delimiter="\t",lineterminator="\n")
  w.writeheader();w.writerows(items)
 temp.replace(p)
def write_md(items,p):
 totals=collections.Counter(x["tier"] for x in items)
 lines=["# 未登録アドレス候補・重要度評価（未検証）","",
  "このスコアは調査の優先順位であり、関数の意味・実機動作・静的確認の確度を示さない。P0は最初の100件、P1は次の400件、P2は次の1500件。",
  "元データは既存研究文書の行番号と統合V9。新規の逆コンパイル・原作変更なし。",
  "保護対象アドレス（元の言及と所有関数）を除外。辞書への自動追加を禁止。","",
  "候補数: "+str(len(items))+"。 "+", ".join(k+" "+str(totals[k]) for k in ("P0","P1","P2","P3")),
  "","## 全体上位20件","","| VA | tier | score | 資料 | 系統 | V9直接CALL検証 | 分野 |","|---|---|---:|---:|---:|---:|---|"]
 for x in items[:20]:
  lines.append(f"| {x['va']} | {x['tier']} | {x['score']} | {x['report_count']} | {x['source_families']} | {x['verified_native_calls']} | {x['domains']} |")
 for domain in DOMAINS:
  lines+=["","## "+domain+" 上位5件",""]
  subset=[x for x in items if domain in x["domains"].split(",")][:5]
  for x in subset:
   lines.append(f"- {x['va']} [{x['tier']} {x['score']}点] {x['reason']}。"
    f"出典例: {x['example_path']}:{x['example_line']}")
 lines+=["","## 運用","",
  "全件TSV: generated/candidate_priorities.tsv。新しい研究が追加されたら再生成する。",
  "コマンド: python -B kb.py candidates --domain 経験値 --limit 30",
  "実際に利用する前に、根拠の独立確認・動的観測・役割の同定を別途行う。"]
 temp=p.with_suffix(".md.tmp");temp.write_text("\n".join(lines)+"\n",encoding="utf-8");temp.replace(p)
def main():
 a=argparse.ArgumentParser()
 a.add_argument("--db",type=Path,default=DEFAULT_DB)
 a.add_argument("--v9",type=Path,default=DEFAULT_V9)
 a.add_argument("--output",type=Path,default=OUTPUT)
 a.add_argument("--report",type=Path)
 o=a.parse_args();items=rank(o.db,o.v9);write_tsv(items,o.output)
 if o.report:write_md(items,o.report)
 counts=collections.Counter(r["tier"] for r in items)
 print("RANKED",len(items),"TIERS",dict(counts),"OUTPUT",o.output)
 for x in items[:8]:print(x["va"],x["tier"],x["score"],x["report_count"],x["domains"])
if __name__=="__main__":main()

