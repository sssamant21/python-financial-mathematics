"""Reconstruct exact 5.10 source; keep exercise extension explicitly separate."""
import hashlib
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
BOOK = HERE.parents[1]
SOURCE = BOOK / 'chapter-05/5.10-configuration-and-environment-separation.md'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def run():
    text = SOURCE.read_text(encoding='utf-8')
    blocks = re.findall(r'^```python\n(.*?)^```', text, re.M | re.S)
    assert len(blocks) == 3
    files = dict(zip(['configuration.py', 'config_demo.py', 'test_configuration.py'], blocks))
    files['development.json'] = re.findall(r'^```json\n(.*?)^```', text, re.M | re.S)[0]
    operations, checks = [], []
    env = {k: v for k, v in os.environ.items() if not k.startswith('FINLAB_') and k not in ('PYTHONPATH', 'PYTHONHOME')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    def ck(exercise, label, actual, expected):
        checks.append(dict(exercise=exercise, label=label, actual=repr(actual), expected=repr(expected), status='PASS' if actual == expected else 'FAIL'))
    def reject(exercise, label, fn, kind='ValueError'):
        try:
            fn()
            actual = 'no exception'
        except Exception as error:
            actual = type(error).__name__
        ck(exercise, label, actual, kind)
    with TemporaryDirectory(prefix='configuration-exercises-') as tmp:
        root = Path(tmp); project = root/'project'; project.mkdir(); outside = root/'outside'; outside.mkdir()
        for name, code in files.items():
            (project/name).write_text(code, encoding='utf-8')
        original = load('configuration', project/'configuration.py')
        (project/'extended_configuration.py').write_bytes((HERE/'extended_configuration.py').read_bytes())
        extended = load('extended_configuration_qa', project/'extended_configuration.py')
        def command(label, args, *, error=None, expected=None, methods=None, cwd=project, variables=None):
            result = subprocess.run([sys.executable, '-B', *map(str, args)], cwd=cwd, env=env if variables is None else dict(env, **variables), capture_output=True, text=True, timeout=30)
            actual_count = re.findall(r'Ran (\d+) tests? in', result.stderr)
            count = int(actual_count[0]) if len(actual_count) == 1 else None
            ok = result.returncode == 0 and result.stderr == ''
            if error:
                ok = result.returncode != 0 and result.stdout == '' and error in result.stderr
            if expected is not None:
                try:
                    actual = json.loads(result.stdout)
                except ValueError:
                    actual = result.stdout
                ok = ok and actual == expected
            if methods is not None:
                ok = result.returncode == 0 and count == methods and bool(re.search(r'^OK\s*$', result.stderr, re.M))
            operations.append(dict(label=label, args=list(map(str, args)), cwd=str(cwd), controlled_variables=variables or {}, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr, expected_error=error, expected_json=expected, expected_methods=methods, actual_methods=count, status='PASS' if ok else 'FAIL'))
            return result
        command('exact original eight-method suite', ['-m','unittest','discover','-v'], methods=8)
        command('E1 required --config, no report', ['config_demo.py'], error='the following arguments are required: --config')
        external = outside/'settings.json'; external.write_text('{"environment":"test","currency":"EUR","decimal_places":"4"}')
        expected = dict(environment='test', currency='EUR', decimal_places=4, sources=dict(environment='file', currency='file', decimal_places='file'))
        command('E2 absolute configuration outside project, outside cwd', [project/'config_demo.py', '--config',external], cwd=outside, expected=expected)
        before = external.read_bytes()
        settings = project/'settings.json'
        def resolve(module, payload=None, environ=None, cli=None):
            settings.write_text(json.dumps({} if payload is None else payload), encoding='utf-8')
            return module.resolve(settings, {} if environ is None else environ, {} if cli is None else cli)
        base = dict(environment='development', currency='USD', decimal_places=2)
        def expected_language(language, source, **sources):
            return dict(base, report_language=language, sources=dict(environment='default', currency='default', decimal_places='default', report_language=source, **sources))
        # Language has its own wire contract, not implicit locale discovery/translation.
        for label, payload, variables, cli, language, source in [
            ('default', {}, {}, {}, 'en', 'default'),
            ('file', {'report_language':'fr'}, {}, {}, 'fr', 'file'),
            ('environment', {'report_language':'fr'}, {'FINLAB_REPORT_LANGUAGE':'en'}, {}, 'en', 'environment'),
            ('cli', {'report_language':'fr'}, {'FINLAB_REPORT_LANGUAGE':'en'}, {'report_language':'fr'}, 'fr', 'cli')]:
            settings.write_text(json.dumps(payload))
            args = ['extended_configuration.py','--config',settings]
            for key, value in cli.items(): args += ['--'+key.replace('_','-'), value]
            command('E3 language '+label, args, variables=variables, expected=expected_language(language,source))
        for layer in ('file', 'environment', 'cli'):
            for value in ('', 'EN', ' fr', 'es', None, True, 2):
                payload = {'report_language':value} if layer == 'file' else {}
                variables = {'FINLAB_REPORT_LANGUAGE':value} if layer == 'environment' else {}
                cli = {'report_language':value} if layer == 'cli' else {'report_language':'en'}
                reject('5.10-E3', f'{layer} invalid language {value!r}, even shadowed', lambda p=payload,e=variables,c=cli:resolve(extended,p,e,c))
        settings.write_text('{}')
        command('E3 CLI invalid language no report', ['extended_configuration.py','--config',settings,'--report-language','es'], error='invalid report_language in cli')
        ck('5.10-E4','original ignores typo',resolve(original,{}, {'FINLAB_CURRNCY':'EUR'}).currency,'USD')
        for name in ('FINLAB_CURRNCY', 'FINLAB_UNUSED', 'FINLAB_'):
            reject('5.10-E4', 'reserved namespace rejects '+name, lambda n=name:resolve(extended,{}, {n:'arbitrary'}))
        ck('5.10-E4','unrelated environment still ignored',resolve(extended,{}, {'UNRELATED':'arbitrary','PATH':'ignored'}).currency,'USD')
        settings.write_text('{}')
        command('E4 misspelled FINLAB CLI process variable no report', ['extended_configuration.py','--config',settings], variables={'FINLAB_CURRNCY':'EUR'}, error='unknown FINLAB_ variable')
        reject('5.10-E3','unknown file key',lambda:resolve(extended, {'language':'en'}))
        reject('5.10-E3','unknown override key',lambda:resolve(extended, {}, {}, {'language':'en'}))
        settings.write_text('{"report_language":"en","report_language":"fr"}')
        reject('5.10-E3','duplicate language member',lambda:extended.resolve(settings,{},{}))
        missing = root/'missing.json'
        reject('5.10-E3','required file despite complete overrides',lambda:extended.resolve(missing,{},dict(extended.DEFAULTS)), 'FileNotFoundError')
        env_input = {'FINLAB_REPORT_LANGUAGE':'fr'}; cli_input = {'currency':'EUR'}
        initial = (dict(env_input), dict(cli_input))
        result = resolve(extended,{},env_input,cli_input)
        ck('5.10-E3','extension input mappings preserved',(env_input,cli_input),initial)
        reject('5.10-E3','frozen settings',lambda:setattr(result,'report_language','en'),'FrozenInstanceError')
        reject('5.10-E5','strict rejects invalid lower file despite valid winner',lambda:resolve(original, {'currency':'GBP'}, {}, {'currency':'EUR'}))
        # Concrete winner-only alternative is a policy demonstration on this field,
        # not a replacement JSON resolver or silently changed published policy.
        def winner_currency(file, environ, cli):
            selected = cli.get('currency', environ.get('FINLAB_CURRENCY', file.get('currency','USD')))
            if type(selected) is not str or selected not in {'USD','EUR'}: raise ValueError('invalid winning currency')
            return selected
        ck('5.10-E5','winner-only hides stale file',winner_currency({'currency':'GBP'},{},{'currency':'EUR'}),'EUR')
        reject('5.10-E5','hidden defect surfaces when override removed',lambda:winner_currency({'currency':'GBP'},{},{}))
        usd = command('E7 exact original USD label report', ['config_demo.py','--config','development.json'])
        eur = command('E7 exact original EUR label report', ['config_demo.py','--config','development.json','--currency','EUR'])
        usd_report, eur_report = json.loads(usd.stdout),json.loads(eur.stdout)
        ck('5.10-E7','currency labels only',(usd_report['currency'],eur_report['currency']),('USD','EUR'))
        for report in (usd_report,eur_report): report.pop('currency');report['sources'].pop('currency')
        ck('5.10-E7','all other settings unchanged',usd_report,eur_report)
        ck('5.10-E7','no amount or rate in original record',set(original.Settings.__dataclass_fields__),{'environment','currency','decimal_places','sources'})
        ck('5.10-E2','external configuration unchanged',external.read_bytes(),before)
        ck('all','original four files unchanged',{name:digest((project/name).read_bytes()) for name in files},{name:digest(code.encode()) for name,code in files.items()})
    output = dict(python=platform.python_version(),platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=digest(SOURCE.read_bytes()),original_files={name:digest(code.encode()) for name,code in files.items()},supplemental_files={'extended_configuration.py':digest((HERE/'extended_configuration.py').read_bytes())},exercise_records=8,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),source_method_invocations=sum(x['actual_methods'] or 0 for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('operations','checks','original_files','supplemental_files')}))
    return bool(output['failed'] or output['command_failed'])

if __name__ == '__main__':
    raise SystemExit(run())
