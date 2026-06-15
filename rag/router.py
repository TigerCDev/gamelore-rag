FACTUAL_KEYWORDS = ['who', 'when', 'where', 'which', 'how many', 'how old']


def classify_question(question):
    question_lower = question.lower()

    for keyword in FACTUAL_KEYWORDS:
        if keyword in question_lower:
            return 'factual'

    return 'narrative'
