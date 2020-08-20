---
layout: post
title: Linear Programming: College Football Power Rankings
---
This tool takes in statistics from college football games as input and generates Power Rankings for each team for Rush, Pass, Returns, and Special Teams. The rankings of each team are dependent on the team's performance relative to all other teams they played games against.  

The Python script solves using a **linearly constrained quadratic optimization problem**. The method used is "minimize" from the scipy.optimize library. The objective function is to minimize the squared error for combined offense/defense scores for each ranking.

The Python script works as an API which listens for / receives data (via http) from Excel, then solves and populates the Power Rankings in the Excel sheet. The Excel sheet uses a VBA script to send/receive via http.

[Python API](https://github.com/ptpro3/ptpro3.github.io/blob/master/Projects/SolverAPI.py)  
[Excel Data File](https://github.com/ptpro3/ptpro3.github.io/blob/master/Projects/NCAA_Data.xlsm)
