# Tests

To test the compilation process and junja templates at the same time, a set consists of input configuration `config.json` and expected results (`expected` folder). The `run-test.py` script runs a test and compares resulting files line by line.

**Naming**
Test Name: `<type>_<ID>`

**ID**: 6 digit number

**Types**:
- **A** - App Test - focuses on testing single app and different configs thereof
- **C** - Configuration test - tests full configuration, with multiple apps, mainly for testing proposed environment configs
- **T** - General tests, not matching other naming


## Existing tests

### App Tests

|Name|Enabled by Default|App|Completion|Description|
|---|---|---|---|---|
|A_000001|true|authorize_roles|10%s|Only a few basic tests|