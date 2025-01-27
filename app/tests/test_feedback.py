from main import handle_negative_feedback, negative_feedback_times

def test_handle_negative_feedback():
    negative_feedback_times.clear()
    handle_negative_feedback()
    assert len(negative_feedback_times) == 1
