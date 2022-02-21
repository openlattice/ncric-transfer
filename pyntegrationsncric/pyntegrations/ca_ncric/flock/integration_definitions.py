from pyntegrationsncric.pyntegrations.ca_ncric.utils.integration_base_classes import Integration
from pkg_resources import resource_filename
import pandas as pd

# Defaults to yesterday, midnight to today's midnight.
# Defaults to NCRIC org, but other org can be specified (e.g. legacy flock db)
# If current time is Monday anytime, this will choose Sunday midnight to Tuesday midnight (Mon evening)
# naming columns to avoid image columns
class FLOCKIntegration(Integration):
    def __init__(self, sql=None, flight_path=None,
                 clean_table_name_suffix='',
                 org_id = '47b646d7-a01a-4232-b25b-15c880ea4046',
                 base_url="https://api.openlattice.com"):
        if sql is None:
            sql = """select f."readid",f."timestamp", f."type", f."plate", f."confidence",
            f."latitude", f."longitude", f."cameraid", f."cameraname", f."platestate", f."speed",
            f."direction", f."model", f."hotlistid", f."hotlistname", f."cameralocationlat",
            f."cameralocationlon", f."cameranetworkid", f."cameranetworkname", s."standardized_agency_name" from flock_reads f left join standardized_agency_names_flock s
            on cast(f.cameranetworkid AS TEXT) = s."ol.id"
            where \"timestamp\" between current_date - interval '1 day' and current_date + interval '1 day';"""
            clean_table_name_root="clean_flock_recurring"
        else:
            clean_table_name_root="clean_flock" + "_" + clean_table_name_suffix

        if flight_path is None:
            flight_path = resource_filename(__name__, "ncric_flock_flight.yaml"),
       
        super().__init__(
            sql=sql,
            atlas_organization_id = org_id,
            clean_table_name_root = "_".join(filter(None,[clean_table_name_root, clean_table_name_suffix])),
            standardize_clean_table_name=True,
            if_exists="replace",
            flight_path=flight_path,
            base_url=base_url)

    def clean_row(cls, row):
        """
        Cleans row from the FLOCK dataset for integration.
        :param row: a row from the FLOCK data set
        :return: a cleaned row of data from the FLOCK data set
        """

        # Empty pd.Series for storing the cleaned row
        new_dict = pd.Series()

        # Reformat variables as needed
        new_dict['vehicle_record_id'] = f'{str(row.readid)}_FLOCK'
        new_dict['eventDateTime'] = row.timestamp
        new_dict['VehicleLicensePlateID'] = str(row.plate)
        if not pd.isnull(row.confidence):
            new_dict['confidence'] = row.confidence
            new_dict['conf_datasource'] = "FLOCK"
        new_dict['latlon'] = str(row.latitude) + ',' + str(row.longitude)
        new_dict['location_id'] = str(row.latitude) + '-' + str(row.longitude)
        new_dict['camera_id'] = str(row.cameraid)
        new_dict['LPRCameraName'] = row.cameraname
        new_dict['agency_id'] = str(row.cameranetworkid)
        new_dict['agencyName'] = row.cameranetworkname
        new_dict['standardized_agency_name'] = row.standardized_agency_name
        if not pd.isnull(row.model) and 'N/A' not in row.model:
            new_dict['model'] = row.model
        new_dict['datasource'] = 'FLOCK'

        # Creates IDs for entity associations.
        new_dict['has_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                             [row.plate, str(row.readid), "FLOCK"]))

        new_dict['recordedby1_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                     [str(row.readid), str(row.cameraid), str(row.timestamp), "FLOCK"]))
        new_dict['recordedby2_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                     [str(row.readid), str(row.cameranetworkid), str(row.timestamp), "FLOCK"]))
        new_dict['recordedby3_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                     [str(row.readid), str(row.standardized_agency_name), str(row.timestamp), "FLOCK"]))

        new_dict['includes1_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                   [str(row.readid), "FLOCK", str(row.confidence)]))
        new_dict['locatedat1_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                    [str(row.cameraid), str(row.latitude),
                                                     str(row.longitude), "FLOCK"]))
        new_dict['locatedat2_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                    [str(row.readid), str(row.latitude),
                                                     str(row.longitude), "FLOCK"]))
        new_dict['locatedat3_id'] = "_".join(filter(None, [row.plate, str(row.latitude),
                                                           str(row.longitude), "FLOCK"]))

        new_dict['collectedby_id'] = "_".join(filter(None, [str(row.cameraid), str(row.cameranetworkid), "FLOCK"]))
        new_dict['collectedby2_id'] = "_".join(filter(lambda x: x != "None" and x is not None, 
                                                [str(row.cameraid), str(row.standardized_agency_name), "FLOCK"]))

        return new_dict

    def add_new_agencies(cls, sql = """select distinct cameranetworkname, cameranetworkid, standardized_agency_name
        from flock_reads f left join standardized_agency_names_flock s
            on cast(f.cameranetworkid AS TEXT) = s.\"ol.id\""""):
        """
        Function to add new agencies every time Flock integration runs
        This probably won't be useful majority of the time, but we want to capture all "standardizations"
        This is only necessary for new integrations going forward (since we can assume that all the
        necessary standardization values are already existing for the fix)
        """

        cls.engine = cls.flight.get_atlas_engine_for_organization()
        data = pd.read_sql(sql, cls.engine)
        print(data)
        data = data[pd.isnull(data['standardized_agency_name'])][['cameranetworkname', 'cameranetworkid']]
        if len(data) > 0:
            data = data.rename({'cameranetworkid': 'ol.id', 'cameranetworkname': 'ol.name'})
            data['ol.datasource'] = "FLOCK"
            data['standardized_agency_name'] = data['ol.name']
            data.to_sql("standardized_agency_names_flock", cls.engine, if_exists = "append", index = False)
            print("Additional agencies successfully added")

        print("No new agencies to add!")

# Defaults to yesterday, midnight to midnight.
class FLOCKImageSourceIntegration(Integration):
    def __init__(self, sql=None, flight_file=None,
                 clean_table_name_suffix='',
                 base_url="https://api.openlattice.com"):
        if sql is None:
            sql = "select distinct \"cameraid\", \"cameraname\" from flock_reads where \"timestamp\" between current_date - interval '1 day' and current_date - interval '0 days';"
        if flight_file is None:
            flight_file = "flock_imagesources_flight.yaml"
        super().__init__(
            sql=sql,
            clean_table_name_root="zzz_clean_flock_imagessources" + clean_table_name_suffix,
            standardize_clean_table_name=False,
            if_exists="replace",
            flight_path=resource_filename(__name__, flight_file),
            base_url=base_url)

    def clean_row(cls, row):
        """
        Cleans row from the FLOCK dataset for integration of imagesources.
        :param row: a row from the FLOCK data set
        :return: a cleaned row of data corresponding to a imagesource from the FLOCK data set
        """

        new_dict = pd.Series()
        new_dict['camera_id'] = str(row.cameraid)
        new_dict['LPRCameraName'] = row.cameraname
        new_dict['datasource'] = "FLOCK"

        return new_dict

# Defaults to yesterday, midnight to midnight.
class FLOCKAgenciesIntegration(Integration):
    def __init__(self, sql=None, flight_file=None,
                 clean_table_name_suffix='',
                 base_url="https://api.openlattice.com"):
        if sql is None:
            sql = "select distinct \"cameranetworkid\", \"cameranetworkname\" from flock_reads where \"timestamp\" between current_date - interval '1 day' and current_date - interval '0 days';"
        if flight_file is None:
            flight_file = "flock_agencies_flight.yaml"
        super().__init__(
            sql=sql,
            clean_table_name_root="zzz_clean_flock_agencylist" + clean_table_name_suffix,
            standardize_clean_table_name=False,
            if_exists="replace",
            flight_path=resource_filename(__name__, flight_file),
            base_url=base_url)

    def clean_row(cls, row):
        """
        Cleans row from the FLOCK dataset for integration of agencies (cameranetworks).
        :param row: a row from the FLOCK data set
        :return: a cleaned row of data corresponding to a agencies (cameranetworks) from the FLOCK data set
        """

        new_dict = pd.Series()
        new_dict['agency_id'] = str(row.cameranetworkid)
        new_dict['agencyName'] = row.cameranetworkname
        new_dict['datasource'] = "FLOCK"

        return new_dict

class FLOCKImagesIntegration(Integration):
    def __init__(self, sql=None, flight_file=None,
                 clean_table_name_suffix='',
                 base_url="https://api.openlattice.com"):
        if sql is None:
            sql = "select \"readid\", \"image\" from flock_reads where \"timestamp\" between current_date - interval '1 day' and current_date - interval '0 days';"
        if flight_file is None:
            flight_file = "flock_images_flight.yaml"
        super().__init__(
            sql=sql,
            clean_table_name_root="zzz_clean_flock_images" + clean_table_name_suffix,
            standardize_clean_table_name=False,
            if_exists="replace",
            flight_path=resource_filename(__name__, flight_file),
            base_url=base_url)

    def clean_row(cls, row):

        new_dict = pd.Series()

        new_dict['vehicle_record_id'] = f'{str(row.readid)}_FLOCK'
        new_dict['LPRVehiclePlatePhoto'] = row.image

        return new_dict


# Daily hotlist left joined to same data as in the main flock integration (all but images)
# we only need to copy data that is already integrating into all the Flock entity sets,
# ...into 2 hotlist-specific entity sets (and no associations).
# This also integrates the standardized agency name instead of the original one (captured in other Flock entity sets)
class FlockHotlistIntegration(Integration):
    def __init__(self, sql='''select * from (select hot.*, "readid","timestamp","type", "confidence",
            "latitude", "longitude", "cameraid", "cameraname", "platestate", "speed",
             "direction", "model", "image", "hotlistid", "hotlistname", "cameralocationlat",
            "cameralocationlon", "cameranetworkid", "cameranetworkname", s."standardized_agency_name" from hotlist_daily hot
            inner join flock_reads f USING("plate")
            left join standardized_agency_names_flock s
            on cast(f.cameranetworkid AS TEXT) = s."ol.id"
            ) temp where "timestamp" between current_date - interval '1 day' and current_date + interval '1 day';''',
                 flight_file="flock_hotlist_flight.yaml",
                 clean_table_suffix='',
                 base_url="https://api.openlattice.com"):
        super().__init__(
            sql=sql,
            clean_table_name_root = "_".join(filter(None,["zzz_clean_flock_hotlist", clean_table_suffix])),
            standardize_clean_table_name=False,
            if_exists="replace",
            flight_path=resource_filename(__name__, flight_file),
            base_url=base_url)

    def clean_row(self, row):
        """
        Cleans row from the FLOCK dataset for integration.
        :param row: a row from the FLOCK data set
        :return: a cleaned row of data from the FLOCK data set
        """
        
        new_dict = pd.Series()
        
        new_dict['vehicle_record_id'] = f'{str(row.readid)}_FLOCK'
        new_dict['VehicleLicensePlateID'] = str(row.plate)
        new_dict['latlon'] = str(row.latitude) + ',' + str(row.longitude)
        new_dict['camera_id'] = str(row.cameraid)
        new_dict['eventDateTime'] = row.timestamp
        # new_dict['cameraname'] = row.cameraname
        # new_dict['platestate'] = row.platestate
        new_dict['agency_id'] = str(row.cameranetworkid)
        new_dict['agencyName'] = row.cameranetworkname
        new_dict['standardized_agency_name'] = row.standardized_agency_name
        new_dict['LPRVehiclePlatePhoto'] = row.image
        if not pd.isnull(row.model) and 'N/A' not in row.model:
            new_dict['model'] = row.model
        new_dict['datasource'] = 'FLOCK'

        return new_dict   
      
class FLOCKAgencyStandardizationFixIntegration(Integration):
    """
    This is primarily for data fixes
    general sql query should be:
    select readid, timestamp, cameranetworkname, standardized_agency_name cameraid from flock_reads f 
                    left join standardized_agency_names_flock s
                    on cast(f.cameranetworkid AS TEXT) = s."ol.id";
    """
    def __init__(self, sql,
                 flight_file="flock_agencies_standardized_fix.yaml",
                 base_url="https://api.openlattice.com"):
        super().__init__(
            sql = sql,
            clean_table_name_root="flock_agencies_standardized",
            standardize_clean_table_name=False,
            if_exists="replace",
            flight_path=resource_filename(__name__, flight_file),
            base_url=base_url)
          
    def clean_row(cls, row):
        """
        Cleans row from the FLOCK dataset for integration.
        :param row: a row from the FLOCK data set
        :return: a cleaned row of data from the FLOCK data set
        """
          
        # Empty pd.Series for storing the cleaned row
        new_dict = pd.Series()

        # Reformat variables as needed
        new_dict['vehicle_record_id'] = f'{str(row.readid)}_FLOCK'
        new_dict['eventDateTime'] = row.timestamp
        new_dict['standardized_agency_name'] = row.standardized_agency_name
        new_dict['cameraid'] = str(row.cameraid)
        new_dict['recordedby3_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                     [str(row.readid), str(row.standardized_agency_name), str(row.timestamp), "FLOCK"]))
        new_dict['collectedby2_id'] = "_".join(filter(lambda x: x != "None" and x is not None,
                                                     [str(row.cameraid), str(row.standardized_agency_name), "FLOCK"]))
        return new_dict


class FLOCKAgencyStandardizationIntegration(Integration):
    # sql is necessary here, but we don't actually clean any files...
    # just set integration.integrate_table(sql = "select * from standardized_agency_names_flock")
    def __init__(self, sql = "select * from standardized_agency_names_flock",
                 flight_file="flock_agencies_standardized.yaml",
                 base_url="https://api.openlattice.com"):
        super().__init__(
            sql = sql,
            clean_table_name_root="flock_agencies_standardized",
            standardize_clean_table_name=False,
            if_exists="replace",
            flight_path=resource_filename(__name__, flight_file),
            base_url=base_url)


