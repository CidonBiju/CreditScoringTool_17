"""Run each US-M4-01 suite with classifier-only statement and branch coverage."""

import ast
import dis
import inspect
import sys
import textwrap
import unittest

from decision.risk_decision import classify_risk_category


SUITES = (
    "blackbox.specification",
    "blackbox.random_based",
    "blackbox.boundary_value",
    "whitebox.control_flow",
    "whitebox.symbolic_execution",
    "whitebox.concolic",
)


def measure(suite, technique):
    source, first_line = inspect.getsourcelines(classify_risk_category)
    function = ast.parse(textwrap.dedent("".join(source))).body[0]
    statements = {
        first_line + node.lineno - 1
        for statement in function.body[1:]
        for node in ast.walk(statement)
        if isinstance(node, ast.stmt)
    }
    instructions = list(dis.get_instructions(classify_risk_category))
    # The graph models the handled lookup errors. It does not include the
    # interpreter's exception-type dispatch for exceptions outside the contract.
    exception_dispatch = {
        following.offset
        for instruction, following in zip(instructions, instructions[1:])
        if instruction.opname == "CHECK_EXC_MATCH"
    }
    jumps = {
        instruction.offset: (following.offset, instruction.argval)
        for instruction, following in zip(instructions, instructions[1:])
        if instruction.opname.startswith("POP_JUMP")
        and instruction.offset not in exception_dispatch
    }
    profile_reads = {
        first_line + statement.lineno - 1
        for node in function.body
        if isinstance(node, ast.Try)
        for statement in node.body
    }
    lines_seen = set()
    jumps_seen = set()
    read_outcomes_seen = set()
    previous_jump = None
    pending_read = None
    current_path = []
    paths = []

    def trace_body(frame, event, arg):
        nonlocal previous_jump, pending_read
        if event == "line":
            lines_seen.add(frame.f_lineno)
            if pending_read is not None:
                read_outcomes_seen.add((pending_read, "success"))
                current_path.append((pending_read, "success"))
            pending_read = frame.f_lineno if frame.f_lineno in profile_reads else None
        elif event == "exception" and pending_read is not None:
            read_outcomes_seen.add((pending_read, "error"))
            current_path.append((pending_read, "error"))
            pending_read = None
        elif event == "opcode":
            offset = frame.f_lasti
            if previous_jump is not None:
                jumps_seen.add((previous_jump, offset))
                current_path.append((previous_jump, offset))
            previous_jump = offset if offset in jumps else None
        elif event == "return":
            paths.append(tuple(current_path))
            current_path.clear()
        return trace_body

    def trace_calls(frame, event, arg):
        if event == "call" and frame.f_code is classify_risk_category.__code__:
            frame.f_trace_opcodes = True
            return trace_body
        return None

    all_jump_outcomes = {
        (offset, target) for offset, targets in jumps.items() for target in targets
    }
    all_read_outcomes = {
        (line, outcome) for line in profile_reads for outcome in ("success", "error")
    }
    previous_trace = sys.gettrace()
    # Python 3.12 requires an opcode-enabled frame before installing the tracer.
    measurement_frame = sys._getframe()
    previous_opcode_setting = measurement_frame.f_trace_opcodes
    measurement_frame.f_trace_opcodes = True
    sys.settrace(trace_calls)
    try:
        result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    finally:
        sys.settrace(previous_trace)
        measurement_frame.f_trace_opcodes = previous_opcode_setting

    statement_count = len(lines_seen & statements)
    branch_count = len(jumps_seen & all_jump_outcomes) + len(
        read_outcomes_seen & all_read_outcomes
    )
    branch_total = len(all_jump_outcomes) + len(all_read_outcomes)
    print(f"Statements: {statement_count}/{len(statements)}")
    print(f"Branches: {branch_count}/{branch_total}")
    print(f"Missing statement lines: {sorted(statements - lines_seen)}")
    print(f"Missing conditional jump edges: {sorted(all_jump_outcomes - jumps_seen)}")
    print(f"Missing profile read edges: {sorted(all_read_outcomes - read_outcomes_seen)}")
    if technique == "whitebox.control_flow":
        # Each bit denotes a traversed edge. XOR eliminates shared edges.
        edge_numbers = {
            edge: number
            for number, edge in enumerate(all_jump_outcomes | all_read_outcomes)
        }
        pivots = {}
        for path in paths:
            vector = sum(1 << edge_numbers[edge] for edge in path)
            while vector:
                pivot = vector.bit_length()
                if pivot not in pivots:
                    pivots[pivot] = vector
                    break
                vector ^= pivots[pivot]
        print(f"Independent observed paths: {len(pivots)}/{len(paths)}")
    if technique == "whitebox.concolic":
        print("Observed paths in test case order:")
        jump_numbers = {offset: number for number, offset in enumerate(jumps, 1)}
        for number, path in enumerate(paths, 1):
            steps = [
                f"line {origin} {target}" if isinstance(target, str)
                else f"J{jump_numbers[origin]} {'next' if target == jumps[origin][0] else 'jump'}"
                for origin, target in path
            ]
            print(f"{number}: {', '.join(steps)}")
    return result.wasSuccessful()


def main():
    loader = unittest.TestLoader()
    results = []
    for technique in SUITES:
        print(f"\n{technique}")
        suite = loader.loadTestsFromName(f"{__package__}.{technique}.test_us_m4_01")
        results.append(measure(suite, technique))
    return all(results)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
