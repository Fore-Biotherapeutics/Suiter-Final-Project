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


#### Step #1: Android Studio and Python Installation

To run the projects in Android Studio and Python, you need to:
 * Install [Android Studio](https://developer.android.com/studio).
 * Install [Python 3.7](https://www.python.org/downloads/).
 * Install [Swig](http://www.swig.org/download.html)
 
 
 #### Step #2: Download the project folder (with all the files) from Github
 
 At the end of downloading the folder, [Usage](#usage) provides detailed explanations about the installations and uses of the 2 subfolders (` AndroidProject ` and ` PythonProject `), respectively.
 
**Note: The explanation of all the algorithms is in the "Acknowledgments" content.


## Usage

The project (file) is divided into 2 parts, 2 sub-files:
1. ` AndroidProject ` folder - a folder with all the codes and graphic material (images) associated with the Suiter application.
2. ` PythonProject ` folder - a folder with all the codes (and libraries) and graphic material (images) related to the general algorithm of clothing worn on a human object identified in the image (by algorithms related to deep learning and computer vision)


#### Explanation about ` AndroidProject ` folder

When you enter Android Studio, go to: ` File -> New -> Import Project.. ` and select the ` AndroidProject ` subfolder in the project folder (` Suiter-Project `).


<a><img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/AndroidPictures/pic1.jpg" title="Suiter - Final Project" alt="Suiter - Final Project"></a>

Explanation of the main files of this folder (` AndroidProject `):
* ` app -> manifest -> AndroidManifest.xml `: XML file with all the permissions of this application.
* ` app -> java -> com -> example -> suiterfinalproject -> Activities -> CreateOutfitActivity `: A JAVA file that contains the main codes of this application, such as: initializing the objects and setting the actions of all the buttons in the application.


<a><img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/AndroidPictures/pic2.jpg" title="Suiter - Final Project" alt="Suiter - Final Project"></a>
* ` app -> java -> com -> example -> suiterfinalproject -> Adapters -> ColorListAdapter `: A JAVA file which is responsible for matching the color list to all the items of the suit in this application.
* ` app -> java -> com -> example -> suiterfinalproject -> Models -> .. `: 
   1. ` ClothingColor ` : A JAVA file with functions (setters and getters) for receiving and returning the colors of the clothing details in this application.
   2. ` ClothingItem ` : A JAVA file with functions (setters and getters) for receiving and returning the colors of the clothing specific category in this application.
   3. ` ColorData ` : A JAVA file with arrays with a list of all the colors of the suit items in this application.
   4. ` Outfit ` : A JAVA file with functions (setters and getters) for receiving and returning the clothing items in this application.
* ` app -> res -> drawable `: Folder with all the graphic material (images) that appears in this application.

**Note: All the graphic material is in the ` drawable ` folder, when the project is uploaded in the explained instructions, all the graphic materials will also be uploaded automatically, which will be downloaded with the entire ` AndroidProject ` subfolder (in the process of downloading the ` Suiter-Project ` project file).


<a><img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/AndroidPictures/pic3.jpg" title="Suiter - Final Project" alt="Suiter - Final Project"></a>
* ` app -> res -> layout -> activity_create_outfit.xml `: An XML file with all the layers of objects and graphics that appear on the main page of the application. This file is responsible for the all this page and size and location of these parts.


<a><img src="https://github.com/JosephGolubchik/SuiterFinalProject/blob/master/Pictures%20to%20README/AndroidPictures/pic4.jpg" title="Suiter - Final Project" alt="Suiter - Final Project"></a>
* ` app -> res -> layout -> activity_main.xml `: An XML file that serves as a login page for the application, a kind of temporary page that pops up at the login to the application and is followed by the main page of this application.
* ` app -> res -> layout -> info.xml `: An XML file used as an information page. By pressing the information button, located in the lower area on the right side of the app, the above page will appear.


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

* **Eli Haimov (ID. 308019306)** - *Programmer*
* **Yosi Golubchik (ID. 209195353)** - *Programmer*


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

