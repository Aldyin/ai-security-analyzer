def format_output(results):
    labels = []
    probs = []

    for lang, prob in results:
        labels.append(lang)
        probs.append(prob)

    text = "\n".join([f"{l}: {p*100:.2f}%" for l, p in results])

    return text, labels, probs