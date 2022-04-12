-------------------------------------------------------------------------------
SEGMENT VIEWER
-------------------------------------------------------------------------------
A software tool for comparing forced-aligners.
Author: Carlos Daniel Hernández Mena
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
REQUIREMENTS
-------------------------------------------------------------------------------

The SEGMENT VIEWER was tested in Ubuntu only. The requirements are :

- Python 3 - https://www.python.org/
- SoX - http://sox.sourceforge.net/
- Flask - https://flask.palletsprojects.com/en/2.1.x/
- An internet browser

Notice that SEGMENT VIEWER does not produce any TextGrid. You have to
create the input TextGrids before using the SEGMENT VIEWER.

-------------------------------------------------------------------------------
SETTING UP
-------------------------------------------------------------------------------

After cloning the repository go to the script SEGMENT_VIEWER.py and identify 
the following lines of code:

#CONTROL PANEL

PATH_RUFA_TGS = <path-to-TextGrids_RUFA

PATH_MFA_TGS  = <path-to-TextGrids_MFA

PATH_WAVS     = <path-to-WAVS>

Update these lines with the actual absolute paths in your system. They paths
have to point to the corresponding directory inside the CORPUS folder
of this recipe.

-------------------------------------------------------------------------------
RUNNING THE SEGMENT VIEWER
-------------------------------------------------------------------------------

Open a terminal and using "cd" go to one of these directories: SV_Word_Level 
or SV_Phoneme_Level and then type:

	$ python3 SEGMENT_VIEWER.py
	
If everything is okay you will see the following instructions:

Run the SEGMENT VIEWER TYPING:
python3 RUN_SV.py

And open this link in your browser:
http://127.0.0.1:5000/

Follow the instructions to run the SEGMENT VIEWER.

-------------------------------------------------------------------------------
ACKNOWLEDGEMENTS
-------------------------------------------------------------------------------

Thanks to the "ERASMUS - Staff Mobility Program" for make the SEGMENT VIEWER 
possible.

-------------------------------------------------------------------------------

