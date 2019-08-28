# su2_gui
## The idea behind the project
In order to be able to parse quickly the SU2's configuration file
the idea was born to create dynamic SU2 config GUI editor

## Disclaimer
This repo is under development and it is rather the initial phase of the project

## Requirements
The app was developed using python 3.7.2

The needed packages are:
 - pyforms
 - pyqt5
 - mayavi (for plotting)
 - pyvalid

The requirements.txt should be uploaded sometime soon

## Stuff stored in this repo:
There are few modules created thus far:
 - The config parser which reads the input cfg file (or template) using regexes.
 - The GUI which displays and allows to load/edit/save the information stored in config
 - Some plotting features stored in mesh_tools folder (Allow for plotting of su2 mesh and selecting FFD box)
 - other stuff (explore to find out :))

## How to run this app

Simply run/execute home_window.py -> this should start thej GUI.

Keep in mind that parsing config may take few minutes.

## How parsing config file works
Using this info it creates single tab for each cfg chunk and fills
each tab with parameter found in that chunk i.e. in the following snippet:


% ------------- DIRECT, ADJOINT, AND LINEARIZED PROBLEM DEFINITION ------------%<br />
%<br />
% Physical governing equations (EULER, NAVIER_STOKES, NS_PLASMA)<br />
PHYSICAL_PROBLEM= EULER<br />
%<br />
% Mathematical problem (DIRECT, CONTINUOUS_ADJOINT)<br />
MATH_PROBLEM= DIRECT<br />
%<br />
% Restart solution (NO, YES)<br />
RESTART_SOL= NO<br />
<br />
% -------------------- COMPRESSIBLE FREE-STREAM DEFINITION --------------------%<br />
%<br />
% Mach number (non-dimensional, based on the free-stream values) <br />
MACH_NUMBER= 0.5<br />
%<br />
% Angle of attack (degrees, only for compressible flows)<br />
AOA= 0.0<br />
%<br />
% Side-slip angle (degrees, only for compressible flows)<br />
SIDESLIP_ANGLE= 0.0<br />
%<br />
% Free-stream pressure (101325.0 N/m^2 by default)<br />
FREESTREAM_PRESSURE= 101300.0<br />
%<br />
% Free-stream temperature (288.15 K by default)<br />
FREESTREAM_TEMPERATURE= 288.0<br />

2 chunks will be found:
- DIRECT, ADJOINT, AND LINEARIZED PROBLEM DEFINITION
    (parsed as DIRECT_ADJOINT_AND_LINEARIZED_PROBLEM_DEFINITION)
- COMPRESSIBLE FREE-STREAM DEFINITION
    (parsed as COMPRESSIBLE_FREE_STREAM_DEFINITION)
   
In chunk no. 1 (DIRECT_ADJOINT_AND_LINEARIZED_PROBLEM_DEFINITION) the
following parameters will be found:
- PHYSICAL_PROBLEM
- MATH_PROBLEM
- RESTART_SOL

If comments are provided for params parser would attempt to extract 
available options from the comment (i.e. YES/NO for RESTART_SOL param)

The comment is added as a tooltip for text box control.

## What's done after the config is parsed

The parsed config is passed to the GUI which dynamically creates the UI structure based on the provided input:
 - If for the given parameter the options to choose from were found in the config the combo box will be created for that param
 - If there are no `allowed values` in the parsed config for a given parameter the simple text box will be created to edit his param

## What are checkboxes for?

There are checkboxes in two places:
 - next to parameters -> those checkboxes allow for enabling/disabling the certain parameters when saving config (disabled parameter will not be saved)
 - next to section names -> those checkboxes will enable/disable entire section of config

## Adding parameters and sections

There is a way to add a parameter or a section to a UI from a UI level:
 - each section tab should have a `Add new parameter` button -> it will add a desired parameter to the current section/tab.
 Remember that providing the parameter name and default value is obligatory. If `allowed values` are provided as well default value should be in `allowed values`
- the section selector (checkbox list on the left) has a button `Add new section` which allows to create a new, empty section tab

## Status
The GUI works (loads/edits/saves) SU2 cfg files which follow
the convention of the original cfg file template

It should be quite intuitive to use - feel free to 
experiment and let me know if you find any bugs :)