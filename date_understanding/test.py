import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import tqdm
# from openai_cost_tracker import query_openai
# load_dotenv()
data = json.load(open("wrong_ans_correct_reason_dataset.json", "r"))

client = OpenAI()

correct=0
saved_responses = []

for d in tqdm.tqdm(data):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": d["prompt"]
            }
        ],
        max_tokens=50
    )
    model_ans = completion.choices[0].message.content
    # print(model_ans)
    saved_responses.append({"prompt": d["prompt"], "response": model_ans, "correct_answer": d["correct_answer"]})
    correct_ans = d["correct_answer"].split(" ")[1]
    if correct_ans in model_ans:
        correct+=1

print("Accuracy:", correct/len(data))

with open("responses_wrong_ans_correct_reason.json", "w") as f:
    json.dump(saved_responses, f, indent=4)




