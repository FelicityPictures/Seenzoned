# Seenzoned
API project for Software Development class (pd 6: Felicity Ng, Yicheng Wang, Dalton Wu, Roy Xu)

## Description
Seenzoned creates a bot called MarkovBot, who will learn speech patterns in a Slack channel and imitate it.

## Prerequisites
- Slack account
- Installation of Python's requests library
```bash
pip install requests
```
- Installation of Python's websocket-client library
```bash
pip install websocket-client
```

## Instructions
Creat a token.txt file containing your token for the Slack API (obtainable at https://api.slack.com/web)

| Command                                         | Result                                                                  |
|-------------------------------------------------|-------------------------------------------------------------------------|
| **Starting MarkovBot**                          |                                                                         |
| *app.py*                                        | run MarkovBot without debug statements                                  |
| *app.py -d*                                     | run MarkovBot with debug statements                                     |
| **Running MarkovBot**                           |                                                                         |
| *//markov*                                      | MarkovBot will talk like how people talk in this channel                |
| *//markov speak like \<channel\>*               | MarkovBot will speak like a channel if possible, or speak like softdev  |
| *//markov speak to me*                          | MarkovBot will message you                                              |
| *//markov speak to \<name\>*                    | MarkovBot will message the person with specificed name                  |
