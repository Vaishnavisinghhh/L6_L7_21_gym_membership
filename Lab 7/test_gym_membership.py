from hypothesis import given, strategies as st
from gym_membership import parse_plan, calculate_bmi, average_workout


# ---------- 1. No-crash fuzz tests (required by the handout) ----------
@given(st.text() | st.none())
def test_parse_plan_no_crash(s):
    try:
        parse_plan(s)
    except Exception as e:
        assert False, f"parse_plan crashed with: {e!r}"


@given(st.text() | st.none())
def test_calculate_bmi_no_crash(s):
    try:
        calculate_bmi(s)
    except Exception as e:
        assert False, f"calculate_bmi crashed with: {e!r}"


@given(st.text() | st.none())
def test_average_workout_no_crash(s):
    try:
        average_workout(s)
    except Exception as e:
        assert False, f"average_workout crashed with: {e!r}"


# ---------- 2. Non-string / structured fuzzing ----------
@given(st.one_of(st.integers(), st.floats(), st.lists(st.integers()), st.binary(), st.booleans()))
def test_non_string_inputs_return_none(x):
    assert parse_plan(x) is None
    assert calculate_bmi(x) is None
    assert average_workout(x) is None


@given(st.text() | st.none() | st.floats() | st.integers())
def test_text_only_chars_that_break_parsers(s):
    for f in (parse_plan, calculate_bmi, average_workout):
        f(s)  # must simply not raise


# ---------- 3. Property tests on valid inputs ----------
@given(st.from_regex(r"[A-Za-z]{1,10}", fullmatch=True), st.integers(min_value=1, max_value=10**6))
def test_parse_plan_valid_roundtrip(plan, months):
    assert parse_plan(f"{plan}-{months}") == (plan.upper(), months)


@given(st.floats(min_value=1, max_value=500), st.floats(min_value=0.5, max_value=2.5))
def test_calculate_bmi_valid(w, h):
    r = calculate_bmi(f"{w},{h}")
    assert r is not None and r > 0


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1, max_size=50))
def test_average_workout_within_bounds(vals):
    r = average_workout(" ".join(map(str, vals)))
    assert min(vals) <= r <= max(vals)


# ---------- 4. Explicit edge cases found by fuzzing ----------
def test_known_edge_cases():
    assert parse_plan("GOLD-12") == ("GOLD", 12)
    assert parse_plan("GOLD") is None
    assert parse_plan("-5") is None
    assert parse_plan("GOLD-") is None
    assert parse_plan("GOLD-1-2") is None
    assert parse_plan("GOLD-0") is None
    assert calculate_bmi("70,1.75") == 22.9
    assert calculate_bmi("70,0") is None
    assert calculate_bmi("nan,1.7") is None
    assert calculate_bmi("70,inf") is None
    assert calculate_bmi("1e308,1e-308") is None
    assert calculate_bmi("70") is None
    assert average_workout("45 60 30") == 45
    assert average_workout("") is None
    assert average_workout("   ") is None
    assert average_workout("10 abc") is None
    assert average_workout("-5 10") is None
