"""
   Copyright 2016 Stantec Consulting
   Author: Ahjung Kim (ahjung.kim@stantec.com)
   Date: August 2016
   Revised:
   Summary: This script updates pseudo null values in the input workspace updates them.
            The update rules were provided by Andrea Weakland (Andrea.Weakland@stantec.com)
   Usage: Use for quality assurance for rFHL database
"""

import arcpy
from arcpy import env
from xlrd import open_workbook
import os

# global variables
reqd_dict = {}
length_dict = {}
gentype_dict = {}

invalid_id_list = []

# get workspace from user input
env.workspace = arcpy.GetParameterAsText(0)
myWorkspace = env.workspace

# lookup table details
project_dir = os.path.dirname(os.path.dirname(__file__))

uid_lookup_tb = project_dir + "\\document\\NFHL_UID_Fields.xls"
uid_worksheet_name = "UID_Fields"

firmdb_lookup_tb = project_dir + "\\document\\FIRM_DB_Fields.xlsx"
firmdb_worksheet_name = "Fields"


# Parse UID table and build a dictionary
workbook = open_workbook(uid_lookup_tb)
worksheet = workbook.sheet_by_name(uid_worksheet_name)
table = (table.value for table in worksheet.col(0))
uid_fields = (uid_fields.value for uid_fields in worksheet.col(1))
uid_dict = dict(zip(table, uid_fields))


def build_firm_db_dict():
    db_workbook = open_workbook(firmdb_lookup_tb)
    db_worksheet = db_workbook.sheet_by_name(firmdb_worksheet_name)
    values = []

    # Parse look up table and build dictionary
    for excel_row in range(1, db_worksheet.nrows):
        col_names = db_worksheet.row(0)
        col_value = []
        for name, col in zip(col_names, range(db_worksheet.ncols)):
            value = db_worksheet.cell(excel_row, col).value
            value = str(value)
            col_value.append((name.value, value))
        values.append(col_value)

    for a, b, c, d, e, f in values:
        key = a[1] + "_" + b[1]
        ra_value = c[1]
        length_value = e[1]
        gentype_value = f[1]

        reqd_dict[key] = ra_value
        length_dict[key] = length_value
        gentype_dict[key] = gentype_value


def update_null(in_data):
    # if feature class has 0 features, skip checking it for null values
    result = arcpy.GetCount_management(in_data)
    count = int(result.getOutput(0))

    if count > 0:
        #
        if count == 1:
            count_unit = " row"
        else:
            count_unit = " rows"

        arcpy.AddMessage("Checking {0}({1}{2})... \n".format(in_data, count, count_unit))

        # get feature ID from the UID dictionary
        fc_uid = uid_dict.get(in_data)

        # list all fields in current feature class
        fields = arcpy.ListFields(in_data)

        for field in fields:
            # warn user if these fields have null values. They should not be updated.
            if field.name in ["DFIRM_ID", "VERSION_ID", fc_uid]:
                fields = ['OBJECTID', field.name]

                with arcpy.da.SearchCursor(in_data, fields) as s_cursor:
                    for row in s_cursor:
                        if row[1] in [None, '']:
                            arcpy.AddWarning("   {0} : {1}, OID {2} is Null or NP \n".format(in_data, field.name,
                                                                                             row[0]))

                            # create a list which will be used in creating output log
                            invalid_id_list.append((in_data, field.name))

            # skip theses fields
            # elif field.name in ['SHAPE_STArea__', 'SHAPE_STLength__', 'SHAPE_Length', 'SHAPE_Length',
            #                     'OBJECTID', 'SHAPE', 'SHAPE_Area']:
            #     pass

            # update pseudo null values in all other fields
            elif field.name not in ['SHAPE_STArea__', 'SHAPE_STLength__', 'SHAPE_Length', 'SHAPE_Length',
                                                     'OBJECTID', 'SHAPE', 'SHAPE_Area', "Shape", "Shape_Length"]:
                key = in_data + "_" + field.name
                reqd_val = reqd_dict.get(key)
                gentype_val = gentype_dict.get(key)
                length_val = length_dict.get(key)
                # arcpy.AddMessage("{0} {1} {2} length is {3}".format(key, reqd_val, gentype_val, length_val))

                # if "feature class_field" value is not in the lookup table, notify user
                if reqd_val is None or gentype_val is None:
                    arcpy.AddWarning("   {0} : {1} is not in the lookup table\n".format(in_data, field.name))

                # get general type value from the dictionary
                # gentype_val = gentype_dict.get(key)

                # ObjectID val is used for user message
                fields = ["VERSION_ID", field.name, "OBJECTID"]

                with arcpy.da.UpdateCursor(in_data, fields) as u_cursor:
                    for row in u_cursor:

                        # Get current field value and format for user message
                        if row[1] == "":
                            current_val = "''"
                        elif row[1] == ' ':
                            current_val = "' '"
                        else:
                            current_val = row[1]

                        # Rules for updating null values in required fields
                        if reqd_val == "R":

                            def update_required(new_val):

                                arcpy.AddMessage("   {0} : {1} ({2}, {3}) OID {4} is {5}. Updated to {6}\n".format
                                                 (in_data, field.name, reqd_val, gentype_val, row[2], current_val,
                                                  new_val))
                                row[1] = new_val

                            # Required fields changes are version-agnostic;
                            if gentype_val == 'Text':

                                # special case to warn user if null and to not update
                                if in_data == "S_Fld_Haz_Ar" and field.name == "FLD_ZONE":
                                    if row[1] in [None, "NP"]:
                                        arcpy.AddWarning("   {0} : {1}, OID {2} is Null or NP\n".format(in_data,
                                                                                                        field.name,
                                                                                                        row[2]
                                                                                                        ))
                                        invalid_id_list.append((in_data, field.name))

                                else:
                                    if row[1] in ['', ' ', "-9999", "-8888", None]:
                                        update_val = "NP"
                                        update_required(update_val)

                            elif row[1] in [-9999, None] and gentype_val == 'Numeric':

                                update_val = -8888
                                update_required(update_val)

                            elif gentype_val == 'Date':

                                if row[1] is None or (
                                                    row[1].year == 9999 and row[1].month == 9 and row[1].day == 9):
                                    update_val = "8/8/8888"
                                    update_required(update_val)

                            elif gentype_val == "TF" and row[1] in [None, '']:

                                update_val = "U"
                                update_required(update_val)

                        # For applicable fields, check version number
                        else:
                            # check version
                            version_id = row[0]
                            # get the third digit of the version ID
                            if version_id:
                                version_id_index = version_id[2]

                                #  update applicable fields
                                def update_applicable(new_val):

                                    # update row[1] with param input
                                    row[1] = new_val
                                    # change new_val format for user message
                                    if new_val == '':
                                        new_val = "''"

                                    arcpy.AddMessage(
                                        "   {0} : {1} ({2}, {3}, {4}) OID {5} is {6}. Updated to {7}\n".format
                                        (in_data, field.name, version_id, reqd_val, gentype_val, row[2],
                                         current_val,
                                         new_val))
                                # For applicable version n.1.n.n
                                if version_id_index == '1':

                                    if gentype_val == "Text" and row[1] in ["NP", "-9999", "-8888", "U", None, ' ']:
                                        update_val = ''
                                        update_applicable(update_val)

                                    elif gentype_val == "Numeric" and row[1] in [-8888, None]:
                                        update_val = -9999
                                        update_applicable(update_val)

                                    elif gentype_val == "Date":
                                        update_val = "9/9/9999"
                                        if row[1] is None or (row[1].year == 8888 and row[1].month == 8 and row[
                                                                1].day == 8):
                                            update_applicable(update_val)

                                    elif gentype_val == "TF" and row[1] in ["U", None]:
                                        update_val = ''
                                        update_applicable(update_val)

                                # Applicable and non-version-n.1.n.n
                                else:

                                    if gentype_val == "Text":

                                        if row[1] in ['-9999', None, ' ']:
                                            # define update value
                                            update_val = ''
                                            update_applicable(update_val)

                                        elif row[1] in ['-8888', 'U']:
                                            update_val = 'NP'
                                            update_applicable(update_val)

                                    elif gentype_val == "Numeric" and row[1] is None:
                                        update_val = -9999
                                        update_applicable(update_val)

                                    elif gentype_val == "Date" and row[1] is None:
                                        update_val = '9/9/9999'
                                        update_applicable(update_val)

                                    elif gentype_val == "TF" and row[1] is None:
                                        update_val = ''
                                        update_applicable(update_val)

                        # Apply update
                        u_cursor.updateRow(row)

    else:
        arcpy.AddMessage("{0} has no features...\n".format(in_data))


def main():
    # perform update null on feature data sets
    for fds in arcpy.ListDatasets('', 'feature') + ['']:
        for featureclass in arcpy.ListFeatureClasses('', '', fds):
            update_null(featureclass)

    # perform update null on feature classes
    for fc in arcpy.ListFeatureClasses():
        update_null(fc)

    # perform update null on tables
    for tb in arcpy.ListTables():
        update_null(tb)


# Create output csv if there are any invalid values
def create_log():
    if invalid_id_list:
        import csv
        import time
        time_str = time.strftime("%Y%m%d_%H%M%S")
        out_csv = project_dir + "\\" + "INVALID_VAL_" + time_str + ".csv"
        csv_list = []
        # Get unique set from the list
        invalid_id_set = set(invalid_id_list)
        for item in invalid_id_set:
            # Get count of the set from the list
            count = invalid_id_list.count(item)
            # Add values to new list
            csv_list.append((str(item[0]), str(item[1]), str(count)))

        # Write list values to csv
        csv_list.sort()
        # Add work space information and header to list
        csv_list.insert(0, (myWorkspace, "", ""))
        csv_list.insert(1, ("Table", "Field", "Count of Invalid Values"))
        with open(out_csv, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(csv_list)
        arcpy.AddMessage("Summary of invalid values at {0}\n".format(out_csv))
        # Uncomment this to open output csv in system default application
        # os.system(out_csv)
try:
    if __name__ == '__main__':
        #  build firm db dictionary
        build_firm_db_dict()

        # start an edit session to update data set
        edit = arcpy.da.Editor(myWorkspace)
        edit.startEditing(False, True)
        edit.startOperation()
        main()
        edit.stopOperation()
        edit.stopEditing(True)

        create_log()

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))

