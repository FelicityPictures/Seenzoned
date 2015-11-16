# Seenzoned
API project for Software Development class (pd 6: Felicity Ng, Yicheng Wang, Dalton Wu, Roy Xu)

## Description
Seenzoned creates a bot called MarkovBot, who will learn speech patterns in a Slack channel and imitate it.

## Commands
| Command                                         | Result                                                                  |
|-------------------------------------------------|-------------------------------------------------------------------------|
| *//markov*                                      | markovBot will talk like how people talk in this channel                |
| *//markov speak like <channel>*                 | markovBot will speak like a channel if possible, or speak like softdev  |
| *//markov speak to me*                          | markovBot will message you                                              |
| *//markov speak to <name>*                      | markovBot will message the person with specificed name                  |
| *//markov help or //markov <invalid command>*   | markovBot will print this string"""                                     |

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
