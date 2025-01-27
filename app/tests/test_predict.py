from app.main import predict_text, handle_negative_feedback, negative_feedback_times

def test_predict_text_positive():
    text = "This is a great product!"
    label, probabilities = predict_text(text)
    assert label == "positive"
    assert probabilities[1] > probabilities[0]

def test_predict_text_negative():
    text = "I don't like this product."
    label, probabilities = predict_text(text)
    assert label == "negative"
    assert probabilities[0] > probabilities[1]
