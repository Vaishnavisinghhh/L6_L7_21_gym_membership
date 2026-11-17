import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ---------- membership_cost: every branch both ways ----------
def test_monthly_plan():
    assert membership_cost("monthly", 30, False, False) == 1500


def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 30, False, False)


def test_too_young():
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)


def test_age_boundary_14_allowed():
    assert membership_cost("monthly", 14, False, False) == 1500


def test_age_59_no_senior_discount():
    assert membership_cost("monthly", 59, False, False) == 1500


def test_senior_discount_boundary_60():
    assert membership_cost("monthly", 60, False, False) == 1125


def test_senior_beats_student_discount():
    # elif branch skipped: senior discount only, not stacked
    assert membership_cost("monthly", 65, True, False) == 1125


def test_student_discount():
    assert membership_cost("monthly", 20, True, False) == 1350


def test_non_student_no_discount_yearly():
    assert membership_cost("yearly", 30, False, False) == 12000


def test_trainer_monthly():
    assert membership_cost("monthly", 30, False, True) == 3500


def test_trainer_quarterly_no_yearly_rebate():
    assert membership_cost("quarterly", 30, False, True) == 6000


def test_trainer_yearly_rebate():
    assert membership_cost("yearly", 30, False, True) == 13500


def test_trainer_yearly_senior():
    assert membership_cost("yearly", 70, False, True) == 10500


# ---------- can_enter: every branch both ways ----------
def test_can_enter():
    assert can_enter(10, True, False, "M") is True


def test_inactive_plan():
    assert can_enter(10, False, False, "M") is False


def test_too_early():
    assert can_enter(4, True, False, "M") is False


def test_too_late():
    assert can_enter(23, True, False, "M") is False


def test_hour_boundaries_allowed():
    assert can_enter(5, True, False, "M") is True
    assert can_enter(22, True, False, "M") is True


def test_women_only_slot_female():
    assert can_enter(10, True, True, "F") is True


def test_women_only_slot_male():
    assert can_enter(10, True, True, "M") is False


# ---------- bmi_category: every branch both ways ----------
def test_invalid_height_zero():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, 0)


def test_invalid_height_negative():
    with pytest.raises(ValueError):
        bmi_category(70, -1.7)


def test_underweight():
    assert bmi_category(40, 1.75) == "underweight"


def test_normal():
    assert bmi_category(70, 1.75) == "normal"


def test_overweight():
    assert bmi_category(85, 1.75) == "overweight"


def test_obese():
    assert bmi_category(100, 1.75) == "obese"


def test_bmi_boundaries():
    assert bmi_category(18.5, 1.0) == "normal"
    assert bmi_category(25, 1.0) == "overweight"
    assert bmi_category(30, 1.0) == "obese"
