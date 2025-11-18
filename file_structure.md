# This is my planned file structure

C:\Users\oe4vm\Proggen\Eqsl-Program\
|-------Eqsl_Program/
        |
        |----__pycache__                        <-- system cache autocreated
        |
        |----database_sql                       <-- folder for databases
        |    |----__init__.py                   <-- to make it module
        |    |----.gitkeep                      <-- to hold folder when empty
        |    |----new_test_db.db                <-- sql database
        |
        |----gui.data                           <-- folder with QT GUI files>
        |    |----__pycache__                   <-- system cache autocreated
        |    |----__init__.py                   <-- to make it module
        |    |----frm_help_view_ui.py           <-- gui design file compiled to .py
        |    |----frm_image_view_ui.py
        |    |----frm_main_window_ui.py
        |    |----frm_settings_ui.py
        |    |----frm_sql_create_ui.py
        |    |----frm_upload_ui.py
        |    |----frm_version_ui.py
        |
        |----scripts                            <-- folder for scripts called by main program
        |    |----__pycache__                   <-- system cache autocreated
        |    |----__init__.py                   <-- to make it module 
        |    |----gui_manager.py                <-- logic for windows call up
        |    |----settings_manager.py           <-- logic for settings window
        |
        |----support_data                       <-- folder for support files
        |    |----__init__.py                   <-- to make it module 
        |    |----dxcc_lookup.csv               <-- csv for second db table for dxcc lookup
        |    |----manual.html                   <-- program manual
        |    |----version.html                  <-- program version, credits
        |
        |----__init__.py                        <-- to make it module 
        |----eqsl_main_prog.py                  <-- main program file
        |----README.md                          <-- standard Readme
        |----settings.json                      <-- path for program use
        |----version_history.md                 <-- history of coding