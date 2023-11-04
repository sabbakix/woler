# woler
Simple Wake on Lan application

## Installation

Only for windows at the moment. 
Unzip the zip file into a folder. 
Edit the **list.csv** file in the same directory as woler.exe and fill each row with the name and the mac address of the pc to wake up.

For example:

    PC Name, MAC
    PC1, '01.02.03.04.05.06'
    PC2, '07.08.08.09.10.11'

Then double click on woler.exe and select type the pc number to wake up then type Enter.

![cmd](docs/001_cmd.png)

## For development

Install wakeonlan dependency

    pip install wakeonlan