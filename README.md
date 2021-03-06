# OBS Source Timer

This is a simple program that will make a single source appear and disappear (with any applied filters and transistions) at a set frequency and for a set duration.

## Installation

*If you already have OBS configured to use python, skip to step 4*
1. Download the appropriate version of Python for your system
    - For MacOS, use python 3.9
    - For Windows, use python 3.6
2. Open OBS Studio and navigate to Tools > Scripts
3. Under the "Python Settings" tab, point OBS to the outermost directory of your Python 3.9.12 installation
    - If the script is not working, navigate to Help > Log Files > View Current Log File to make sure OBS has correctly discovered your python installation
4. Clone this repository to any directory
5. Under the "Scripts" tab, click the "+" button and add the script from the directory you cloned it to. You may keep the script in this directory to easily update it from the repository

## Usage

1. In the settings pane to the right, select the source that you would like to make visible/invisible from the Source dropdown menu
2. Set the Frequency time and units to determine how often you would like the source to appear
3. Set the Duration time and unit to dertmine how long to wait between appearances
4. Save your configuration and start the timer
    1. Click the "Add/Update" button to add/update a source configuration with the current settings without starting a timer
    2. Click "Start Timer" to add/update the source with the currently selected settings and immediately start the timer
3. Click "Start All" to start all currently configured timers
5. Click "Stop Timer" to stop the timer for the currently selected source.
6. Click "Stop All" to stop all timers. All saved configurations will still be available if you decide to restart a timer

## Saving/Loading Configurations

1. You can save all currently configured sources by clicking the "Browse" button for the "Path to save to" field, inputting a file name, and then clicking "Save Configuration Settings". **You must click "Save Configuration Settings" to store your settings**
2. To load a saved configuration file, click the "Browse" button for the "Path to load from" field, navigate to your saved configuration file, and then click "Load Configuration File". This will restore all saved configuration settings for each source in the file.
3. You can manulaly edit the JSON files, however note that **there is no validation for files**. If the configuration file fails to load properly, the script may crash or simply not work
4. Check "Run at startup" to have OBS automatically load the config you have selected and start all timers when you open OBS or reload the script

Please report any issues in the Issues tab of this repository.
