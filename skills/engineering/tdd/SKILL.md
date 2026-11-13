---
name: tdd
description: Test-driven development loop for features and bug fixes. Use when the user asks for TDD, test-first work, a red-green-refactor cycle, or when implementing a feature or fix where a failing test should come before the code.
---

# TDD

Build the change one behaviour at a time. Each cycle starts with a test that fails for the right reason, then the smallest code that makes it pass, then cleanup while the suite stays green.

## Plan the behaviours

Before the first test, list the behaviours the change must have, in the order to build them. Each item is one observable outcome a caller can see. Show the list to the user only when the scope is unclear; otherwise proceed.

Pick the first behaviour that gives a visible result, not the easiest internal helper.

## The cycle

For each behaviour:

1. **Red.** Write one test through the public interface that describes the behaviour. Run it. It must fail, and the failure message must say the behaviour is missing (an assertion mismatch or a missing function), not a syntax error or a broken import. Fix the test until it fails for the right reason.
2. **Green.** Write the least code that passes. Hard-coded returns are fine at this step if the next test forces generalisation. Run the whole suite.
3. **Refactor.** Remove duplication, rename, and move code only while every test is green. Run the suite after each change.

Do not write two new failing tests at once. One red test at a time keeps the feedback clear.

## Rules for good tests

- Test through the public interface: function calls, HTTP endpoints, CLI output, rendered output. Do not assert on private helpers or call order between internal collaborators.
- Assert on outcomes a caller relies on (return values, persisted state, emitted events). Avoid asserting that a mock was called unless the call itself is the behaviour.
- Mock only at system boundaries you do not control: network, clock, randomness, third-party services. Use real in-process collaborators otherwise.
- Keep each test independent. No shared mutable state between tests; no test depends on another running first.
- Name the test after the behaviour in plain words, e.g. `rejects a coupon that expired yesterday`.

## Bug fixes

A bug fix starts with a test that reproduces the reported symptom at the seam where the bug lives:

1. Write the test with the exact input from the report. Watch it fail for the reported reason.
2. Fix the code. Watch the test pass.
3. Re-run the full suite.

If the bug's cause is not yet known, stop and use `diagnosing-bugs` first. Do not guess a fix and write a test to match the guess.

## When TDD does not fit

Say so and ask before proceeding when:

- There is no test harness and setting one up is a separate task. Offer to set up the harness first.
- The change is pure configuration, a rename, or a docs edit with no behaviour to test.
- The code is a throwaway spike the user has said they will delete.

## Done when

- Every behaviour on the list has a test that was seen failing before the code existed.
- The full suite passes, and you ran it after the last change.
- No test was deleted or weakened to get to green. If one had to change, say why in the summary.
