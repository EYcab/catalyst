import torch


def prepare_optimizable_params(params, fp16=False):
    master_params = list(filter(lambda p: p.requires_grad, params))

    if fp16:
        master_params = [
            param.detach().clone().float() for param in master_params
        ]
        for param in master_params:
            param.requires_grad = True

    return master_params


def assert_fp16_available():
    assert torch.backends.cudnn.enabled, \
        "fp16 mode requires cudnn backend to be enabled."


__all__ = ["assert_fp16_available", "prepare_optimizable_params"]
