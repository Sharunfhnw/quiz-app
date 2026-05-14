import hashlib


# TC_001 — Score 80%
def test_score_80_prozent():
    score = 4
    max_score = 5
    prozent = round(score / max_score * 100)
    assert prozent == 80


# TC_002 — Score 100%
def test_score_100_prozent():
    score = 5
    max_score = 5
    prozent = round(score / max_score * 100)
    assert prozent == 100


# TC_003 — Score 0%
def test_score_0_prozent():
    score = 0
    max_score = 5
    prozent = round(score / max_score * 100)
    assert prozent == 0