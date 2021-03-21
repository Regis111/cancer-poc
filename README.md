<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO 
<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Best-README-Template</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</p>
-->


<!-- TABLE OF CONTENTS
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details> -->



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This is proof of concept project of cancer prediction using Reservoir Computing and Approximate Bayesian Computation.

### Major third party apps

* [Qt](https://www.qt.io/)
* [Pyabc](https://pyabc.readthedocs.io/en/latest/)

<!-- ## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps. -->

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Regis111/cancer-poc.git
   ```
2. Install pipenv
   ```sh
   pip install pipenv
   ```
3. From root of repository move to `app` folder
   ```sh
   cd app/
   ```
4. Activate virtual environment
   ```sh
   pipenv shell
   ```
5. Install dependencies
   ```sh 
   pipenv install
   ```
6. Run application
   ```sh
   python app.py
   ```

<!-- USAGE EXAMPLES -->
## Example scenario with Approximate Bayesian Computation

Scenario starts with 8 points spread over 110 days.
![abc_state_1](./abc_scenario/podst.png)
Doctor calculates prediction. It tells about slow growth.
![abc_state_2](./abc_scenario/predykcja1.png)
Next, after 2 months, 4 points are added.
![abc_new_data](abc_scenario/4pomiary.png)
This time prediction shows steady growth. Doctor decides to plan treatments.
![abc_state_3](./abc_scenario/predykcja2.png)
Firstly, doctor does prediction 17th July
![abc_state_4](./abc_scenario/predykcja2_z_1_lekiem.png)
Next, prediction with treatments 17th July and 1st November.
![abc_state_5](./abc_scenario/predykcja2_z_2_lekami.png)

## Example scenario with Reservoir Computing

First situation is similar to abc example.
![rc_state_1](./rc_scenario/podst.png)
Doctor calculates prediction. It tells about slow growth.
![rc_state_2](./rc_scenario/predykcja1.png)
Next, after 2 months, 3 points are added.
![rc_new_data](./rc_scenario/3pomiary.png)
This time prediction shows steady growth. Doctor decides to plan treatments.
![rc_state_3](./rc_scenario/predykcja2.png)
Doctor does prediction 1st November and it is enough.
![rc_state_4](./rc_scenario/predykcja2_z_1_lekiem.png)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png -->
