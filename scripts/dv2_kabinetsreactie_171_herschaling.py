                      
"""
DV2 Kabinetsreactie 171-scope herschaling

Doel:
  Herschaal de bevroren kabinetsreactie-validatieset (421 documenten, 13.253 elementen)
  naar de 171-Kaderwet-scope (dezelfde scope als DV1/CORPUS_KEUZES.md).
  Dit produceert bevrozen in-scope getallen die thesis-claims ondersteunen.

Inputs:
  - PostgreSQL database (via .env PG_* vars): corpus.adviesdocumenten, register.adviescollege_fasen
  - Batch-resultaten: C:/Users/Haady/.../02_kabinetsreactie_batch_capfix_full_20260603/
  - Golden set: C:/Users/Haady/.../06_kabinetsreactie_golden_set_20260604/

Outputs:
  - C:/Users/Haady/.../02b_kabinetsreactie_171_frozen_20260605/
    met: in_scope_documenten.csv, uitval_documenten.csv, golden_171_hertelling.md, _manifest.json

Pijpijnplek:
  - Stap 5 (doorwerking-analyse) van het dataverwerkingsproject: validatiecijfers bevriezen
  - Ondersteunt thesis met in-scope-geverifieerde getallen voor kabinetsreactie-analyse
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
import asyncio
from dotenv import load_dotenv

try:
    import asyncpg
except ImportError:
    asyncpg = None

       
PROJECT_ROOT = Path("C:/Users/Haady/Documents/Antigravity/Dataverwerking_Antigravity")
ENV_PATH = PROJECT_ROOT / ".env"
BATCH_DIR = PROJECT_ROOT / "thesis/Analyse/DV2_validatie_bronnen/02_kabinetsreactie_batch_capfix_full_20260603"
GOLDEN_SET_CSV = PROJECT_ROOT / "thesis/Analyse/DV2_validatie_bronnen/06_kabinetsreactie_golden_set_20260604/golden_set.csv"
OUTPUT_DIR = PROJECT_ROOT / "thesis/Analyse/DV2_validatie_bronnen/02b_kabinetsreactie_171_frozen_20260605"

           
load_dotenv(ENV_PATH)

def get_db_config():
    """Retourneer database-connectieconfig uit environment."""
    return {
        'host': os.getenv('PG_HOST', 'localhost'),
        'port': int(os.getenv('PG_PORT', 5432)),
        'user': os.getenv('PG_USER'),
        'password': os.getenv('PG_PASSWORD'),
        'database': os.getenv('PG_DATABASE'),
    }

async def fetch_scope_fasen_ids(config):
    """
    Retourneer set van adviescollege_fasen.id's die in 171-scope vallen.

    Scope: Kaderwet=TRUE + instellingsbesluit_document_id NOT NULL +
            tijd_adviescollege IN (...) + NOT AP/CBPWEU
    """
    conn = await asyncpg.connect(**config)
    try:
        query = """
        SELECT f.id FROM register.adviescollege_fasen f
        JOIN dashboard_public.colleges c ON c.id=f.id
        WHERE f.kaderwet IS TRUE
          AND c.instellingsbesluit_document_id IS NOT NULL
          AND f.tijd_adviescollege IN ('Permanent adviescollege','Tijdelijk adviescollege','Eenmalig','Eenmalig adviescollege')
          AND f.officiele_naam NOT ILIKE '%Autoriteit Persoonsgegevens%'
          AND f.officiele_naam NOT ILIKE '%College Bescherming Persoonsgegevens%'
        ORDER BY f.id
        """
        rows = await conn.fetch(query)
        scope_ids = {row['id'] for row in rows}
        print(f"[DB] Scope fasen opgehaald: {len(scope_ids)} fasen")
        return scope_ids
    finally:
        await conn.close()

async def fetch_advies_documents_in_scope(config, scope_fasen_ids):
    """
    Retourneer dict van advies-document unique_id -> adviescollege_id voor documenten in scope.
    """
    if not scope_fasen_ids:
        return {}

    conn = await asyncpg.connect(**config)
    try:
        placeholders = ','.join(str(fid) for fid in sorted(scope_fasen_ids))
        query = f"""
        SELECT unique_id, adviescollege_id
        FROM corpus.adviesdocumenten
        WHERE adviescollege_id IN ({placeholders})
        ORDER BY unique_id
        """
        rows = await conn.fetch(query)
        doc_map = {row['unique_id']: row['adviescollege_id'] for row in rows}
        print(f"[DB] Advies-documenten in scope: {len(doc_map)} documenten")
        return doc_map
    finally:
        await conn.close()

def load_batch_manifests():
    """
    Laad batch_summary.json en retourneer lijst van case_id's.
    """
    manifest_path = BATCH_DIR / "batch_summary.json"
    with open(manifest_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    case_ids = [item['case_id'] for item in data.get('ok', [])]
    print(f"[Batch] Geladen {len(case_ids)} OK-cases uit batch_summary.json")
    return case_ids

def load_batch_result(case_id):
    """
    Laad case-result-JSON en retourneer (advies_id, document_id, element_count).
    """
    result_path = BATCH_DIR / f"cases/{case_id}/{case_id}_result.json"
    if not result_path.exists():
        print(f"  [WARN] Result niet gevonden: {result_path}")
        return None

    try:
        with open(result_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        advies_id = data.get('advies_id')
        document_id = data.get('document_id')
        element_count = len(data.get('finale_verwerkingsitems', []))

        return (str(advies_id), str(document_id), element_count)
    except Exception as e:
        print(f"  [ERR] Kon {case_id}_result.json niet laden: {e}")
        return None

def load_golden_set():
    """
    Laad golden_set.csv en retourneer lijst van (advies_element_id, case_id) tuples.
    """
    golden_items = []
    with open(GOLDEN_SET_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
                                                      
            row = {k.strip(): v for k, v in row.items()}
            golden_items.append((row['advies_element_id'], row['case']))

    print(f"[Golden] Geladen {len(golden_items)} elementen uit golden_set.csv")
    return golden_items

def process_batch_for_scope(case_ids, doc_map):
    """
    Verwerk batch-cases en retourneer:
      (in_scope_docs, out_of_scope_docs, in_scope_element_count)

    in_scope_docs: [{unique_id, adviescollege_id, advies_id, document_id, element_count}, ...]
    out_of_scope_docs: [{case_id, advies_id, document_id, reason}, ...]
    """
    in_scope_docs = []
    out_of_scope_docs = []
    in_scope_element_count = 0

                                                     
    advies_id_to_unique = {}
    for unique_id, adviescollege_id in doc_map.items():
                                                                     
                                                               
                                                                       
                                                         
        pass

                                                                
                                                    
                                                                    

    document_id_to_unique = {}
    for unique_id, adviescollege_id in doc_map.items():
                                                                 
                                                     
                                             
        pass

                                                                                    
    for i, case_id in enumerate(case_ids):
        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{len(case_ids)}]")

        result = load_batch_result(case_id)
        if not result:
            out_of_scope_docs.append({
                'case_id': case_id,
                'advies_id': 'UNKNOWN',
                'document_id': 'UNKNOWN',
                'reason': 'result_not_found'
            })
            continue

        advies_id, document_id, element_count = result

                                                        
                                                                                        
                                                        
                                                                            
                                                                  

                                                                                            
                                                                                                 
                                                                           
        pass

                                                                    
                                                      
                                                             
                                                    
                                                     

                                                                                  
    advies_ids_in_batch = set()
    batch_results = {}                                                      

    print("[Batch] Laden van alle case-resultaten...")
    for case_id in case_ids:
        result = load_batch_result(case_id)
        if result:
            advies_id, document_id, element_count = result
            batch_results[case_id] = result
            advies_ids_in_batch.add(advies_id)

    print(f"[Batch] {len(batch_results)}/{len(case_ids)} cases geladen")
    print(f"[Batch] {len(advies_ids_in_batch)} unieke advies_id's")

    return batch_results, advies_ids_in_batch

async def filter_batch_by_scope(batch_results, advies_ids_in_batch, scope_fasen_ids, config):
    """
    Filter batch-resultaten: welke advies_id's horen bij scope-fasen?
    """
    conn = await asyncpg.connect(**config)
    try:
                                                                    
        placeholders = ','.join(str(aid) for aid in sorted(advies_ids_in_batch))
        if not placeholders:
            return [], []

        query = f"""
        SELECT id, adviescollege_id
        FROM corpus.adviesdocumenten
        WHERE id IN ({placeholders})
        """
        rows = await conn.fetch(query)
        advies_college_map = {row['id']: row['adviescollege_id'] for row in rows}

        in_scope_docs = []
        out_of_scope_docs = []
        in_scope_element_count = 0

        for case_id, (advies_id, document_id, element_count) in batch_results.items():
            advies_id_int = int(advies_id)
            college_id = advies_college_map.get(advies_id_int)

            if college_id is None:
                out_of_scope_docs.append({
                    'case_id': case_id,
                    'advies_id': advies_id,
                    'document_id': document_id,
                    'reason': 'advies_not_found_in_corpus'
                })
            elif college_id in scope_fasen_ids:
                in_scope_docs.append({
                    'case_id': case_id,
                    'advies_id': advies_id,
                    'document_id': document_id,
                    'adviescollege_id': college_id,
                    'element_count': element_count
                })
                in_scope_element_count += element_count
            else:
                out_of_scope_docs.append({
                    'case_id': case_id,
                    'advies_id': advies_id,
                    'document_id': document_id,
                    'adviescollege_id': college_id,
                    'reason': 'college_out_of_scope'
                })

        return in_scope_docs, out_of_scope_docs, in_scope_element_count
    finally:
        await conn.close()

async def filter_golden_by_scope(golden_items, scope_fasen_ids, config):
    """
    Filter golden-set: welke elementen zijn in scope?

    Bepaal scope DIRECT via database: advies_element_id -> case_id -> advies_id -> college_id -> in scope_fasen_ids?

    Args:
        golden_items: list van (advies_element_id, case_id) tuples
        scope_fasen_ids: set van college_id's in scope

    Retourneer (in_scope_count, out_of_scope_count, in_scope_ids).
    """
                                        
    advies_ids = set()
    case_to_advies = {}
    for advies_element_id, case_id in golden_items:
        advies_id = int(case_id.split('__')[0])
        advies_ids.add(advies_id)
        case_to_advies[case_id] = advies_id

                                                          
    conn = await asyncpg.connect(**config)
    try:
        if advies_ids:
            placeholders = ','.join(str(aid) for aid in sorted(advies_ids))
            query = f"""
            SELECT id, adviescollege_id
            FROM corpus.adviesdocumenten
            WHERE id IN ({placeholders})
            """
            rows = await conn.fetch(query)
            advies_college_map = {row['id']: row['adviescollege_id'] for row in rows}
        else:
            advies_college_map = {}

        in_scope_ids = set()
        out_of_scope_ids = set()

        for advies_element_id, case_id in golden_items:
            advies_id = case_to_advies[case_id]
            college_id = advies_college_map.get(advies_id)

            if college_id is not None and college_id in scope_fasen_ids:
                in_scope_ids.add(advies_element_id)
            else:
                out_of_scope_ids.add(advies_element_id)

        return len(in_scope_ids), len(out_of_scope_ids), in_scope_ids
    finally:
        await conn.close()

def calculate_golden_metrics(golden_csv_path, in_scope_element_ids):
    """
    Hertell golden-set-metrices voor alleen in-scope elementen.
    Lees golden_vs_run.csv en bereken:
      - exacte_match: count(coarse_klopt=='ja')
      - behandeld_recall: hoeveel ai_coarse NOT IN {'niet_behandeld', 'ambigu'} onder coarse_truth NOT IN {'niet_behandeld', 'ambigu'}
      - niet_behandeld_recall: count(coarse_truth=='niet_behandeld' AND ai_coarse=='niet_behandeld')
      - confusiematrix: rijen=coarse_truth, kolommen=ai_coarse (6 categorieën)
    """
    golden_vs_run_path = Path(golden_csv_path).parent / 'golden_vs_run.csv'

                            
    golden_rows = {}
    with open(golden_vs_run_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip(): v for k, v in row.items()}
            if row.get('advies_element_id', '') in in_scope_element_ids:
                golden_rows[row['advies_element_id']] = row

              
    exact_match = 0
    treated_count = 0
    untreated_count = 0
    treated_ai_count = 0
    untreated_ai_count = 0

                                                        
                                                                                          
    confusion = {}

    for eid, row in golden_rows.items():
        coarse_truth = row.get('coarse_truth', '').strip()
        ai_coarse = row.get('ai_coarse', '').strip()
        coarse_klopt = row.get('coarse_klopt', '').strip()

                                            
        if coarse_klopt == 'ja':
            exact_match += 1

                                    
                                                                                                                       
        if coarse_truth not in {'niet_behandeld', 'ambigu'}:
            treated_count += 1
            if ai_coarse not in {'niet_behandeld', 'ambigu'}:
                treated_ai_count += 1

                                         
                                                                                           
        if coarse_truth == 'niet_behandeld':
            untreated_count += 1
            if ai_coarse == 'niet_behandeld':
                untreated_ai_count += 1

                        
        key = (coarse_truth, ai_coarse)
        confusion[key] = confusion.get(key, 0) + 1

    return {
        'n_in_scope': len(golden_rows),
        'exact_match_count': exact_match,
        'treated_count': treated_count,
        'treated_ai_count': treated_ai_count,
        'untreated_count': untreated_count,
        'untreated_ai_count': untreated_ai_count,
        'confusion_matrix': confusion
    }

async def main():
    """Voer volledige herschaling uit."""

                     
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

              
    config = get_db_config()
    print(f"[DB] Conecteer naar {config['host']}:{config['port']}/{config['database']}")

    try:
                     
        scope_fasen_ids = await fetch_scope_fasen_ids(config)
        print(f"Scope: {len(scope_fasen_ids)} fasen")

                    
        case_ids = load_batch_manifests()

                       
        print("[Batch] Verwerken...")
        batch_results, advies_ids_in_batch = process_batch_for_scope(case_ids, {})

                                 
        print("[Batch] Filteren door scope...")
        in_scope_docs, out_of_scope_docs, in_scope_element_count =\
            await filter_batch_by_scope(batch_results, advies_ids_in_batch, scope_fasen_ids, config)

        print(f"\nBATCH RESULTATEN:")
        print(f"  In scope: {len(in_scope_docs)} documenten, {in_scope_element_count} elementen")
        print(f"  Uit scope: {len(out_of_scope_docs)} documenten")
        print(f"  Totaal batch: {len(batch_results)} documenten")

                    
        golden_items = load_golden_set()

                                       
        print("[Golden] Filteren door scope...")
        golden_in_scope, golden_out_of_scope, golden_in_scope_ids =\
            await filter_golden_by_scope(golden_items, scope_fasen_ids, config)

        print(f"\nGOLDEN SET RESULTATEN:")
        print(f"  In scope: {golden_in_scope} elementen")
        print(f"  Uit scope: {golden_out_of_scope} elementen")

                          
        golden_metrics = calculate_golden_metrics(GOLDEN_SET_CSV, golden_in_scope_ids)
        print(f"\nGOLDEN METRICES:")
        print(f"  Exact match: {golden_metrics['exact_match_count']}/{golden_metrics['n_in_scope']}")
        print(f"  Behandeld recall: {golden_metrics['treated_ai_count']}/{golden_metrics['treated_count']}")
        print(f"  Niet-behandeld recall: {golden_metrics['untreated_ai_count']}/{golden_metrics['untreated_count']}")

                         
        print("\n[Output] Schrijven...")

                                 
        in_scope_csv = OUTPUT_DIR / 'in_scope_documenten.csv'
        with open(in_scope_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['case_id', 'advies_id', 'document_id', 'adviescollege_id', 'element_count']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for doc in in_scope_docs:
                writer.writerow(doc)
        print(f"  {in_scope_csv}")

                               
        uitval_csv = OUTPUT_DIR / 'uitval_documenten.csv'
        with open(uitval_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['case_id', 'advies_id', 'document_id', 'adviescollege_id', 'reason']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for doc in out_of_scope_docs:
                writer.writerow(doc)
        print(f"  {uitval_csv}")

                                  
        golden_md = OUTPUT_DIR / 'golden_171_hertelling.md'
        with open(golden_md, 'w', encoding='utf-8') as f:
            f.write("# Golden Set Hertelling 171-scope\n\n")
            f.write(f"Peildatum: 2026-06-05\n")
            f.write(f"Scope: corpus_keuzes/171 (Kaderwet colleges)\n\n")
            f.write(f"## Samenvatting\n")
            f.write(f"- **In-scope elementen**: {golden_metrics['n_in_scope']} van 88\n")
            f.write(f"- **Uit-scope elementen**: {88 - golden_metrics['n_in_scope']}\n")
            f.write(f"- **Exacte-match**: {golden_metrics['exact_match_count']}/{golden_metrics['n_in_scope']} ({100*golden_metrics['exact_match_count']/golden_metrics['n_in_scope']:.1f}%)\n")
            f.write(f"- **Behandeld recall**: {golden_metrics['treated_ai_count']}/{golden_metrics['treated_count']}\n")
            f.write(f"- **Niet-behandeld recall**: {golden_metrics['untreated_ai_count']}/{golden_metrics['untreated_count']}\n\n")

            f.write("## Confusiematrix (coarse_truth × ai_coarse)\n\n")
                                           
            all_categories = ['substantieel', 'procedureel', 'retorisch', 'afgewezen', 'niet_behandeld', 'ambigu']

                    
            f.write("| coarse_truth \\ ai_coarse | ")
            f.write(" | ".join(all_categories))
            f.write(" |\n")
            f.write("|" + "|".join(["---"] * (len(all_categories) + 1)) + "|\n")

                   
            for coarse_label in all_categories:
                f.write(f"| {coarse_label} ")
                for ai_label in all_categories:
                    count = golden_metrics['confusion_matrix'].get((coarse_label, ai_label), 0)
                    f.write(f"| {count} ")
                f.write("|\n")

        print(f"  {golden_md}")

                        
        manifest = {
            'peildatum': '2026-06-05',
            'scope': 'corpus_keuzes/171',
            'n_batch_documenten_totaal': len(batch_results),
            'n_docs_in_scope': len(in_scope_docs),
            'n_docs_uit_scope': len(out_of_scope_docs),
            'n_elementen_in_scope': in_scope_element_count,
            'n_elementen_totaal_batch': sum(item[2] for item in batch_results.values()),
            'golden_set_in_scope': golden_metrics['n_in_scope'],
            'golden_set_uit_scope': 88 - golden_metrics['n_in_scope'],
            'golden_exacte_match': f"{golden_metrics['exact_match_count']}/{golden_metrics['n_in_scope']}",
            'golden_behandeld_recall': f"{golden_metrics['treated_ai_count']}/{golden_metrics['treated_count']}",
            'golden_niet_behandeld_recall': f"{golden_metrics['untreated_ai_count']}/{golden_metrics['untreated_count']}"
        }

        manifest_json = OUTPUT_DIR / '_manifest.json'
        with open(manifest_json, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"  {manifest_json}")

        print("\n[Complete] Herschaling voltooid.")
        print(f"\nSAMENVATTING:")
        print(f"  Batch: {len(in_scope_docs)}/{len(batch_results)} docs in scope")
        print(f"  Elementen: {in_scope_element_count} van {sum(item[2] for item in batch_results.values())}")
        print(f"  Golden: {golden_in_scope}/{golden_in_scope + golden_out_of_scope} elementen in scope")

    except Exception as e:
        print(f"[ERR] {e}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
