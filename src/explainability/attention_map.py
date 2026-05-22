import torch


def extract_attention_weights(
    model
):

    attentions = []

    for layer in model.encoder.layers:

        if hasattr(
            layer.self_attn,
            "attn_output_weights"
        ):

            attentions.append(
                layer.self_attn.attn_output_weights
            )

    return attentions