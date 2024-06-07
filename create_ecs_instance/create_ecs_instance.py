from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest
from aliyunsdkecs.request.v20140526.AttachNetworkInterfaceRequest import (
    AttachNetworkInterfaceRequest,
)
from aliyunsdkecs.request.v20140526.CreateNetworkInterfaceRequest import (
    CreateNetworkInterfaceRequest,
)
from aliyunsdkvpc.request.v20160428.AllocateEipAddressRequest import (
    AllocateEipAddressRequest,
)
from aliyunsdkvpc.request.v20160428.AssociateEipAddressRequest import (
    AssociateEipAddressRequest,
)
from aliyunsdkecs.request.v20140526.StartInstanceRequest import StartInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import (
    DescribeInstancesRequest,
)

import base64
import json
import time

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize the AcsClient
client = AcsClient(
    config["access_key_id"], config["access_key_secret"], config["region_id"]
)

# Use config for other IDs
security_group_id = config["security_group_id"]
v_switch_id = config["vswitch_id"]
vpc_id = config["vpc_id"]


def create_ecs_instance():
    """
    Creates an ECS instance with specified configurations.

    Returns:
        str: The ID of the created ECS instance.

    Raises:
        Exception: If there is an error in creating the ECS instance.
    """
    try:
        request = CreateInstanceRequest()
        request.set_InstanceName("MyECSInstance")
        request.set_ImageId(
            "ubuntu_22_04_x64_20G_alibase_20240508.vhd"
        )
        request.set_InstanceType("ecs.t5-lc1m2.large")
        request.set_SecurityGroupId(security_group_id)
        request.set_VSwitchId(v_switch_id)
        request.set_SystemDiskCategory(
            "cloud_efficiency"
        )
        request.set_SystemDiskSize(40)

        data_disks = [
            {
                "Size": 40,
                "Category": "cloud_efficiency",
                "DeleteWithInstance": True,
                "Device": "/dev/vdb",
            }
        ]
        request.set_DataDisks(data_disks)

        request.set_InternetChargeType("PayByTraffic")
        request.set_InternetMaxBandwidthOut(10)
        request.set_InternetMaxBandwidthIn(10)

        user_data_script = """#!/bin/bash
        apt-get update -y
        apt-get upgrade -y
        apt-get install -y docker.io
        systemctl start docker
        systemctl enable docker
        """

        encoded_user_data = base64.b64encode(user_data_script.encode('utf-8')).decode('utf-8')
        request.set_UserData(encoded_user_data)

        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Create ECS Instance Response:", response_dict)
        instance_id = response_dict["InstanceId"]
        return instance_id
    except Exception as e:
        print(f"Error creating ECS instance: {e}")
        raise


def allocate_eip():
    """
    Allocates a new Elastic IP (EIP) address.

    Returns:
        tuple: A tuple containing the allocation ID and the allocated EIP address.

    Raises:
        Exception: If there is an error in allocating the EIP.
    """
    try:
        request = AllocateEipAddressRequest()
        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Allocate EIP Response:", response_dict)
        return response_dict["AllocationId"], response_dict["EipAddress"]
    except Exception as e:
        print(f"Error allocating EIP: {e}")
        raise


def create_network_interface(vpc_id, v_switch_id, security_group_id):
    """
    Creates a new network interface in the specified VPC and VSwitch, and associates it with a security group.

    Args:
        vpc_id (str): The ID of the VPC.
        v_switch_id (str): The ID of the VSwitch.
        security_group_id (str): The ID of the security group.

    Returns:
        str: The ID of the newly created network interface.

    Raises:
        Exception: If there is an error in creating the network interface.
    """
    try:
        request = CreateNetworkInterfaceRequest()
        request.set_VSwitchId(v_switch_id)
        request.set_SecurityGroupId(security_group_id)
        request.set_NetworkInterfaceName("MyNetworkInterface")
        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Create Network Interface Response:", response_dict)
        return response_dict["NetworkInterfaceId"]
    except Exception as e:
        print(
            f"Error creating network interface in VPC {vpc_id}, VSwitch {v_switch_id}: {e}"
        )
        raise


def attach_network_interface(instance_id, network_interface_id):
    """
    Attaches a secondary network interface to a specified ECS instance.

    Args:
        instance_id (str): The ID of the ECS instance.
        network_interface_id (str): The ID of the network interface to attach.

    Returns:
        dict: The response dictionary from the API call.

    Raises:
        Exception: If there is an error in attaching the network interface.
    """
    try:
        request = AttachNetworkInterfaceRequest()
        request.set_InstanceId(instance_id)
        request.set_NetworkInterfaceId(network_interface_id)
        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Attach Network Interface Response:", response_dict)
        return response_dict
    except Exception as e:
        print(
            f"Error attaching network interface {network_interface_id} to instance {instance_id}: {e}"
        )
        raise


def associate_eip_with_instance(allocation_id, instance_id):
    """
    Associates an Elastic IP (EIP) address with a specified ECS instance.

    Args:
        allocation_id (str): The allocation ID of the EIP.
        instance_id (str): The ID of the ECS instance to associate with the EIP.

    Returns:
        str: The EIP address associated with the ECS instance.

    Raises:
        Exception: If there is an error in associating the EIP with the ECS instance.
    """
    try:
        request = AssociateEipAddressRequest()
        request.set_AllocationId(allocation_id)
        request.set_InstanceId(instance_id)
        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Associate EIP with Instance Response:", response_dict)
        return response_dict.get("EipAddress", "No EipAddress found in response")
    except Exception as e:
        print(f"Error associating EIP {allocation_id} with instance {instance_id}: {e}")
        raise


def associate_eip_with_network_interface(allocation_id, network_interface_id):
    """
    Associates an Elastic IP (EIP) address with a specified network interface.

    Args:
        allocation_id (str): The allocation ID of the EIP.
        network_interface_id (str): The ID of the network interface to associate with the EIP.

    Returns:
        str: The EIP address associated with the network interface.

    Raises:
        Exception: If there is an error in associating the EIP with the network interface.
    """
    try:
        request = AssociateEipAddressRequest()
        request.set_AllocationId(allocation_id)
        request.set_InstanceType("NetworkInterface")
        request.set_InstanceId(network_interface_id)
        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Associate EIP with Network Interface Response:", response_dict)
        return response_dict.get("EipAddress", "No EipAddress found in response")
    except Exception as e:
        print(
            f"Error associating EIP {allocation_id} with network interface {network_interface_id}: {e}"
        )
        raise


def start_instance(instance_id):
    """
    Starts the specified ECS instance.

    Args:
        instance_id (str): The ID of the ECS instance to be started.

    Returns:
        dict: The response from the start instance request.

    Raises:
        Exception: If there is an error in starting the instance.
    """
    try:
        request = StartInstanceRequest()
        request.set_InstanceId(instance_id)
        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Start Instance Response:", response_dict)
        return response_dict
    except Exception as e:
        print(f"Error starting instance {instance_id}: {e}")
        raise


def get_instance_status(instance_id):
    """
    Retrieves the current status of an ECS instance.

    Args:
        instance_id (str): The ID of the ECS instance.

    Returns:
        str: The current status of the instance (e.g., 'Running', 'Stopped').

    Raises:
        Exception: If there is an error in retrieving the instance status.
    """
    try:
        request = DescribeInstancesRequest()
        request.set_InstanceIds(json.dumps([instance_id]))
        response = client.do_action_with_exception(request)
        response_dict = json.loads(response)
        print("Instance Status Response:", response_dict)
        status = response_dict["Instances"]["Instance"][0]["Status"]
        return status
    except Exception as e:
        print(f"Error retrieving instance status for {instance_id}: {e}")
        raise


def wait_for_instance_status(instance_id, desired_status, timeout=600, interval=10):
    """
    Waits for an ECS instance to reach a desired status within a specified timeout period.

    Args:
        instance_id (str): The ID of the ECS instance.
        desired_status (str): The desired status to wait for (e.g., 'Running', 'Stopped').
        timeout (int, optional): The maximum time (in seconds) to wait for the instance to reach the desired status. Defaults to 600 seconds.
        interval (int, optional): The time interval (in seconds) between status checks. Defaults to 10 seconds.

    Returns:
        bool: True if the instance reaches the desired status within the timeout period, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            status = get_instance_status(instance_id)
        except Exception as e:
            print(f"Error getting instance status: {e}")
            time.sleep(interval)
            continue

        if status == desired_status:
            print(f"Instance {instance_id} reached desired status: {desired_status}")
            return True
        print(
            f"Current status: {status}. Waiting for instance to be in '{desired_status}' state..."
        )
        time.sleep(interval)

    print(
        f"Timeout reached. Instance {instance_id} did not reach desired status: {desired_status}"
    )
    return False


# Main Execution Flow

# Step 1: Create ECS instance
instance_id = create_ecs_instance()
print("Instance Created:", instance_id)

# Step 2: Wait for the instance to be in 'Stopped' state before making further changes
if not wait_for_instance_status(instance_id, "Stopped"):
    raise Exception("Instance did not reach 'Stopped' state in time")

# Step 3: Allocate the primary EIP while the instance is stopped
primary_eip_allocation_id, primary_eip = allocate_eip()
print("Primary EIP Allocated:", primary_eip)

# Step 4: Create and attach the secondary network interface while the instance is stopped
secondary_network_interface_id = create_network_interface(
    vpc_id=vpc_id, v_switch_id=v_switch_id, security_group_id=security_group_id
)
print("Secondary Network Interface Created:", secondary_network_interface_id)

# Attach the secondary network interface to the ECS instance
attach_network_interface(instance_id, secondary_network_interface_id)
print("Secondary Network Interface Attached to ECS Instance")

# Step 5: Allocate the secondary EIP while the instance is stopped
secondary_eip_allocation_id, secondary_eip = allocate_eip()
print("Secondary EIP Allocated:", secondary_eip)

# Step 6: Start the instance and wait for it to be in 'Running' state
start_instance(instance_id)
if not wait_for_instance_status(instance_id, "Running"):
    raise Exception("Instance did not reach 'Running' state in time")
print("Instance is now running. Proceeding with EIP association...")

# Step 7: Associate the primary EIP with the primary network interface (instance)
associate_eip_with_instance(primary_eip_allocation_id, instance_id)
print("Primary EIP Associated with Instance")

# Step 8: Associate the secondary EIP with the secondary network interface
associate_eip_with_network_interface(
    secondary_eip_allocation_id, secondary_network_interface_id
)
print("Secondary EIP Associated with Secondary Network Interface")
