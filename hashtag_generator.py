from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import random
nltk.download('punkt')

tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-base-tag-generation")
model = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-base-tag-generation")

def genrate_hashtag(text:str):

    inputs = tokenizer([text], max_length=512, truncation=True, return_tensors="pt")
    output = model.generate(**inputs, num_beams=8, do_sample=True, min_length=10,
                            max_length=64)
    decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    tags = list(set(decoded_output.strip().split(", ")))

    # choose 3 random tags
    tags_chosen = random.sample(tags, 3)
    tags_chosen = [tag.replace(" ", "") for tag in tags_chosen]

    # print the tags
    tags_string = "#" + " #".join(tags_chosen)

    return tags_string

if __name__ == "__main__":

    genrate_hashtag()