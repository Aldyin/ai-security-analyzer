MODELS = {}


def register_model(
    name,
    model
):

    MODELS[name] = model


def get_model(
    name
):

    return MODELS.get(name)