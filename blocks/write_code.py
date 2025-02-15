from openai import OpenAI


def call_openai(messages):
    client = OpenAI()
    response = client.chat.completions.create(model="o3-mini", messages=messages)
    return response.choices[0].message.content.strip()


# Generates (or modifies) code based on instructions and review feedback using model "o3-mini".
def generate_code(instructions):
    msgs = [
        {"role": "system", "content": "You are a helpful assistant that writes code."},
        {"role": "user", "content": instructions},
    ]
    code = call_openai(msgs)
    return code


if __name__ == "__main__":
    instructions = "Write a function that prints 'Hello, world!'"
    code = generate_code(instructions)
    print(code)
