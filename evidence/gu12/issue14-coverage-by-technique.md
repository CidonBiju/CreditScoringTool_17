# Issue 14 · Weighting profile coverage by technique

Tested revision `db447c1bc64fb60cc5d68c00e060826ea44892bc` on 26 November 2026 in a clean Linux checkout with Python 3.12.14 and coverage.py 7.10.7. Each run measured the function `scoring.credit_scoring.apply_weighting_profile` independently. All 15 test methods passed in the full gu12 discovery run.

| Test package under gu12.test | Methods passed | Executable lines | Branch outcomes |
|---|---:|---:|---:|
| blackbox.equivalence_partitioning | 5 | 15/16 | 7/8 |
| blackbox.boundary_value_analysis | 2 | 14/16 | 6/8 |
| blackbox.random_based | 1 | 13/16 | 5/8 |
| whitebox.control_flow | 4 | 16/16 | 8/8 |
| whitebox.symbolic_execution | 2 | 16/16 | 8/8 |
| whitebox.concolic | 1 | 14/16 | 6/8 |

## Symbolic paths and concrete outcomes

The [symbolic tree](issue14-symbolic-tree.png) assumes a string profile and the expected metric keys. An accepted metric has exact Python type int or float and lies in the closed interval [0, 100]. The baseline uses Conservative, payment consistency 90, debt-to-income ratio 60 and utilisation 60. Each row changes only the specified input. The tests assert the exact exception message on P1–P5 and the profile and score on P6.

| Path | Conditions along the path | Change from baseline | Expected outcome, confirmed by the test |
|---|---|---|---|
| P1 | Unknown profile | Profile = "Unknown" | ValueError, Unknown weighting profile: Unknown |
| P2 | Supported profile and missing payment consistency | Payment = None | ValueError, Insufficient payment history |
| P3 | Supported profile and present, invalid payment consistency | Payment = "90" (string) | ValueError, payment_history must be a number between 0 and 100 |
| P4 | Supported profile, valid payment, invalid DTI | DTI = 101 | ValueError, dti must be a number between 0 and 100 |
| P5 | Supported profile, valid payment and DTI, invalid utilisation | Utilisation = 101 | ValueError, utilisation must be a number between 0 and 100 |
| P6 | Supported profile and all three metrics valid | Baseline, then profile = "High Risk" | Conservative 630 and High Risk 685 |

The manually derived concolic test starts from the P6 seed, which returns 630. It preserves the valid profile, payment, DTI and numeric utilisation type, then reverses the upper-bound condition by setting utilisation to 101. The second execution reaches P5 and raises the expected utilisation error. Its two unvisited error routes are unknown profile and missing payment history.

## Reproducing the evidence

Run from the repository root with coverage.py 7.10.7 available to the selected interpreter. For each technique, replace the example directory with the corresponding package directory in the table and run the two coverage commands together.

```sh
python -m coverage run --branch --source=scoring -m unittest discover -s gu12/test/whitebox/symbolic_execution -t . -v
python -m coverage json -o coverage-report.json
python -c "import json; print(json.load(open('coverage-report.json'))['files']['scoring/credit_scoring.py']['functions']['apply_weighting_profile']['summary'])"
python -m unittest discover -s gu12 -t . -v
```

## Full test output

```text
Python 3.12.14
test_accepts_endpoints_and_values_just_inside (gu12.test.blackbox.boundary_value_analysis.test_payment_consistency.TestPaymentConsistencyBoundaries.test_accepts_endpoints_and_values_just_inside) ... ok
test_rejects_values_just_outside (gu12.test.blackbox.boundary_value_analysis.test_payment_consistency.TestPaymentConsistencyBoundaries.test_rejects_values_just_outside) ... ok
test_each_profile_returns_its_signed_score_breakdown (gu12.test.blackbox.equivalence_partitioning.test_weighting_profiles.TestWeightingProfiles.test_each_profile_returns_its_signed_score_breakdown) ... ok
test_missing_payment_consistency_reports_insufficient_history (gu12.test.blackbox.equivalence_partitioning.test_weighting_profiles.TestWeightingProfiles.test_missing_payment_consistency_reports_insufficient_history) ... ok
test_supported_profiles_apply_their_agreed_weights (gu12.test.blackbox.equivalence_partitioning.test_weighting_profiles.TestWeightingProfiles.test_supported_profiles_apply_their_agreed_weights) ... ok
test_unknown_profile_is_rejected (gu12.test.blackbox.equivalence_partitioning.test_weighting_profiles.TestWeightingProfiles.test_unknown_profile_is_rejected) ... ok
test_zero_payment_consistency_is_valid (gu12.test.blackbox.equivalence_partitioning.test_weighting_profiles.TestWeightingProfiles.test_zero_payment_consistency_is_valid) ... ok
test_scores_match_the_agreed_weights (gu12.test.blackbox.random_based.test_weighting_profiles.TestRandomWeightingProfiles.test_scores_match_the_agreed_weights) ... ok
test_reverse_utilisation_decision_from_p6_to_p5 (gu12.test.whitebox.concolic.test_weighting_profiles.TestConcolicWeightingProfiles.test_reverse_utilisation_decision_from_p6_to_p5) ... ok
test_loop_finishes_and_returns_all_contributions (gu12.test.whitebox.control_flow.test_weighting_profiles.TestWeightingControlFlow.test_loop_finishes_and_returns_all_contributions) ... ok
test_loop_rejects_invalid_values_at_each_position (gu12.test.whitebox.control_flow.test_weighting_profiles.TestWeightingControlFlow.test_loop_rejects_invalid_values_at_each_position) ... ok
test_missing_history_exits_before_validation_loop (gu12.test.whitebox.control_flow.test_weighting_profiles.TestWeightingControlFlow.test_missing_history_exits_before_validation_loop) ... ok
test_profile_guard_runs_before_metric_lookup (gu12.test.whitebox.control_flow.test_weighting_profiles.TestWeightingControlFlow.test_profile_guard_runs_before_metric_lookup) ... ok
test_error_paths_from_symbolic_tree (gu12.test.whitebox.symbolic_execution.test_weighting_profiles.TestSymbolicWeightingProfiles.test_error_paths_from_symbolic_tree) ... ok
test_p6_returns_a_score_for_each_profile (gu12.test.whitebox.symbolic_execution.test_weighting_profiles.TestSymbolicWeightingProfiles.test_p6_returns_a_score_for_each_profile) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.006s

OK
```

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
