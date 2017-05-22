# ==========================================================================
# Name: Update_IDs.py
# Purpose: Automated tool to updated primary key field in the FIRM database
# Prerequisite: python 2.7, arcpy
# Inputs: File or Personal Geodatabase from the ArcMap interface
# 
# Authors: Andrea Weakland
# Stantec Consulting Services
# 
# Created: 4/15/2015
# Updated: 4/15/2015
# Revised: 05/22/2017v(S_Gen_Struct.STRUCT_ID and L_Cst_Struct.STRUCT_ID need to have STRUCTID_2 added to them and the original STRUCT_ID field calculated into the new field."
#          06/2017 By Ahjung Kim
# ==========================================================================

# List of table, temporary new ID field to calc over the original values
table_field_list = [
    # ('table name','temporary field name','original field name'}
    ('FIRM_Spatial_Layers\S_Cst_Tsct_Ln', 'TRANLNID_2', 'TRAN_LN_ID'),
    ('FIRM_Spatial_Layers\S_Cst_Tsct_Ln', 'TBASELNID_2', 'TBASELN_ID'),
    ('FIRM_Spatial_Layers\S_Cst_Tsct_Ln', 'CSTMDLID_2', 'CST_MDL_ID'),

    ('FIRM_Spatial_Layers\S_Tsct_Basln', 'CSTMDLID_2', 'CST_MDL_ID'),
    ('FIRM_Spatial_Layers\S_Tsct_Basln', 'TBASELNID_2', 'TBASELN_ID'),

    ('FIRM_Spatial_Layers\S_XS', 'XSLNID_2', 'XS_LN_ID'),

    ('FIRM_Spatial_Layers\S_Submittal_Info', 'CSTMDLID_2', 'CST_MDL_ID'),

    ('FIRM_Spatial_Layers\S_Cst_Gage', 'CSTMDLID_2', 'CST_MDL_ID'),

    ('FIRM_Spatial_Layers\S_Gen_Struct', 'STRUCTID_2', 'STRUCT_ID'),

    ('L_XS_Struct', 'XSLNID_2', 'XS_LN_ID'),

    ('L_XS_Elev', 'XSLNID_2', 'XS_LN_ID'),

    ('L_Mtg_POC', 'MTGID_2', 'MTG_ID'),

    ('L_Meetings', 'MTGID_2', 'MTG_ID'),

    ('L_Cst_Model', 'CSTMDLID_2', 'CST_MDL_ID'),

    ('L_Cst_Tsct_Elev', 'TRANLNID_2', 'TRAN_LN_ID'),

    ('L_Cst_Struct', 'STRUCTID_2', 'STRUCT_ID')
]
# List of table and field names to assign auto-incrementing IDs
auto_increment_list = [
    #  (table name, field name)
    ('FIRM_Spatial_Layers\S_Cst_Tsct_Ln', 'TRAN_LN_ID'),
    ('FIRM_Spatial_Layers\S_XS', 'XS_LN_ID'),
    ('FIRM_Spatial_Layers\S_Wtr_Ln', 'WTR_LN_ID'),
    ('FIRM_Spatial_Layers\S_Wtr_Ar', 'WTR_AR_ID'),
    ('FIRM_Spatial_Layers\S_Tsct_Basln', 'TBASELN_ID'),
    ('FIRM_Spatial_Layers\S_Trnsport_Ln', 'TRANS_ID'),
    ('FIRM_Spatial_Layers\S_Topo_Confidence', 'LOWCONF_ID'),
    ('FIRM_Spatial_Layers\S_Submittal_Info', 'SUBINFO_ID'),
    ('FIRM_Spatial_Layers\S_Subbasins', 'SUBBAS_ID'),
    ('FIRM_Spatial_Layers\S_Riv_Mrk', 'RIV_MRK_ID'),
    ('FIRM_Spatial_Layers\S_Profil_Basln', 'BASELN_ID'),
    ('FIRM_Spatial_Layers\S_POL_AR', 'POL_AR_ID'),
    ('FIRM_Spatial_Layers\S_PLSS_AR', 'PLSS_AR_ID'),
    ('FIRM_Spatial_Layers\S_PFD_Ln', 'PFD_ID'),
    ('FIRM_Spatial_Layers\S_LOMR', 'LOMR_ID'),
    ('FIRM_Spatial_Layers\S_LiMWA', 'LIMWA_ID'),
    ('FIRM_Spatial_Layers\S_Levee', 'LEVEE_ID'),
    ('FIRM_Spatial_Layers\S_Label_Pt', 'LABEL_ID'),
    ('FIRM_Spatial_Layers\S_Label_Ld', 'LEADER_ID'),
    ('FIRM_Spatial_Layers\S_Hydro_Reach', 'REACH_ID'),
    ('FIRM_Spatial_Layers\S_HWM', 'HWM_ID'),
    ('FIRM_Spatial_Layers\S_Gen_Struct', 'STRUCT_ID'),
    ('FIRM_Spatial_Layers\S_Gage', 'GAGE_ID'),
    ('FIRM_Spatial_Layers\S_Fld_Haz_Ln', 'FLD_LN_ID'),
    ('FIRM_Spatial_Layers\S_Fld_Haz_Ar', 'FLD_AR_ID'),
    ('FIRM_Spatial_Layers\S_FIRM_Pan', 'FIRM_ID'),
    ('FIRM_Spatial_Layers\S_Datum_Conv_Pt', 'DATCONPTID'),
    ('FIRM_Spatial_Layers\S_Cst_Gage', 'CSTGAGE_ID'),
    ('FIRM_Spatial_Layers\S_CBRS', 'CBRS_ID'),
    ('FIRM_Spatial_Layers\S_BFE', 'BFE_LN_ID'),
    ('FIRM_Spatial_Layers\S_Base_Index', 'BASE_ID'),
    ('FIRM_Spatial_Layers\S_Alluvial_Fan', 'ALLUVL_ID'),
    ('L_XS_Struct', 'XS_STR_ID'),
    ('L_XS_Elev', 'XS_ELEV_ID'),
    ('L_Survey_Pt', 'SURVPT_ID'),
    ('L_Summary_Elevations', 'SUMELEV_ID'),
    ('L_Summary_Discharges', 'SUMDSCH_ID'),
    ('L_Profil_Panel', 'PROFPAN_ID'),
    ('L_Profil_Label', 'PROFLBL_ID'),
    ('L_Profil_Bkwtr_El', 'PROF_BW_ID'),
    ('L_Pol_FHBM', 'FHBM_ID'),
    ('L_Pan_Revis', 'REVIS_ID'),
    ('L_Mtg_POC', 'POC_ID'),
    ('L_MT2_LOMR', 'LOMR_ID'),
    ('L_Meetings', 'MTG_ID'),
    ('L_ManningsN', 'MANN_ID'),
    ('L_Cst_Struct', 'CST_STR_ID'),
    ('L_Cst_Struct', 'STRUCT_ID'),
    ('L_Cst_Model', 'CST_MDL_ID'),
    ('L_Comm_Revis', 'COM_REV_ID'),
    ('Study_Info', 'STD_NFO_ID'),
    ('L_Cst_Tsct_Elev', 'CT_INFO_ID')
]

import arcpy
from arcpy import env, da

# variables
field_type = 'TEXT'
field_length = 32
field_is_nullable = True
field_is_required = False
flag = None
env.workspace = arcpy.GetParameterAsText(0)

# a list to hold empty table names. To show empty table warning to user only once
emtpy_list1 = []
# emtpy_list2 = []


def AddField(table, temp_field):

    # Check if table is empty
    result = arcpy.GetCount_management(table)
    count = int(result.getOutput(0))
    # If table is empty, show message
    if count == 0:
        # Don't show table name if it's a duplicate
        if table not in emtpy_list1:
            arcpy.AddMessage("-" + table + " is empty")
            emtpy_list1.append(table)

    else:
        # Check if temp ID field already exists
        if len(arcpy.ListFields(table, temp_field)) > 0:
            arcpy.AddWarning("-" + temp_field + " already exists in " + table)
        # Add temporary ID field if it doesn't exist in the table
        else:
            arcpy.AddMessage("-Add field " + temp_field + " to " + table + "...")
            arcpy.AddField_management(table, temp_field, field_type, "", "", field_length, "", field_is_nullable,
                                      field_is_required, "")

# Calculate temp ID field with original ID values
def CalcField(table, temp_field, original_field):
    # Check if table is empty
    result = arcpy.GetCount_management(table)
    count = int(result.getOutput(0))
    #
    if count > 0:
        fields = [temp_field, original_field]
        arcpy.AddMessage("-Updating " + temp_field + " with " + original_field + " in " + table)
        with da.UpdateCursor(table, fields) as cursor:
            for row in cursor:
                row[0] = row[1]
                cursor.updateRow(row)
    # else:
    #     if table not in emtpy_list2:
    #         arcpy.AddMessage("-" + table + " is empty")
    #         emtpy_list1.append(table)


def autoIncrement(pStart=1, pInterval=1):
    global rec
    if (rec == 0):
        rec = pStart
        return rec
    else:
        rec += pInterval
        return rec


def AssignAutoIncrementingID(table, field):
    result = arcpy.GetCount_management(table)
    count = int(result.getOutput(0))
    if count == 0:
        pass
        arcpy.AddMessage("-" + table + " is empty")
    else:
        # Populate target field with incrementing ID
        with da.UpdateCursor(table, field) as cursor:
            arcpy.AddMessage("-Assigning ID to " + field + " in " + table + "(" + str(count) + " rows)")
            for row in cursor:
                row[0] = autoIncrement()
                cursor.updateRow(row)

try:
    if __name__ == '__main__':
        arcpy.AddMessage("\n" + "Adding temporary ID fields " + arcpy.env.workspace + "...")
        for table, id_field, existing_field in table_field_list:
            AddField(table, id_field)
        #
        edit = arcpy.da.Editor(arcpy.env.workspace)
        edit.startEditing(False, True)
        edit.startOperation()
        arcpy.AddMessage("\n" + "Calculating field...")
        for table, id_field, existing_field in table_field_list:
            CalcField(table, id_field, existing_field)


        arcpy.AddMessage("\n" + "Assigning auto-incrementing IDs...")
        for table, field in auto_increment_list:
            rec = 0
            AssignAutoIncrementingID(table, field)
        arcpy.AddMessage(
            "Completed adding temporary fields and updating primary and foreign key fields in " + arcpy.env.workspace)
        edit.stopOperation()
        edit.stopEditing(True)
except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))

finally:
    del table_field_list, field_type, field_length, field_is_nullable, field_is_required,
