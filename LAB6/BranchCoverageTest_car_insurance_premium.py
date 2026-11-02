import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ---------- annual_premium ----------
def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_unknown_car_type():
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)


def test_driver_too_young():
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)


def test_minimum_valid_age_18():
    # boundary: 18 is allowed, and gets the young-driver surcharge
    assert annual_premium("hatchback", 18, 1, False) == 12000


def test_age_24_gets_surcharge():
    assert annual_premium("sedan", 24, 1, False) == 16000


def test_age_25_no_surcharge():
    # boundary: 25 is neither young nor senior
    assert annual_premium("sedan", 25, 1, False) == 12000


def test_age_59_no_surcharge():
    assert annual_premium("sedan", 59, 1, False) == 12000


def test_age_60_senior_surcharge():
    assert annual_premium("suv", 60, 1, False) == 17000


def test_two_claims_no_change():
    # boundary: 2 claims is neither 0 nor > 2
    assert annual_premium("sedan", 30, 2, False) == 12000


def test_three_claims_doubles():
    assert annual_premium("sedan", 30, 3, False) == 24000


def test_no_claims_discount_with_surcharge():
    # (8000 + 4000) = 12000, 20% off -> 9600
    assert annual_premium("hatchback", 22, 0, False) == 9600


def test_anti_theft_true():
    assert annual_premium("sedan", 30, 0, True) == 9100


def test_anti_theft_false():
    assert annual_premium("suv", 30, 1, False) == 15000


# ---------- no_claim_bonus ----------
def test_no_bonus():
    assert no_claim_bonus(0) == 0


def test_bonus_negative_years():
    with pytest.raises(ValueError):
        no_claim_bonus(-1)


def test_bonus_5_years():
    assert no_claim_bonus(5) == 50


def test_bonus_4_years():
    assert no_claim_bonus(4) == 35


def test_bonus_3_years():
    assert no_claim_bonus(3) == 35


def test_bonus_2_years():
    assert no_claim_bonus(2) == 20


def test_bonus_1_year():
    assert no_claim_bonus(1) == 20


# ---------- claim_payout ----------
def test_payout_negative_damage():
    with pytest.raises(ValueError):
        claim_payout(-1, 100000, 1000, False)


def test_payout_negative_deductible():
    with pytest.raises(ValueError):
        claim_payout(5000, 100000, -1, False)


def test_payout_total_loss():
    assert claim_payout(50000, 80000, 1000, True) == 80000


def test_payout_below_deductible():
    assert claim_payout(500, 100000, 1000, False) == 0


def test_payout_equal_to_deductible():
    # boundary: damage == deductible -> 0
    assert claim_payout(1000, 100000, 1000, False) == 0


def test_payout_normal():
    assert claim_payout(5000, 100000, 1000, False) == 4000


def test_payout_equal_to_insured_value():
    # boundary: payout == insured value -> not capped, same result
    assert claim_payout(101000, 100000, 1000, False) == 100000


def test_payout_capped_at_insured_value():
    assert claim_payout(200000, 100000, 1000, False) == 100000
