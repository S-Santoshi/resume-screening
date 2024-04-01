# from transformers import GPT2Tokenizer, GPT2LMHeadModel

# # Load pre-trained GPT-2 tokenizer and model
with open("resume.txt","r") as f:
    resume=f.read()
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# model = GPT2LMHeadModel.from_pretrained('gpt2')
# input_ids = tokenizer.encode(resume, return_tensors='pt')

# prompt = f"Based on the provided resume below, \n\n{resume}\n\n,please generate follow-up questions to the candidate to understand the candidate better:"

# output = model.generate(input_ids, max_length=600, num_return_sequences=3, temperature=0.7, pad_token_id=tokenizer.eos_token_id, 
#                         bos_token_id=tokenizer.bos_token_id, top_p=0.95, early_stopping=True, do_sample=True, 
#                         top_k=50, eos_token_id=tokenizer.eos_token_id)
# print("*************************************************")
# for i, sample_output in enumerate(output):
#     decoded_output = tokenizer.decode(sample_output[len(input_ids[0]):], skip_special_tokens=True)
#     print(f"Follow-up Question {i+1}: {decoded_output}")


from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load pre-trained T5 tokenizer and model
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

prompt = f"Based on the provided resume below, please generate follow-up questions:\n\n{resume}\n\n"

# Tokenize the prompt
inputs = tokenizer.encode(prompt, return_tensors='pt', max_length=512, truncation=True)

# Generate follow-up questions based on the prompt
output = model.generate(inputs, max_length=100, temperature=0.7)

# Decode and print the generated follow-up questions
print("Generated Follow-up Questions:")
for i, sample_output in enumerate(output):
    decoded_output = tokenizer.decode(sample_output, skip_special_tokens=True)
    print(f"Follow-up Question {i+1}: {decoded_output}")