import torch
model_path = input('model: ').replace('\r','')
ckpt = torch.load(model_path)
torch.save(ckpt, "updated-model.pt")
