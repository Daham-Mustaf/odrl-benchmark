"""
gen_layer0_signature.py
================
Generates TWO signature files for the FOIS 2026 deontic grounding.
"""
import argparse, textwrap
from pathlib import Path
from datetime import date

META = {
    "domain":  "Deontic Ontology / ODRL Grounding",
    "source":  "Mohammed et al., What Does ODRL Mean? FOIS 2026",
    "version": "1.5",
}

def generate_smt2() -> str:
    from gen_layer0_signature_full import generate_smt2 as _full
    return _full()

def generate_fof() -> str:
    from gen_layer0_signature_full import generate_fof as _full
    return _full()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default="Problems/DeonticOntology/Axioms/Layer0-Signature")
    p.add_argument("--stdout-fof",  action="store_true")
    p.add_argument("--stdout-smt2", action="store_true")
    args = p.parse_args()
    if args.stdout_fof:  print(generate_fof());  return
    if args.stdout_smt2: print(generate_smt2()); return
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "GRND000-0.ax").write_text(generate_fof(),    encoding="utf-8")
    (out / "GRND000-0.smt2").write_text(generate_smt2(), encoding="utf-8")
    print("Written GRND000-0.ax and GRND000-0.smt2")

if __name__ == "__main__":
    main()
