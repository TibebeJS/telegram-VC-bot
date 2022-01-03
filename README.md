[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<br />
<p align="center">  
  <br/>
  <h1 align="center">🎙 Telegram VC Bot</h1>
  <p align="center">
    Manage your VC with ease. (Logging, Auto-Recording, and other cool features)
    <br />
    <br />
    <a href="https://github.com/TibebeJS/telegram-VC-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/TibebeJS/telegram-VC-bot/issues">Request Feature</a>
  </p>
  <br/>
  <br/>
</p>

## Getting Started

Git clone the repo:
```bash
git clone https://github.com/TibebeJS/telegram-VC-bot.git
```

Change directory into the newly created repository ("telegram-VC-bot")
```bash
cd telegram-VC-bot
```

### (Option 1) Install dependencies using `pip` from `requirements.txt`
```bash
pip install -r requirements.txt
```

### (Option 2) Install dependencies using `Pipenv`
```bash
pipenv install --python python3
```

and then activate the environment,
```bash
pipenv shell
```


Open up `.env` file in a text editor/IDE of your choice and replace with your IDs and credentials.
```env
API_ID=... # you can find these values from my.telegram.org
API_HASH="..."

GROUP_ID=... # group you want to monitor
LOG_CHANNEL_ID=... # group you want the logs to be posted to
LOGGER_BOT_TOKEN="..." # bot the sends the logs (the bot should be able to send in the log channel)
```

Finally, just run `main.py`
```
python main.py
```

More details can be found over: [Project canban](https://github.com/TibebeJS/telegram-VC-bot/projects/1)

## Contribution:

#### Pick a task from [Project canban](https://github.com/TibebeJS/telegram-VC-bot/projects/1), Create a feture issue, fork, code and send a PR :)

[forks-shield]: https://img.shields.io/github/forks/TibebeJS/telegram-VC-bot.svg?style=for-the-badge
[forks-url]: https://github.com/TibebeJS/telegram-VC-bot/network/members

[stars-shield]: https://img.shields.io/github/stars/TibebeJS/telegram-VC-bot.svg?style=for-the-badge
[stars-url]: https://github.com/TibebeJS/telegram-VC-bot/stargazers

[issues-shield]: https://img.shields.io/github/issues/TibebeJS/telegram-VC-bot.svg?style=for-the-badge
[issues-url]: https://github.com/TibebeJS/telegram-VC-bot/issues

[license-shield]: https://img.shields.io/github/license/TibebeJS/telegram-VC-bot.svg?style=for-the-badge
[license-url]: https://github.com/TibebeJS/telegram-VC-bot/blob/main/LICENSE