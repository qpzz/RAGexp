"""One authorized frozen run; key stays in process environment, never on disk."""
import getpass
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
import warnings
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from run_experiment import execute


def main():
    os.chdir(ROOT)
    os.environ['AGENT_LLM_BASE_URL'] = 'https://api.deepseek.com'
    os.environ['AGENT_LLM_MODEL'] = 'deepseek-v4-pro'
    if not os.environ.get('AGENT_LLM_API_KEY'):
        # Refuse an echoing fallback. The supplied key never enters a command line.
        warnings.simplefilter('error', getpass.GetPassWarning)
        os.environ['AGENT_LLM_API_KEY'] = getpass.getpass('API key (hidden; process environment only): ')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    preflight = ROOT / 'results' / ('deepseek_preflight_' + stamp + '.json')
    preflight.parent.mkdir(exist_ok=True)
    record = {'time_utc': stamp, 'base_url': os.environ['AGENT_LLM_BASE_URL'],
              'requested_model': os.environ['AGENT_LLM_MODEL'], 'generation_calls': 0}
    try:
        req = urllib.request.Request(os.environ['AGENT_LLM_BASE_URL'] + '/models',
                                     headers={'Authorization': 'Bearer ' + os.environ['AGENT_LLM_API_KEY']})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        ids = [item['id'] for item in data['data']]
        record.update(status='ok', available_models=ids)
        if os.environ['AGENT_LLM_MODEL'] not in ids:
            record['status'] = 'requested_model_not_available'
    except urllib.error.HTTPError as exc:
        record.update(status='failed', http_status=exc.code)
    except Exception as exc:
        record.update(status='failed', error_type=type(exc).__name__)
    preflight.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Preflight:', record['status'], '|', preflight, flush=True)
    if record['status'] != 'ok':
        os.environ.pop('AGENT_LLM_API_KEY', None)
        return 2
    output = ROOT / 'results' / ('live_deepseek_10x3_' + stamp + '.jsonl')
    print('Starting frozen run:', output, flush=True)
    try:
        path, status = execute(ROOT / 'configs/compositional_live_10x3.json', output)
        print('Run status:', status, flush=True)
        subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'evaluate.py'), '--run', str(path)], check=True)
        return 0 if status == 'complete' else 2
    finally:
        os.environ.pop('AGENT_LLM_API_KEY', None)


if __name__ == '__main__':
    raise SystemExit(main())
