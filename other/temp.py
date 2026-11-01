import re
from email.message import EmailMessage
from pathlib import Path

import pandas as pd

df = pd.read_csv("D:\\Github\\PhisPhing\\other\\CEAS_08.csv")

df = df[df["subject"] != "CNN Alerts: My Custom Alert"]
df = df[df["subject"] != "CNN.com Daily Top 10"]

df = pd.concat(
    [
        df[df["label"] == 1].sample(n=16, random_state=42),
        df[df["label"] == 0].sample(n=16, random_state=42),
    ]
)

df = df.sample(frac=1, random_state=42)

output = Path("eml")
output.mkdir(exist_ok=True)

for i, row in df.iterrows():
    msg = EmailMessage()
    msg["From"] = str(row["sender"])
    msg["Subject"] = str(row["subject"])
    msg.set_content(str(row["body"]))

    subject = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", str(row["subject"]))
    subject = subject.strip(" .")
    filename = f"{subject}_{i}_{row['label']}.eml"
    (output / filename).write_bytes(msg.as_bytes())

print(f"Total EML files created: {len(df)}")
print(df["label"].value_counts())
