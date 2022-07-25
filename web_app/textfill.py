from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

class TextFill:
    def __init__(self, model_checkpoint="distilbert-base-uncased-finetuned-cvpr"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model = AutoModelForMaskedLM.from_pretrained(model_checkpoint)
        self.punc = "!.,':;-()&|?"
        self.punc_len = len(self.punc)
    
    def _predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        token_logits = self.model(**inputs).logits

        # Find the location of [MASK] and extract its logits
        mask_token_index = torch.where(inputs["input_ids"] == self.tokenizer.mask_token_id)[1]
        mask_token_logits = token_logits[0, mask_token_index, :]

        return mask_token_logits
    
    def _get_top_k(self, mask_token_logits, top_k):
        k2 = top_k + self.punc_len
        top_topkens = torch.topk(mask_token_logits, k2, dim=1).indices[0].tolist()
        out = []
        cnt = 0
        for token in top_topkens:
            pred = self.tokenizer.decode([token])
            if not (pred in self.punc):
                out.append(pred)
                cnt += 1
            if cnt == top_k: break
        return out
    
    def fill_mask(self, text, top_k=10):
        mask_token_logits = self._predict(text)
        out = self._get_top_k(mask_token_logits, top_k)
        return out