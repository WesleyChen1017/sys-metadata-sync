import requests as a
import json as b
import re as c
import os as d
import unicodedata as e
import base64 as f
from dotenv import load_dotenv as g
import urllib3 as h
import time as i
import random as j
from datetime import datetime as dt
import subprocess as sp

h.disable_warnings(h.exceptions.InsecureRequestWarning)
g()

k1 = d.getenv("K1")
k2 = d.getenv("K2")
k3 = d.getenv("K3")
k4 = d.getenv("K4")

def en(t): return f.b64encode(str(t).encode()).decode()
def de(t):
    try: return f.b64decode(t.encode()).decode()
    except: return ""

def sync_db():
    try:
        sp.run(["git", "add", k3], check=True)
        ts = dt.now().strftime('%H:%M:%S')
        msg = f"sys-sync: delta at {ts} [skip ci]" 
        sp.run(["git", "commit", "-m", msg], check=True)
        sp.run(["git", "push"], check=True)
        print(f"   > [GIT] Database persisted to remote (CI skipped).")
    except Exception as e_git:
        print(f"   > [GIT] Push skipped or failed: {e_git}")

def u(v):
    if not k1 or not k2: return
    w = d.getenv("K5")
    x = {"Content-Type": "application/json", "Authorization": f"Bearer {k1}"}
    y = {"to": k2, "messages": [{"type": "text", "text": v}]}
    try: a.post(w, headers=x, json=y, verify=False, timeout=20)
    except: pass

def z():
    st = i.time()
    ct = 0 
    while i.time() - st < 9000:
        ct += 1
        now = dt.now().strftime('%H:%M:%S')
        print(f"[{now}] ID_{ct:04d}: Buffer synchronization initiated...", flush=True)
        
        aa = d.getenv("K6")
        ab = {"User-Agent": d.getenv("K7"), "Accept-Language": "zh-TW,zh;q=0.9"}
        try:
            ac = a.get(f"{aa}?v={j.random()}", headers=ab, timeout=15)
            ac.raise_for_status()
            ae = c.compile(d.getenv("K8"), c.DOTALL).search(ac.text)
            if ae:
                ag = b.loads(ae.group(1))
                ah = ag.get("tiles", [])
                ai = {}
                aj_s = {}
                for ak in ah:
                    sk = ak.get("partNumber"); name = ak.get("title", "???")
                    price = ak.get("price", {}).get("currentPrice", {}).get("amount", "N/A")
                    dims = ak.get("filters", {}).get("dimensions", {})
                    ram = dims.get("tsMemorySize", "N/A").upper()
                    ssd = dims.get("dimensionCapacity", "N/A").upper()
                    ai[sk] = {"n": name, "r": ram, "s": ssd, "p": price}
                    aj_s[en(sk)] = {"n": en(name), "r": en(ram), "s": en(ssd), "p": en(price)}

                tc = len(ai)
                print(f"   > Active objects in scope: {tc}", flush=True)

                at = {}
                if d.path.exists(k3):
                    with open(k3, "r", encoding="utf-8") as f_in:
                        r_data = b.load(f_in)
                    at = {de(k_): {nk: de(nv) for nk, nv in v_.items()} for k_, v_ in r_data.items()}

                ar = []
                for sku, info in ai.items():
                    if sku not in at: ar.append(info)
                    elif info['p'] != at[sku]['p']:
                        info['op'] = at[sku]['p']; ar.append(info)

                if ar:
                    uc = len(ar)
                    aw = f"{d.getenv('M1')} (Total: {tc} / +{uc})\n"
                    for ax in ar:
                        aw += f"📦 {ax['n']}\n💎 {ax['r']}/{ax['s']}\n💰 {ax.get('op', '') + ' -> ' if 'op' in ax else ''}{ax['p']}\n---\n"
                    u(aw.strip() + f"\n🔗 {k4}")
                    print(f"   > Metadata delta detected ({uc}). Patching remote node...", flush=True)
                    
                    with open(k3, "w", encoding="utf-8") as az:
                        b.dump(aj_s, az, ensure_ascii=False, indent=4)
                    
                    sync_db()

        except Exception as e_err:
            print(f"   > Warning: Remote endpoint timeout. {e_err}", flush=True)
        
        wt = j.randint(5, 10)
        print(f"   > Cycle {ct:04d} complete. Standby for {wt}s...\n", flush=True)
        i.sleep(wt)

if __name__ == "__main__":
    z()
