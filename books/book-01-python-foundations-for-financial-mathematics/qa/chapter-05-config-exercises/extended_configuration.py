"""QA exercise implementation, not the published configuration.py.

Non-secret language values are en/fr. All supplied values, including shadowed
ones, must be valid. The FINLAB_ namespace is reserved by this application.
"""
from collections.abc import Mapping
from dataclasses import dataclass
import json
from pathlib import Path
from configuration import unique_object

ALLOWED = {'environment': {'development', 'test', 'production'},
           'currency': {'USD', 'EUR'}, 'decimal_places': {'0', '2', '4'},
           'report_language': {'en', 'fr'}}
DEFAULTS = dict(environment='development', currency='USD', decimal_places='2',
                report_language='en')
ENV_KEYS = {key: 'FINLAB_' + key.upper() for key in ALLOWED}

@dataclass(frozen=True)
class Settings:
    environment: str
    currency: str
    decimal_places: int
    report_language: str
    sources: tuple[tuple[str, str], ...]

def resolve(path: Path, environ: Mapping[str, str],
            overrides: Mapping[str, str]) -> Settings:
    payload = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    if type(payload) is not dict or set(payload) - ALLOWED.keys():
        raise ValueError('configuration must be an object with known keys')
    if set(overrides) - ALLOWED.keys():
        raise ValueError('unknown command-line configuration key')
    if any(name.startswith('FINLAB_') and name not in ENV_KEYS.values() for name in environ):
        raise ValueError('unknown FINLAB_ variable')
    selected = dict(DEFAULTS)
    sources = {key: 'default' for key in ALLOWED}
    layers = [('file', payload),
              ('environment', {key: environ[name] for key, name in ENV_KEYS.items() if name in environ}),
              ('cli', dict(overrides))]
    for source, layer in layers:
        for key, value in layer.items():
            if type(value) is not str or value not in ALLOWED[key]:
                raise ValueError(f'invalid {key} in {source}')
            selected[key] = value
            sources[key] = source
    return Settings(selected['environment'], selected['currency'],
                    int(selected['decimal_places']), selected['report_language'],
                    tuple(sorted(sources.items())))

def main(argv=None):
    import argparse
    import os
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--config', type=Path, required=True)
    for key in ALLOWED:
        parser.add_argument('--' + key.replace('_', '-'))
    args = parser.parse_args(argv)
    overrides = {key: getattr(args, key) for key in ALLOWED if getattr(args, key) is not None}
    settings = resolve(args.config, dict(os.environ), overrides)
    result = {key: getattr(settings, key) for key in ALLOWED}
    result['sources'] = dict(settings.sources)
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
