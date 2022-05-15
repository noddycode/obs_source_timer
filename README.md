# OBS Source Timer

This is a simple program that will make a single source appear and disappear (with any applied filters and transistions) at a set frequency and for a set duration.

## Instructions for use

*If you already have OBS configured to use python, skip to step 4*
1. Download Python 3.9.12 from the following link: https://www.python.org/downloads/release/python-3912/
  - Make sure the *lib* directory of the new installation contains a file called *libpython3.9.dylib*
2. Open OBS Studio and navigate to Tools > Scripts
3. Under the "Python Settings" tab, point OBS to the outermost directory of your Python 3.9.12 installation
  - If the script is not working, navigate to Help > Log Files > View Current Log File to make sure OBS has correctly discovered your python installation
4. Clone this repository to any directory
5. Under the "Scripts" tab, click the "+" button and add the script from the directory you cloned it to. You may keep the script in this directory to easily update it from the repository
6. In the settings pane to the right, select the source that you would like to make visible/invisible from the Source dropdown menu
7. Set the Frequency time and units to determine how often you would like the source to appear
8. Set the Duration time and unit to dertmine how long to wait between appearances
9. Click "Start" to start the timer. You may click "Stop" at any time to stop the timer
  - Note: Any changes you make to these settings will automatically stop the timer. Click "Start" to start the timer again

Please report any issues in the Issues tab of this repository.
