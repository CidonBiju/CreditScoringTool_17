# Issue 14 weighting-profile test evidence

Measured on Python 3.12.14 with coverage.py 7.10.7. The production function is the version in a8387c0. Each row measures only `apply_weighting_profile` in a separate test run.

| Technique | Test methods | Executable lines | Branch outcomes |
| --- | ---: | ---: | ---: |
| Random-based black-box | 1 | 13/16 | 5/8 |
| White-box control flow | 4 | 16/16 | 8/8 |

The black-box test uses seed 1401 to generate 100 valid metric triples. It checks each under both profiles against a calculation based on their agreed percentage weights and the 300–850 score scale. The three uncovered outcomes reject invalid data, which the generator deliberately excludes.

The white-box suite selects inputs to reach the unknown-profile guard, the missing-history guard, validation failures at each loop position, and successful loop exhaustion. Seed 1402 makes the sampled values repeatable. The eight outcomes are two per source-level decision (the two guards, the loop, and the validation condition). This count does not measure every individual Boolean condition or every possible execution path.

Run the suites from the repository root with the standard library:

```sh
python -m unittest -v gu12.test.blackbox.random_based.test_weighting_profiles
python -m unittest -v gu12.test.whitebox.control_flow.test_weighting_profiles
python -m unittest discover -s gu12 -t . -v
```

To reproduce the measurements with coverage.py 7.10.7 installed, run:

```sh
for suite in blackbox.random_based whitebox.control_flow; do
    python -m coverage run --branch --source=scoring -m unittest "gu12.test.${suite}.test_weighting_profiles" &&
    python -m coverage json -o "coverage-${suite}.json" || break
done
```

In each JSON report, read `files → scoring/credit_scoring.py → functions → apply_weighting_profile → summary`. The full gu12 run passed all 12 test methods.

## Commit references after the author update

Each pair has the same Git tree. The original hashes above identify the revisions used for the coverage measurements.

| Original commit | Rewritten commit |
| --- | --- |
| `150441dc0dfc` | `c0b732563106` |
| `a8387c073eaf` | `7fab3ef59c2e` |
| `ee245e4c261b` | `65fd5af3a0f2` |
| `e44bde483275` | `2b4946d9f424` |
| `db447c1bc64f` | `2f77c484064e` |
| `c9d2983a24a3` | `bf573efd94d3` |
