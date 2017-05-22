# ==========================================================================
# Name: Strip_DFIRM_IDs.py
# Purpose: remove DFIRM ID from ID and SOURCE_CIT fields for NFHL RiskMap DFIRM database
# Prerequisite: python 2.7, arcpy
# Inputs: File or Personal Geodatabase from the ArcMap interface
# 
# Returns: Creates, add rules, and validates topology per FEMA guidance 
# 
# Authors: Andrea Weakland
# Stantec Consulting Services
# 
# Created: 5/5/2015
# Updated: 5/5/2015
# Revised: 06/2016 by Ahjung Kim
# ==========================================================================


import arcpy
from arcpy import da, env

# table name, field name, and type(required)"s list. User may edit this list.
table_list = [
    ("L_Comm_Info", "COM_NFO_ID", "R"),
    ("L_Comm_Revis", "COM_REV_ID","R"),
    ("L_Comm_Revis", "COM_NFO_ID","R"),
    ("L_Cst_Model", "CST_MDL_ID","R"),
    ("L_Cst_Struct", "CST_STR_ID","R"),
    ("L_Cst_Struct", "STRUCT_ID","R"),
    ("L_Cst_Tsct_Elev", "CT_INFO_ID","R"),
    ("L_Cst_Tsct_Elev", "TRAN_LN_ID","R"),
    ("L_ManningsN", "MANN_ID","R"),
    ("L_Meetings", "MTG_ID","R"),
    ("L_Meetings", "COM_NFO_ID","R"),
    ("L_MT2_LOMR", "LOMR_ID","R"),
    ("L_Mtg_POC", "POC_ID","R"),
    ("L_Mtg_POC", "MTG_ID","R"),
    ("L_Pan_Revis", "REVIS_ID","R"),
    ("L_Pol_FHBM", "FHBM_ID","R"),
    ("L_Pol_FHBM", "COM_NFO_ID","R"),
    ("L_Profil_Bkwtr_El", "PROF_BW_ID","R"),
    ("L_Profil_Label", "PROFLBL_ID","R"),
    ("L_Profil_Panel", "PROFPAN_ID","R"),
    ("L_Source_Cit", "SOURCE_CIT","R"),
    ("L_Summary_Discharges", "SUMDSCH_ID","R"),
    ("L_Summary_Discharges", "NODE_ID","R"),
    ("L_Summary_Elevations", "SUMELEV_ID","R"),
    ("L_Summary_Elevations", "NODE_ID","R"),
    ("L_Survey_Pt", "SURVPT_ID","R"),
    ("L_XS_Elev", "XS_ELEV_ID","R"),
    ("L_XS_Elev", "XS_LN_ID","R"),
    ("L_XS_Struct", "XS_STR_ID","R"),
    ("L_XS_Struct", "XS_LN_ID","R"),
    ("Study_Info", "STD_NFO_ID","R"),
    ("FIRM_Spatial_Layers\S_Alluvial_Fan", "ALLUVL_ID","R"),
    ("FIRM_Spatial_Layers\S_Alluvial_Fan", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Base_Index", "BASE_ID","R"),
    ("FIRM_Spatial_Layers\S_Base_Index", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_BFE", "BFE_LN_ID","R"),
    ("FIRM_Spatial_Layers\S_BFE", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_CBRS", "CBRS_ID","R"),
    ("FIRM_Spatial_Layers\S_CBRS", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Cst_Gage", "CSTGAGE_ID","R"),
    ("FIRM_Spatial_Layers\S_Cst_Gage", "CST_MDL_ID","A"),
    ("FIRM_Spatial_Layers\S_Cst_Gage", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Cst_Tsct_Ln", "TRAN_LN_ID","R"),
    ("FIRM_Spatial_Layers\S_Cst_Tsct_Ln", "TBASELN_ID","R"),
    ("FIRM_Spatial_Layers\S_Cst_Tsct_Ln", "CST_MDL_ID","A"),
    ("FIRM_Spatial_Layers\S_Cst_Tsct_Ln", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Datum_Conv_Pt", "DATCONPTID","R"),
    ("FIRM_Spatial_Layers\S_Datum_Conv_Pt", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_FIRM_Pan", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_FIRM_Pan", "FIRM_ID","R"),
    ("FIRM_Spatial_Layers\S_Fld_Haz_Ar", "FLD_AR_ID","R"),
    ("FIRM_Spatial_Layers\S_Fld_Haz_Ar", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Fld_Haz_Ln", "FLD_LN_ID","R"),
    ("FIRM_Spatial_Layers\S_Fld_Haz_Ln", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Gage", "GAGE_ID","R"),
    ("FIRM_Spatial_Layers\S_Gage", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Gen_Struct", "STRUCT_ID","R"),
    ("FIRM_Spatial_Layers\S_Gen_Struct", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_HWM", "HWM_ID","R"),
    ("FIRM_Spatial_Layers\S_HWM", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Hydro_Reach", "REACH_ID","R"),
    ("FIRM_Spatial_Layers\S_Hydro_Reach", "UP_NODE","A"),
    ("FIRM_Spatial_Layers\S_Hydro_Reach", "DN_NODE","A"),
    ("FIRM_Spatial_Layers\S_Hydro_Reach", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Label_Ld", "LEADER_ID","R"),
    ("FIRM_Spatial_Layers\S_Label_Pt", "LABEL_ID","R"),
    ("FIRM_Spatial_Layers\S_Levee", "LEVEE_ID","R"),
    ("FIRM_Spatial_Layers\S_Levee", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_LiMWA", "LIMWA_ID","R"),
    ("FIRM_Spatial_Layers\S_LiMWA", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_LOMR", "LOMR_ID","R"),
    ("FIRM_Spatial_Layers\S_LOMR", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Nodes", "NODE_ID","R"),
    ("FIRM_Spatial_Layers\S_Nodes", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_PFD_Ln", "PFD_ID","R"),
    ("FIRM_Spatial_Layers\S_PFD_Ln", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_PLSS_Ar", "PLSS_AR_ID","R"),
    ("FIRM_Spatial_Layers\S_PLSS_Ar", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Pol_Ar", "POL_AR_ID","R"),
    ("FIRM_Spatial_Layers\S_Pol_Ar", "COM_NFO_ID","A"),
    ("FIRM_Spatial_Layers\S_Pol_Ar", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Profil_Basln", "BASELN_ID","R"),
    ("FIRM_Spatial_Layers\S_Profil_Basln", "START_ID","R"),
    ("FIRM_Spatial_Layers\S_Profil_Basln", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Riv_Mrk", "RIV_MRK_ID","R"),
    ("FIRM_Spatial_Layers\S_Riv_Mrk", "START_ID","R"),
    ("FIRM_Spatial_Layers\S_Riv_Mrk", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Stn_Start", "START_ID","R"),
    ("FIRM_Spatial_Layers\S_Stn_Start", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Subbasins", "SUBBAS_ID","R"),
    ("FIRM_Spatial_Layers\S_Subbasins", "NODE_ID","A"),
    ("FIRM_Spatial_Layers\S_Subbasins", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Submittal_Info", "SUBINFO_ID","R"),
    ("FIRM_Spatial_Layers\S_Submittal_Info", "CST_MDL_ID","A"),
    ("FIRM_Spatial_Layers\S_Submittal_Info", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Topo_Confidence", "LOWCONF_ID","R"),
    ("FIRM_Spatial_Layers\S_Topo_Confidence", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Trnsport_Ln", "TRANS_ID","R"),
    ("FIRM_Spatial_Layers\S_Trnsport_Ln", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Tsct_Basln", "TBASELN_ID","R"),
    ("FIRM_Spatial_Layers\S_Tsct_Basln", "CST_MDL_ID","A"),
    ("FIRM_Spatial_Layers\S_Tsct_Basln", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Wtr_Ar", "WTR_AR_ID","R"),
    ("FIRM_Spatial_Layers\S_Wtr_Ar", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_Wtr_Ln", "WTR_LN_ID","R"),
    ("FIRM_Spatial_Layers\S_Wtr_Ln", "SOURCE_CIT","R"),
    ("FIRM_Spatial_Layers\S_XS", "XS_LN_ID","R"),
    ("FIRM_Spatial_Layers\S_XS", "START_ID","R"),
    ("FIRM_Spatial_Layers\S_XS", "SOURCE_CIT","R")
]

def strip(in_table, in_field, in_type):
    #  Check if table is empty
    result = arcpy.GetCount_management(table)
    count = int(result.getOutput(0))

    # If table has no rows, alert user
    if count == 0:
        arcpy.AddMessage("\n"+ table + " has no rows...")
    # If table has data, proceed with stripping DFIRM ID
    else:
        arcpy.AddMessage ("\n"+"Stripping DFIRM ID off "+in_field+ " in "+in_table+"...")
        fields = [in_field, "OBJECTID"]
        with da.UpdateCursor(in_table, fields) as cursor:
            for row in cursor:
                #  if current cell's value is Null, update with "" or "NP" depending on the field type
                if row[0] is None:

                    if in_type == "R":
                        row[0]="NP"
                        arcpy.AddWarning("- "+in_table+", "+in_field+" OID: "+str(row[1])+" is Null. Updated with NP")
                    elif in_type == "A":
                        row[0]=""
                        arcpy.AddWarning("- "+in_table+", "+in_field+" OID: "+str(row[1])+" is Null. Updated with "+ '""')

                else:
                    # if current cell's value is not Null, find the index for underscore
                    underscore_index = row[0].find("_")
                    strip_index=underscore_index+1

                    # if the parsed value does not contain underscore, alert user and do nothing
                    if underscore_index== -1:
                        pass
                        # arcpy.AddMessage ("- "+in_table+", "+in_field+" OID: "+str(row[1])+" has no underscore")
                    # if the parse value contains underscore, strip characters before + 1
                    else:
                        row[0] = row[0][strip_index:]
                #  save updates
                cursor.updateRow(row)

# Used only for testing
def  copy_db():
    print "Copying geodatabase..."
    arcpy.Copy_management("C:\\TEMP\FEMA\\testdata\\04015C_appended.gdb","C:\\TEMP\\FEMA\\04015C_appended.gdb")

try:
    if __name__ == '__main__':
        # copy_db()
        env.workspace  = arcpy.GetParameterAsText(0)
        arcpy.AddMessage("Started stripping DFIRM ID off ID and SOURCE CIT fields for: " + arcpy.env.workspace)

        #  Start an edit session. Update feature data set can't be done outside edit session
        edit = arcpy.da.Editor(arcpy.env.workspace)
        edit.startEditing(False, True)
        edit.startOperation()
        # For each item in the list, strip DFIRM ID
        for table, id_field, type in table_list:
            strip(table, id_field, type)

        #  Stop edit session
        edit.stopOperation()
        edit.stopEditing(True)
        arcpy.AddMessage("\n"+"All done!")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))

finally:
    del table_list
