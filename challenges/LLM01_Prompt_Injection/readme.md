# LLM01- Prompt Injection

A Prompt Injection Vulnerability occurs when user prompts alter the LLM’s behavior or output in unintended ways. These inputs can affect the model even if they are imperceptible to humans, therefore prompt injections do not need to be human-visible/readable, as long as the content is parsed by the model.

This challenge is a playground of 8 levels. In levels 1–7 an assistant knows a secret password and each level adds a defense to protect it. Level 8 is the original indirect injection challenge: a chatbot where the admin stored a secret key in the chat history.

Application URL: http://127.0.0.1:5001

## Levels

All levels are unlocked from the start.

| # | Level | Defense | Hint |
|---|---|---|---|
| 1 | No Protection | None | Sometimes the simplest approach works. |
| 2 | Basic Prompt Protection | The system prompt says not to reveal the password | Instructions are only words. Can a role or a story make sharing feel allowed? |
| 3 | Self-Check Protection | The assistant also reviews its own answer before replying | It looks for the password as written. What if the answer held it in another form? |
| 4 | External Output Validation | A second LLM reads every reply and withholds it if it reveals the password | The validator has to recognise the password. Which forms might it miss? |
| 5 | Stronger Topic Restriction | The assistant refuses to discuss the password in any way | It avoids the topic. Can you get it without ever talking about passwords? |
| 6 | External Input Validation | A second LLM reads your message first and blocks attempts to get the password | The validator only sees your message. Make it look harmless. |
| 7 | AI Defense in Depth | Topic restriction, self-check, input and output validation together | Every layer has a blind spot. You need one prompt that slips past all of them. |
| 8 | Indirect Injection | A guardian model screens chat messages; `/fetch` summarises web pages | External URL feature can help. |

## Challenge Objective

- **Levels 1–7:** make the assistant reveal its secret password, then enter it in the "Submit the secret" form on the level page. A correct secret shows the flag and a one-line story about the secret. The form is checked by the application only; it is never sent to the model.
- **Level 8:** log in as a participant and use Prompt Injection/Jailbreak techniques to get the admin's secret key. The flag appears when the key is revealed. The admin role is restricted.

Each message on levels 1–7 is sent to the model on its own, without the earlier conversation, so every attempt starts fresh.

## Requirements

```shell
ollama pull mistral:7b-instruct-v0.3-q4_K_M   # levels 1-7, assistant and validators (pinned)
ollama pull mistral                           # level 8
ollama pull granite3-guardian                 # level 8 guardian
```

The pinned tag has the same digest as `mistral:latest` at the time the levels were tuned, so Ollama reuses the downloaded layers if you already have it. Pinning keeps a newer `latest` from silently changing how the levels behave.

All model calls use temperature 0, so the same prompt gives the same reply on the same machine.
