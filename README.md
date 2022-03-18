# Attendance Marking Module
Group 6: Dang Minh Tuan, Ta Minh Tien, Nguyen Tien Dung
# Prerequisite
Use the following command in command console or powershell to install required libs
```
    pip install requirements.txt
```
# Usage

The application provides a modular kits of function and a GUI to mark attendance through Face Recognition. It can easily integrate into existing security systems as a second layer of protection to ensure unregistered people can not enter certain places without permission. It also mark and log the verification of registered people passed through the system. The module uses a pre-train model from OpenFace to convert face images into 128D Vectors to calculate the Euclidean Distance or the similarity between two people. The module come with a GUI and script to let user quickly gather image through webcam. The general usage is as follow:

#### Step 1: Gather Data
After starting the GUI, enter the list of desired names in the top TextBox seperated by comma (,). The GUI will try to access the webcam, a new window will open showing the current captured live from webcam. 

Align face as centered as possible in the webcam window, then Hold "P" to start saving samples, altering facial expression and slightly turn around to provide a good quality sample. The webcam window will close after taking 100 pictures and will open again if there were multiple names entered. All the captured images will be save in folder with the name entered in the folder "images".

![ezcv logo](https://raw.githubusercontent.com/ karrystare /DPL/master/GUI.png)

#### Step 2: Create a Database
The module will read through all the images inside the folder "images" and convert them into vectors through the OpenFace model. It will create a dictionary with the names as keys and a list of vectors as value for each name. The user can choose to manipulate the processed data here if wished using the options such as "Add Entry", "Remove Entry", "Save Database" and "Load Database". Simply clear out the "List of Names" TextBox and replace with respective name, i.e Name of Entry to Add/Remove or Name of Database to Save/Load (The Module will automatically add ".npy" at the end).

#### Step 3: Verification Module
After Creating/Loading Database, enter a Shift Name in the middle TextBox to assign a shift to this run. Click "Run Verification" to open webcam and start the process. For any face appeared on the camera, the module will automatically detect and crop the ROI of the faces then try to verify it. Unregistered Faces will not pass as likely target since the module used the closest distance instead of a standard classification model. Each successful verification will add into a log file created in the "logs" folder with the time the person verified and their name. Each person can only verify once in each shift and the "attendance.txt" will save all the verified name in each shift. To Exit, Hold "Q" in the webcam window.
