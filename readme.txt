* Author: 
Stantec Consulting, Ahjung Kim(ahjung.kim@stantec.com)

* Requirements: 
ArcGIS Desktop 10.3 or above

* Install Dependency: 
Run Check_Null.exe found under Check_Null folder.

* How to Use: 
From ArcMap or ArcCatalog, connect to "rFHL QC" folder.  Open "FEMA_QC.tbx\Update Null" tool and
enter/drag-and-drop/browse to your workspace(i.e. file geodatabase). Click OK to run the tool.

* Overview:
The tool will get field information (required/applicable, version, field type, feature ID) from the look up tables (found under "document" folder) and update any "pseudo null" values found in the input workspace.

    # Required fields:
    - String : Change “”, -9999, -8888, U or null to NP
    - Numeric : Change -9999 or null to -8888
    - Date : Change 9/9/9999 or null to 8/8/8888
    - T/F : Change “” or null to “U”

    # Applicable fields:
    - Version 'x.1.x.x'
        String : Change NP, -9999, -8888, U, " " or null to “”
        Numeric : Change -8888 or null to -9999
        Date : Change 8/8/8888 or null to 9/9/9999
        T/F : Change U or null to “”

    - Version non-'x.1.x.x'
        String : Change “”, " ", -9999 or null to “”;  change -8888 or U to NP
        Numeric : Change null to -9999; -8888 stays the same
        Applicable Date : Change null to 9/9/9999; 8/8/8888 stays the same
        T/F : Change null to “”; U stays the same

User message will display tables and feature classes with no features;

User message will display feature and update information;

User message will warn if "feature class(table)_field name" combination is not found in the look up table.

When following fields have invalid values, user warning will show and log file (csv) will be created.
    - DFIRM_ID, VERSION_ID, or feature ID is null in any feature class or table
    - S_Fld_Haz_Ar : FLD_ZONE is null or NP



