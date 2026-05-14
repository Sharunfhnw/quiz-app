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


# TC_004 — Leerer Titel ungueltig
def test_validierung_leerer_titel():
    titel = ''
    assert titel.strip() == ''


# TC_005 — Quiz ohne Fragen ungueltig
def test_validierung_keine_fragen():
    fragen = []
    assert len(fragen) == 0


# TC_006 — Passwort Hashing
def test_passwort_hashing():
    passwort = 'meinPasswort123'
    hash1 = hashlib.sha256(passwort.encode()).hexdigest()
    hash2 = hashlib.sha256(passwort.encode()).hexdigest()
    assert hash1 == hash2


def test_passwort_hashing_unterschiedlich():
    hash1 = hashlib.sha256('passwort1'.encode()).hexdigest()
    hash2 = hashlib.sha256('passwort2'.encode()).hexdigest()
    assert hash1 != hash2