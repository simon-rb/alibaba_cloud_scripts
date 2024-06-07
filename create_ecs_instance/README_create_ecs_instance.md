### Script (create_ecs_instance.py) Overview

This script automates the creation and configuration of an Elastic Compute Service (ECS) instance on Alibaba Cloud, along with the allocation and association of Elastic IPs (EIPs) and network interfaces (ENIs). 
It uses the Alibaba Cloud SDK to perform these tasks programmatically. Here's a breakdown of the main components and their purpose:

1. **Initialize the AcsClient**: 
   - `AcsClient` is initialized using access credentials and region information stored in a `config.json` file. This client is used to interact with the Alibaba Cloud API.

2. **Function Definitions**:
   - `create_ecs_instance()`: Creates an ECS instance with configurations such as instance type, image ID, and system and data disks.
   - `allocate_eip()`: Allocates a new Elastic IP (EIP) address.
   - `create_network_interface(vpc_id, v_switch_id, security_group_id)`: Creates a new network interface in the specified VPC and VSwitch and associates it with a security group.
   - `attach_network_interface(instance_id, network_interface_id)`: Attaches a secondary network interface to a specified ECS instance.
   - `associate_eip_with_instance(allocation_id, instance_id)`: Associates an Elastic IP (EIP) address with a specified ECS instance.
   - `associate_eip_with_network_interface(allocation_id, network_interface_id)`: Associates an Elastic IP (EIP) address with a specified network interface.
   - `start_instance(instance_id)`: Starts the specified ECS instance.
   - `get_instance_status(instance_id)`: Retrieves the current status of an ECS instance.
   - `wait_for_instance_status(instance_id, desired_status, timeout=600, interval=10)`: Waits for an ECS instance to reach a desired status within a specified timeout period.

3. **Main Execution Flow**:
   - **Step 1**: Create the ECS instance and retrieve its ID.
   - **Step 2**: Wait for the instance to be in a 'Stopped' state before making further changes.
   - **Step 3**: Allocate the primary EIP while the instance is stopped.
   - **Step 4**: Create and attach a secondary network interface while the instance is stopped.
   - **Step 5**: Allocate the secondary EIP while the instance is stopped.
   - **Step 6**: Start the instance and wait for it to be in a 'Running' state.
   - **Step 7**: Associate the primary EIP with the primary network interface (instance).
   - **Step 8**: Associate the secondary EIP with the secondary network interface.

This script ensures that you have an ECS instance configured with 2 EIPs and 2 ENIs, enabling you to run Docker containers and bind them to specific EIPs for distinct network traffic routing.
