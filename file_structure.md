# This is my planned file structure

C:\Users\oe4vm\Proggen\Eqsl-Program\
|-------Eqsl_Program/
        |
        |----__pycache__                        <-- system cache autocreated
        |
        |----.vscode                            <-- vs code folder
        |    |----settings.json                 <-- vs code and extensions settings
        |
        |----database_sql                       <-- folder for databases
        |    |----__init__.py                   <-- to make it module
        |    |----.gitkeep                      <-- to hold folder when empty
        |    |----new_test_db.db                <-- sql database
        |
        |----gui.data                           <-- folder with QT GUI files>
        |    |----__pycache__                   <-- system cache autocreated
        |    |----__init__.py                   <-- to make it module
        |    |----frm_bulk_card_import_ui.py    <-- gui design file compiled to .py
        |    |----frm_help_view_ui.py     
        |    |----frm_image_view_ui.py
        |    |----frm_main_window_ui.py
        |    |----frm_settings_ui.py
        |    |----frm_single_card_import_ui.py
        |    |----frm_upload_ui.py
        |    |----frm_version_ui.py              
        |
        |----scripts                            <-- folder for scripts called by main program
        |    |----__pycache__                   <-- system cache autocreated
        |    |----__init__.py                   <-- to make it module
        |    |----adif_importer.py              <-- imports adif file in database
        |    |----gui_manager.py                <-- logic for windows call up
        |    |----image_viewer_dialog.py        <-- viewer for bulk card showing
        |    |----qsl_image_importer.py         <-- importer for bulk image import
        |    |----qsl_single_image_importer.py  <-- importer for single image import
        |    |----settings_manager.py           <-- logic for settings window
        |
        |----support_data                       <-- folder for support files
        |    |----manual_images                 <-- folder for manual support files 
        |    |    |----main_window.png          <-- various images shown in the manual
        |    |----__init__.py                   <-- to make it module
        |    |----default_preview.png           <-- default logo picture
        |    |----dxcc_lookup.csv               <-- csv for second db table for dxcc lookup
        |    |----manual.html                   <-- program manual
        |
        |----__init__.py                        <-- to make it module
        |----.timetracker                       <-- worktime tracker file
        |----eqsl_main_prog.py                  <-- main program file
        |----file_structure.md                  <-- provides the filestructure in md
        |----README.md                          <-- standard Readme
        |----settings.json                      <-- path for program use
        |----version_history.md                 <-- history of coding