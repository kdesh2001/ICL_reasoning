import json
import random

k=16

correct_data = json.load(open("tweet_hate_correct_ans_correct_reason.json"))["examples"]
incorrect_data = json.load(open("tweet_hate_incorrect_ans_incorrect_reason.json"))["examples"]

cacr = []
cawr = []
wawr = []
wacr = []

for i in range(0, len(correct_data)):
    indices = list(range(len(correct_data)))
    indices.pop(i)
    indices_kshots = random.sample(indices, k)
    # print("Chosen kshots:", indices_kshots, "****")
    correct_kshots = [correct_data[ii] for ii in indices_kshots]
    incorrect_kshots = [incorrect_data[ii] for ii in indices_kshots]
    cacr_datapoint = {}
    cacr_datapoint['prompt'] = ""
    cawr_datapoint = {}
    cawr_datapoint['prompt'] = ""
    wawr_datapoint = {}
    wawr_datapoint['prompt'] = ""
    wacr_datapoint = {}
    wacr_datapoint['prompt'] = ""
    for j in range(0,k):
        
        question = correct_kshots[j]["input"]
        assert question==incorrect_kshots[j]["input"]
        correct_options = correct_kshots[j]["target_scores"]
        
        incorrect_options = incorrect_kshots[j]["target_scores"]
        correct_reason = correct_kshots[j]["reason"]
        incorrect_reason = incorrect_kshots[j]["reason"]
        correct_ans = ""
        incorrect_ans = ""
        for key, value in correct_options.items():
            if value==1:
                correct_ans = key
                break
        for key, value in incorrect_options.items():
            if value==1:
                incorrect_ans = key
                break
        correct_options = list(correct_options.keys())
        correct_options = [s.replace(",", "") for s in correct_options]
        correct_options.sort()
        incorrect_options = list(incorrect_options.keys())
        incorrect_options = [s.replace(",", "") for s in incorrect_options]
        incorrect_options.sort()
        correct_options_str = " ".join([f"({chr(97 + i)}) {value}" for i, value in enumerate(correct_options)])
        incorrect_options_str = " ".join([f"({chr(97 + i)}) {value}" for i, value in enumerate(incorrect_options)])

        correct_ans = correct_ans.replace(",", "")
        incorrect_ans = incorrect_ans.replace(",", "")
        
        correct_ans = f"({chr(97 + correct_options.index(correct_ans))}) {correct_ans}"
        incorrect_ans = f"({chr(97 + incorrect_options.index(incorrect_ans))}) {incorrect_ans}"


        cacr_datapoint["prompt"]+=(question+"\n")
        cawr_datapoint["prompt"]+=(question+"\n")
        wawr_datapoint["prompt"]+=(question+"\n")
        wacr_datapoint["prompt"]+=(question+"\n")
        # Options
        cacr_datapoint["prompt"]+=(correct_options_str+"\n")
        cawr_datapoint["prompt"]+=(correct_options_str+"\n")
        wawr_datapoint["prompt"]+=(incorrect_options_str+"\n")
        wacr_datapoint["prompt"]+=(incorrect_options_str+"\n")
        # Answer
        cacr_datapoint["prompt"]+=("Answer:"+correct_ans+"\n")
        cawr_datapoint["prompt"]+=("Answer:"+correct_ans+"\n")
        wawr_datapoint["prompt"]+=("Answer:"+incorrect_ans+"\n")
        wacr_datapoint["prompt"]+=("Answer:"+incorrect_ans+"\n")
        # Reason
        cacr_datapoint["prompt"]+=("Reason: "+correct_reason+"\n***\n")
        cawr_datapoint["prompt"]+=("Reason: "+incorrect_reason+"\n***\n")
        wawr_datapoint["prompt"]+=("Reason: "+incorrect_reason+"\n***\n")
        wacr_datapoint["prompt"]+=("Reason: "+correct_reason+"\n***\n")
    
    # Test example
    cacr_datapoint["prompt"]+=(correct_data[i]["input"]+"\n")
    cawr_datapoint["prompt"]+=(correct_data[i]["input"]+"\n")
    wawr_datapoint["prompt"]+=(correct_data[i]["input"]+"\n")
    wacr_datapoint["prompt"]+=(correct_data[i]["input"]+"\n")

    correct_options = correct_data[i]["target_scores"]
    correct_ans = ""
    for key, value in correct_options.items():
        if value==1:
            correct_ans = key
            break
    
    correct_options = list(correct_options.keys())
    correct_options.sort()
    correct_options_str = " ".join([f"({chr(97 + i)}) {value}" for i, value in enumerate(correct_options)])
    correct_ans = f"({chr(97 + correct_options.index(correct_ans))}) {correct_ans}"

    cacr_datapoint["prompt"]+=(correct_options_str+"\nAnswer:")
    cawr_datapoint["prompt"]+=(correct_options_str+"\nAnswer:")
    wawr_datapoint["prompt"]+=(correct_options_str+"\nAnswer:")
    wacr_datapoint["prompt"]+=(correct_options_str+"\nAnswer:")

    cacr_datapoint["correct_answer"]=correct_ans
    cawr_datapoint["correct_answer"]=correct_ans
    wawr_datapoint["correct_answer"]=correct_ans
    wacr_datapoint["correct_answer"]=correct_ans

    cacr.append(cacr_datapoint)
    cawr.append(cawr_datapoint)
    wawr.append(wawr_datapoint)
    wacr.append(wacr_datapoint)

with open("tweet_hate_correct_ans_correct_reason_dataset.json", "w") as f1:
    json.dump(cacr, f1, indent=4)

with open("tweet_hate_correct_ans_wrong_reason_dataset.json", "w") as f2:
    json.dump(cawr, f2, indent=4)

with open("tweet_hate_wrong_ans_wrong_reason_dataset.json", "w") as f3:
    json.dump(wawr, f3, indent=4)

with open("tweet_hate_wrong_ans_correct_reason_dataset.json", "w") as f4:
    json.dump(wacr, f4, indent=4)
