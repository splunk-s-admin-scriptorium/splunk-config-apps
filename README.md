# splunk-config-apps
Templated configs facilitating Splunk Enterprise config deployment and management.

**README, docs and examples are a work in progress.**

## How to use

Example usage (in repository root):
```
python3 utils/scripts/compile-apps.py utils/conf-examples/example_1.json ~/splunk-config-apps-out/ apps/ apps_sources/
```

### Switches:
* **-q**, --quiet - limits the verbosity of the output