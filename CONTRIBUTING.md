# Welcome contributor(s)!

Thanks for considering contributing to Research Analytics. 
We are very excited to make academic research faster and easier, and build together an Open Source academic tech community :microscope::purple_heart::computer:

# Table of Contents
1. [About the Project](#about-the-project)
2. [Project Status](#project-status)
3. [Getting Started](#getting-started)

# About the project

Research Analytics was thought by "lazy" research students who wanted to automate as many research tasks as possible. 
Having a general interest in coding, data science, and software development, we took on this first project of building a data science web app for doing academic research.

The project was first released in February 2022 :baby:

# Project status

Research Analytics has just been publicly released in February 2022. The current release version is version 1.0.

## Deployment
The web app works and does the job it was designed for. However, being deployed on Heroku (free plan) it is quite slow :snail:

More computing power should improve the app's performance.

## Where is the data fetched from?
The data about research papers are collected from [Semantic Scholar](https://www.semanticscholar.org/product/api) who provides a very well-documented API :heart:

Currently, the app makes use of the API developer plan which only allows for 100 queries per 5 minutes. An upgrade in the query rate is absolutely necessary as a single search on Research Analytics involves about 25 queries.

## How is the app built?
The app has been developed with the amazing [Plotly Dash](https://plotly.com/dash/) python framework. It is built on top of Flask, Plotly.js, React, and React.js.
Dash offers endless possibilites for creating custom data-oriented web apps from NLP to object detection, predictive analytics and more.

# Getting started

Please check out our [Code of Conduct]() before diving into coding :raised_hands:

If you wish to suggest new features for the app, please create an issue and we'll consider it. Keep in mind that we're trying to make researchers' lives easier, so try to put yourself in a researcher's shoes when suggesting a new feature.

# Contribution suggestions

You may want to consider improving the following:

1. Responsivness of the app
2. App's design and internal CSS stylesheet
3. Improving the code's performance (more elegant and shorter code)
