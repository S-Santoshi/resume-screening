import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from torch.utils.data import Dataset, DataLoader

# Sample dataset
dataset = [
    ("Experienced software engineer with a background in machine learning.", "What programming languages are you proficient in?"),
    ("Marketing professional with a focus on digital marketing strategies.", "Can you tell me about your experience with social media marketing?"),
    ("Financial analyst skilled in data analysis and financial modeling.", "How do you approach financial forecasting?"),
    # Add more examples as needed
]
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
# Define dataset class
class ResumeDataset(Dataset):
    def __init__(self, dataset, tokenizer, max_length):
        self.dataset = dataset
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        resume_text, followup_question = self.dataset[idx]
        inputs = self.tokenizer.encode_plus(
            resume_text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        labels = self.tokenizer.encode(
            followup_question,
            add_special_tokens=False,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        return {
            "input_ids": inputs["input_ids"].flatten(),
            "attention_mask": inputs["attention_mask"].flatten(),
            "labels": labels.flatten()
        }

# Load GPT-2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
tokenizer.pad_token = '[PAD]'
# Fine-tuning parameters
batch_size = 4
max_length = 128
learning_rate = 1e-5
epochs = 3

# Prepare data loader
train_dataset = ResumeDataset(dataset, tokenizer, max_length)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Prepare optimizer and scheduler
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.9)

# Fine-tune the model
model.train()
for epoch in range(epochs):
    total_loss = 0
    for batch in train_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss}")

# Save the fine-tuned model
model.save_pretrained("fine_tuned_gpt2")
fine_tuned_model = GPT2LMHeadModel.from_pretrained("fine_tuned_gpt2")
fine_tuned_model.eval()

# Generate follow-up questions for a new resume text
new_resume_text = "Experienced project manager with a track record of delivering successful projects on time and within budget."
inputs = tokenizer.encode(new_resume_text, return_tensors="pt")
outputs = fine_tuned_model.generate(inputs, max_length=50, num_return_sequences=3, temperature=0.7, top_k=50)
followup_questions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

print("Follow-up Questions:")
for question in followup_questions:
    print("-", question)