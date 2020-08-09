<p align="center">
   <a href="https://github.com/JosephGolubchik/SuiterFinalProject">
   <img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/logo_small.png" title="Suiter - Final Project" alt="Suiter - Final Project">
</a>
   </p>

# Suiter - Final Project

An app for selecting a suit and adapting it to the user.


## Introduction

 * Project goal: Our goal is to create an app that helps users choose a suit and see how it looks on them before buying it.

 * The Suiter application will allow the user to choose a suit for himself and see how it will look on him. The user will provide a front view photograph of himself and 
   choose colors for the suit, and the application will draw the suit on top of him accordingly.


## Table of contents

> * [Introduction](#introduction)
> * [Table of contents](#table-of-contents)
> * [Installation](#installation)
>   * [Step #1: Android Studio and Python Installation](#step-1-android-studio-and-python-installation)
>   * [Step #2: Download the project folder (with all the files) from Github](#step-2-download-the-project-folder-with-all-the-files-from-github)
> * [Usage](#usage)
>   * [Explanation about ` AndroidProject ` folder](#explanation-about-androidproject-folder)
>   * [` AndroidProject ` (Suiter App) Example](#androidproject-suiter-app-example)
>   * [Explanation about ` PythonProject ` folder](#explanation-about-pythonproject-folder)
>   * [` PythonProject ` Algorithm](#pythonproject-algorithm)
>   * [Articles](#articles)
>   * [Tools](#tools)
> * [Authors](#authors)
> * [License](#license)
> * [Acknowledgments](#acknowledgments)


## Installation


#### Step #1: Python Installation

To run the projects in Python, you need to:
 * Install [Python 3.7](https://www.python.org/downloads/).
 * Install [Swig](http://www.swig.org/download.html)
 
 
 #### Step #2: Download the project folder (with all the files) from Github
 
 At the end of downloading the folder, [Usage](#usage) provides detailed explanations about the installations and uses of the ` PythonProject ` subfolder.
**Note: The explanation of all the algorithms is in the "Acknowledgments" content.


## Usage

The project (file) is divided into 2 parts:
1. ` AndroidProject ` - the app is available in the Google Play.
2. ` PythonProject ` folder - a folder with all the codes (and libraries) and graphic material (images) related to the general algorithm of clothing worn on a human object identified in the image (by algorithms related to deep learning and computer vision)


#### Explanation about ` AndroidProject `

This project is available in the Google Play and can be downloaded for all Android users:
[Download Suiter for Android now!](https://play.google.com/store/apps/details?id=com.suiter.suiterprototype)


#### ` AndroidProject ` (Suiter App) Example

![GIF](https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/AndroidPictures/suiter_video_gif_1.gif)


#### Explanation about ` PythonProject ` folder

After downloading the ` PythonProject ` directory, we reccomend two ways to install and run the project:<br>
1. First way: <br>
Install PyCharm,<br>
create a new project,<br>
paste the files from ` PythonProject ` into the project folder,<br>
run `pip install -r requirements.txt` in the PyCharm terminal. This will install the required libraries.<br>
You will probably get these errors during the installation:<br>
` ERROR: tensorflow 2.2.0 has requirement gast==0.3.3, but you'll have gast 0.2.2 which is incompatible.
ERROR: tensorflow 2.2.0 has requirement tensorboard<2.3.0,>=2.2.0, but you'll have tensorboard 1.15.0 which is incompatible.
ERROR: tensorflow 2.2.0 has requirement tensorflow-estimator<2.3.0,>=2.2.0, but you'll have tensorflow-estimator 1.15.1 which is incompatible. `<br>
This is ok and irrelevent to our project.<br>
Then go to ".\SuiterFinalProject\PythonProject\tf_pose_estimation\models\graph\cmu" and run "download.bat" to download "graph_opt.pb" which is needed for pose_estimation.
Then go to ".\SuiterFinalProject\PythonProject\image_background_remove_tool" and run "setup.bat" and hoose "u2net". This will download "u2net.pth" which is neede for background removal.<br>
Then go to ".\SuiterFinalProject\PythonProject\tf_pose_estimation\tf_pose\pafprocess" and run the command:<br>
`swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace`<br>
Then run the script `run.py`.

2. Second Way: <br>
Open a terminal in the directory and run `pip install -r requirements.txt`. This will install the required libraries.<br>
You will probably get these errors during the installation:<br>
` ERROR: tensorflow 2.2.0 has requirement gast==0.3.3, but you'll have gast 0.2.2 which is incompatible.
ERROR: tensorflow 2.2.0 has requirement tensorboard<2.3.0,>=2.2.0, but you'll have tensorboard 1.15.0 which is incompatible.
ERROR: tensorflow 2.2.0 has requirement tensorflow-estimator<2.3.0,>=2.2.0, but you'll have tensorflow-estimator 1.15.1 which is incompatible. `<br>
This is ok and irrelevent to our project.
Then go to ".\SuiterFinalProject\PythonProject\tf_pose_estimation\models\graph\cmu" and run "download.bat" to download "graph_opt.pb" which is needed for pose_estimation.
Then go to ".\SuiterFinalProject\PythonProject\image_background_remove_tool" and run "setup.bat" and choose "u2net". This will download "u2net.pth" which is neede for background removal.
Then go to ".\SuiterFinalProject\PythonProject\tf_pose_estimation\tf_pose\pafprocess" and run the command:<br>
`swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace`<br>
Then run `python run.py`

Running `run.py` will open a GUI interface:<br>
<p align="center">
   <img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/PythonPictures/empty_gui.PNG?raw=true"><br>
</p>
To choose an image you can either load an image url, or browse for an iamge in your computer. The image should be: <br>
Front view, Full body, the person should be in sort of an "A Pose".<br>
You can also choose colors for the trousers, shirt and jacket by pressing the corresponding buttons in the bottom of the screen.<br>

After choosing an image it will appear in the GUI:<br>
<p align="center">
   <img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/PythonPictures/image_gui.PNG?raw=true"><br>
</p>
After choosing an image and suit colors, Press "Process Image" to apply a suit to the image.<br>

The process will take around half a minute, and then the result will appear:<br>
<p align="center">
   <img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/PythonPictures/result_gui.PNG?raw=true"><br>
</p>


#### ` PythonProject ` Algorithm

<p align="center">
   <img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/PythonPictures/steps_v2.png?raw=true"><br>
</p>


#### Articles
* An research article explaining human identification and dressing it: 
[Image-based clothes changing system (by Zhao-Heng Zheng, Hao-Tian Zhang, Fang-Lue Zhang and Tai-Jiang Mu)](https://link.springer.com/content/pdf/10.1007/s41095-017-0084-6.pdf)

**Note: The person photos in the project presentation were taken from this article


## Authors

* **Eli Haimov (ID. 308019306)** - *Development Team Leader*
* **Yosi Golubchik (ID. 209195353)** - *Software Developer*


## License

* Copyright (C) Eli Haimov and Yosi Golubchik - All Rights Reserved
* Unauthorized copying of this file, via any medium is strictly prohibited
* Proprietary and confidential
* Written by Eli Haimov and Yosi Golubchik < yosieli2020@gmail.com >, July 2020


## Acknowledgments

* Explanation about [License](https://softwareengineering.stackexchange.com/questions/68134/best-existing-license-for-closed-source-code)


#### Deep Learning algorithms:
* Explanation about Pose estimation algorithm: [tf-pose-estimation (by ildoonet)](https://github.com/ildoonet/tf-pose-estimation)
* Explanation about background removal algorithm: [image-background-remove-tool (by OPHoperHPO)](https://github.com/OPHoperHPO/image-background-remove-tool)

#### Computer Vision algorithms:
* Explanation about Triangulation algorithm: [Triangulation (by OpenCV)](https://docs.opencv.org/3.4/d0/dbd/group__triangulation.html)
* Explanation about Piecewise Affine Tranformation algorithm: [Affine Transformations (by OpenCV)](https://docs.opencv.org/3.4/d4/d61/tutorial_warp_affine.html)

