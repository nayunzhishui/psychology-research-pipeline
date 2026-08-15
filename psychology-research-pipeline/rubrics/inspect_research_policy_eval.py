"""Optional Inspect AI adapter; the deterministic frozen suite remains authoritative."""

try:
    from inspect_ai import Task, task
    from inspect_ai.dataset import json_dataset
    from inspect_ai.scorer import includes
    from inspect_ai.solver import generate
except ImportError:  # Keep the skill usable without the optional evaluator.
    Task = None


if Task is not None:
    @task
    def research_policy_guardrails():
        return Task(
            dataset=json_dataset("../tests/frozen_cases/research_policy_cases.json"),
            solver=[generate()],
            scorer=includes(),
        )
