import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ---------- membership_cost ----------
def test_monthly_plan():
    assert membership_cost("monthly", 30, False, False) == 1500


def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 30, False, False)


def test_too_young():
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)


def test_senior_discount():
    assert membership_cost("monthly", 60, False, False) == 1125


def test_student_discount():
    assert membership_cost("monthly", 20, True, False) == 1350


def test_trainer_monthly():
    assert membership_cost("monthly", 30, False, True) == 3500


def test_trainer_yearly():
    assert membership_cost("yearly", 30, False, True) == 13500


# ---------- can_enter ----------
def test_can_enter():
    assert can_enter(10, True, False, "M") is True


def test_inactive_plan():
    assert can_enter(10, False, False, "M") is False


def test_outside_hours():
    assert can_enter(3, True, False, "M") is False


def test_women_only_slot_female():
    assert can_enter(10, True, True, "F") is True


def test_women_only_slot_male():
    assert can_enter(10, True, True, "M") is False


# ---------- bmi_category ----------
def test_invalid_height():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, 0)


def test_underweight():
    assert bmi_category(40, 1.75) == "underweight"


def test_normal():
    assert bmi_category(70, 1.75) == "normal"


def test_overweight():
    assert bmi_category(85, 1.75) == "overweight"


def test_obese():
    assert bmi_category(100, 1.75) == "obese"
