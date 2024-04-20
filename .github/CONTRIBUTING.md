# Contributing

Welcome to whos-there! We're excited to have you join us. This document will help you get started.

## Design Principles

We encourage all sorts of contributions you're interested in adding!
Code should be intuitive, pythonic, and follow the defined style.
We also require the use of type hints and docstrings.

### Force User Decisions To Best Practices

There are 1,000 ways to do something.
However, eventually one popular solution becomes standard practice, and everyone follows.
We try to find the best way to solve a particular problem, and then force our users to use it for readability and simplicity.

### Backward-compatible API

We all hate updating our packages because we don't want to refactor a bunch of stuff.
Therefore, every change which could break an API is backward compatible with good deprecation warnings.


---

## Contribution Types

We are always open to contributions of new features or bug fixes.

### Bug Fixes:

1. If you find a bug please submit a GitHub issue.

    - Make sure the title explains the issue.
    - Describe your setup, what you are trying to do, expected vs. actual behaviour.
    - Add details on how to reproduce the issue - a minimal test case is always best.

2. Try to fix it or recommend a solution. We highly recommend to use a test-driven approach:

    - Convert your minimal code example to a unit/integration test with assert on expected results.
    - Start by debugging the issue... You can run just this particular test in your IDE and draft a fix.
    - Verify that your test case fails on the master branch and only passes with the fix applied.

3. Submit a PR!

_**Note**, even if you do not find the solution, sending a PR with a test covering the issue is a valid contribution, and we can help you or finish it with you :\]_

### New Features:

1. Submit a GitHub issue - describe what is the motivation of such feature (adding the use case, or an example is helpful).

2. Determine the feature scope with us.

3. Submit a PR! We recommend test driven approach to adding new features as well:

   - Write a test for the functionality you want to add.
   - Write the functional code until the test passes.

4. Add/update the relevant tests!

### Test cases:

Want to keep whos_there healthy?
Love seeing those green tests? So do we!
How to we keep it that way?
We write tests!
We value tests contribution even more than new features.
