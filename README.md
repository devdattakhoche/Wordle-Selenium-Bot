
[![Contributors][contributors-shield]][contributors-url]
[![Language][Language-shield]][Language-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]




<!-- PROJECT LOGO -->
<br />
<p align="center">
  

  <h2 align="center">Wordle Bot</h2>

  <p align="center">
    A simple python bot to solve today's wordle
    <br />
    ·
    <a href="https://github.com/devdattakhoche/Wordle-Selenium-Bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/devdattakhoche/Wordle-Selenium-Bot/issues">Request Feature</a>
  </p>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/49261633/154818636-7d2f0702-609a-4860-9ca0-e6165b31e4dd.png">
</p>

<!-- TABLE OF CONTENTS -->


## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project
<p align="center">
  <img src="https://user-images.githubusercontent.com/49261633/154830750-5b45838e-543d-4a52-95cf-a8928e2fa821.gif">
</p>

Wordle has been fairly liked and much popular game. Solving wordle feels really really good.
I built a bot for the same who will do it for, now watching the bot solve the worlde feels much better than me solving it myself.😂😂
I bot opens the wordle site which is (https://www.nytimes.com/games/wordle/index.html) and solves the wordle by itself.

I have used two strategies to solve a problem :
1. Randomized Algorithm with some pre info gathering
2. Freq distrbution of letters in the valid words

Here are the results for the same when we run it on 1000 words:
Strategy 1:

```
Success Percentage :  70.39999999999999
Failure Percentage :  29.599999999999998
Average Attempts :  4.802556818181818
```


Strategy 2:
```
Success Percentage :  87.7
Failure Percentage :  12.3
Average Attempts :  4.6419612314709235

```
I will further keep improving the bot with some addons.
A list of commonly used resources that I found helpful are listed in the acknowledgements.
I have listed the source of the data in the acknowledegements.

### Built With

* [Python](https://www.python.org/)
* [Selenium](https://selenium-python.readthedocs.io/)

<!-- GETTING STARTED -->
## Getting Started

Getting started with the bot is fairly easy.
Make sure you are using an or virtual environment(not compulsory but recommended) for installing all the libraries. Once you have activated your virtual env you can install all the packages with this command below :
```
pip install -r requirments.txt
```
Now you can run the bot with:
```
python wordle.py
```

To test the bot I have made wordle game which is the `wordle_test.py`, you can always change it if you want.
To test bot you can `wordle_test.py` :
```
python wordle_test.py

```
By default it will run it on 1000 random words, to change the argument you can pass `--Nwords` in cli and mention the number of words :
```
python wordle_test.py --Nwords 100
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Srajan1122/TK-Player/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- ## Contributors -->




<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Data-Wordle-Words](https://github.com/tabatkins/wordle-list/blob/main/words)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/devdattakhoche/Wordle-Selenium-Bot
[contributors-url]: https://github.com/devdattakhoche/Wordle-Selenium-Bot/graphs/contributors
[activity-shield]: https://img.shields.io/github/commit-activity/m/devdattakhoche/Wordle-Selenium-Bot
[activity-url]: https://github.com/devdattakhoche/Wordle-Selenium-Bot/commits/main
[version-shield]: https://img.shields.io/github/v/tag/devdattakhoche/Wordle-Selenium-Bot
[version-url]: https://github.com/devdattakhoche/Wordle-Selenium-Bot/releases
[language-shield]: https://img.shields.io/github/languages/top/devdattakhoche/Wordle-Selenium-Bot
[language-url]: https://www.python.org/
[forks-shield]: https://img.shields.io/github/forks/devdattakhoche/Wordle-Selenium-Bot
[forks-url]:https://github.com/devdattakhoche/Wordle-Selenium-Bot/network/members
[stars-shield]: 	https://img.shields.io/github/stars/devdattakhoche/Wordle-Selenium-Bot
[stars-url]: https://github.com/devdattakhoche/Wordle-Selenium-Bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/devdattakhoche/Wordle-Selenium-Bot
[issues-url]: hhttps://github.com/devdattakhoche/Wordle-Selenium-Bot/issues




