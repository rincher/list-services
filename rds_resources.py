def fetch_and_format_rds_data(client):
    instance_response = client.describe_db_instances()
    db_data_set = []
    db_instances = instance_response.get("DBInstances", "")
    for db_instance in db_instances:
        db_data = {}
        db_type = db_instance.get("DBInstanceClass", "")
        db_engine = db_instance.get("Engine", "")
        db_engine_version = db_instance.get("EngineVersion", "")
        db_multiaz = db_instance.get("MultiAZ", "")
        db_az = db_instance.get("AvailabilityZone", "")
        db_status = db_instance.get("DBInstanceStatus", "")
        db_storage_type = db_instance.get("StorageType", "")
        db_storage = db_instance.get("AllocatedStorage", "")
        db_maintenance = db_instance.get("PreferredMaintenanceWindow", "")
        db_instance_pg = db_instance.get("DBParameterGroups")[0].get(
            "DBParameterGroupName"
        )
        db_subnet_group = db_instance.get("DBSubnetGroup").get("DBSubnetGroupName")
        db_vpc = db_instance.get("DBSubnetGroup").get("VpcId")
        db_option_group = db_instance.get("OptionGroupMemberships")[0].get(
            "OptionGroupName"
        )
        db_instance_id = db_instance.get("DBInstanceIdentifier", "")
        db_cluster_id = db_instance.get("DBClusterIdentifier", "")
        if db_cluster_id != "":
            cluster_response = client.describe_db_clusters(
                DBClusterIdentifier=db_cluster_id
            )
            for db_clusters in cluster_response.get("DBClusters"):
                db_data["DBClusterPG"] = db_clusters.get("DBClusterParameterGroup")

        db_data["Size"] = db_type
        db_data["Engine"] = db_engine
        db_data["EngineVersion"] = db_engine_version
        db_data["MultiAZ"] = db_multiaz
        db_data["Region"] = db_az
        db_data["Status"] = db_status
        db_data["StorageType"] = db_storage_type
        db_data["Storage"] = db_storage
        db_data["MaintenanceEnable"] = db_maintenance
        db_data["DBInstancePG"] = db_instance_pg
        db_data["VPC"] = db_vpc
        db_data["DBSubnetGroup"] = db_subnet_group
        db_data["OptionGroup"] = db_option_group
        db_data["DBClusterIdentifer"] = db_cluster_id
        db_data["DBInstanceIdentifier"] = db_instance_id

        db_data_set.append(db_data)
    return db_data_set
