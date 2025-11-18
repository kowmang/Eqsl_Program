
# Version 0.0.4
### (database handling)


* **all files** added adif file (from any logbook) import
                deleted dxcc list query (not useful when adif import)
* **gui_data**  some changes in design (only minor)
* **adif_importer** added and logic for import adif into database included
                    also crosscheck for duplicates and if fields in adif are
                    not filled the field is NULL
* **design**    added popup window when import data to see how many and if ready
* **qsl_image_importer** added take qsl cards from folder and check with adif db 
                         then when found image converted to blob and insert in db


                        
---

# Version 0.0.3
### (start with logic for settings window)


* **gui_manager** added all windows settings (open, close, reject)
* **version.html** updated design (center text)
* **gui_data**  updated some name definition in all windows
* **settings_manager** created for settings_window logic
* **settings.json** for file path storage
* **settings_manager** logic for database creation (db predefined with colums and tables);
* **settings_manager** logic for dxcc list import (always overrides existing file!!);      
* **settings_manager** logic for download folder selection added
* **gui_manager** function of button reset; new db; select db and text field for db path added;
* **gui_manager** function of button select dxcc and text field for dxcc path added
* **gui_manager** function of button select download folder and text field for download folder path added


---

# Version 0.0.2
### (start of coding, in different branches)


* **create_sql_db** created, script for first database creation
* **gui_data** all .ui files are compiled to _ui.py for python use
* **__init__.py** in all folders integrated to make folder as module for python
* **file_structure** create to visualize the file structre 
* **eqsl_main_prog** now triggers a gui manager
* **gui_manager** added in scripts



---

# Version 0.0.1
### (preparing for coding)


* **eqsl_main_prog** file created
* **README** created
* **Version_history** created
* **gui_data** folder created and filled with .ui files from QT Designer 
    + frm_help_view
    + frm_image_view
    + frm_main_window
    + frm_settings
    + frm_upload
    + frm_version
    + frm_sql_create
* **support_data** folder created, filled with support files
    + dxcc_lookup
    + version
    + manual
* **settings_data** folder created, filled with settings files
    + settings   
* **database_sql** folder created, will be filled with database
* **scripts** folder created, filled with script files
* testing upload to .git

---

## Project begin 08.11.2025
