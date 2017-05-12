import susi_python as susi


# Check a simple reply
def test_reply():
    answer = susi.ask("hi")
    assert answer is not None
