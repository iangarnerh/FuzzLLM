
import sys
from openai import OpenAI
client = OpenAI()

def SendPrompts(tempFile, outFile):
    with open(tempFile, "r") as tf:
        with open(outFile, "w") as outFile:
            for line in tf:
                if len(line.strip()) != 0:
                    if line.strip()[0] != '#':
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            # model="gpt-4",
                            temperature=1.0,
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": line}
                            ]
                        )
                        outFile.write(completion.choices[0].message.content+"\n\n[end]\n\n")
                        
# First arg is the template file name
# Second arg is the output file name

if __name__ == '__main__':
    SendPrompts(sys.argv[1], sys.argv[2])
