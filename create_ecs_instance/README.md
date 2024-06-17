### Deploy an ECS Instance with 2 EIPs and 2 ENIs Using the Alibaba Cloud SDK

This guide outlines setting up an ECS instance on Alibaba Cloud with two Elastic IP addresses (EIPs) and two Elastic Network Interfaces (ENIs). The Alibaba Cloud SDK automates the creation and setup of these resources, and a Docker image hosted in Alibaba Cloud Container Registry (ACR) will be deployed on the ECS instance.

### Prerequisites

Ensure the following prerequisites are met to successfully deploy and manage the ECS instance:

1. **Alibaba Cloud Account**:
   - You need access to an Alibaba Cloud account with permissions to create and manage ECS, VPC, and ACR resources.

2. **SDK Installation on Local Machine**:
   - Install the Alibaba Cloud Python SDK to programmatically manage Alibaba Cloud services:
     ```sh
     pip install aliyun-python-sdk-core
     pip install aliyun-python-sdk-ecs
     pip install aliyun-python-sdk-vpc
     ```

3. **Access Keys**:
   - Obtain an Access Key ID and Secret from the Alibaba Cloud Management Console for SDK authentication.

4. **Container Registry Setup**:
   - Log into the Alibaba Cloud Console, navigate to the **Container Registry** service, and set up a personal Container Registry instance.
   - Create a repository within your ACR, noting down the repository name, namespace, and a created password for access.

5. **Docker Installation**:
   - Docker must be installed on both your local machine and the ECS instance to manage and deploy images. The installation on the ECS instance is handled automatically.

6. **Python Environment**:
   - Ensure Python is installed and configured on your local machine for running deployment scripts.

Complete these prerequisites before initiating the ECS setup to ensure a smooth deployment process using the Alibaba Cloud SDK.


### Step 1: Running the Script (Local Machine)

This step involves using a script from the GitHub repository to automate the deployment of an ECS instance configured with 2 EIPs and 2 ENIs. Follow these streamlined instructions:

1. **Set Up `config.json`**:
   - Ensure the `config.json` file, located in the same directory as `create_ecs_instance.py`, is correctly configured with your Alibaba Cloud credentials and resource identifiers. It should include keys for `access_key_id`, `access_key_secret`, `region_id`, `vpc_id`, `security_group_id`, and `vswitch_id`.

2. **Ensure Script Availability**:
   - Verify that `create_ecs_instance.py` is in the same folder as `config.json`. Both files should be pulled from the existing GitHub repository.

3. **Execute the Script**:
   - Run the script via your command line to initiate the ECS setup:
     ```sh
     python create_ecs_instance.py
     ```

4. **Monitor Progress**:
   - Observe the script's output as it progresses through creating the ECS instance, attaching ENIs, allocating EIPs, and associating the EIPs with the instance.

This procedure sets up the ECS instance with two network interfaces, ensuring EIP_1 is attached to ENI_1, and EIP_2 is attached to ENI_2. Each step is critical for the successful deployment of the configured resources.

### Step 2: Push the Docker Image to ACR (Local Machine)

This step involves pushing a Docker image from your local machine to Alibaba Cloud Container Registry (ACR), ensuring it's available for deployment on your ECS instance.

1. **Log in to ACR**:
   - Use the Docker CLI to authenticate to your ACR instance:
     ```sh
     docker login --username=your-username@your-alibaba-cloud-id registry-intl.eu-central-1.aliyuncs.com
     ```
   - Replace `your-username@your-alibaba-cloud-id` with your actual Alibaba Cloud username, and adjust the registry endpoint accordingly.

2. **Push the Docker Image**:
   - Push your Docker image to ACR. This could be a POC-specific image or any other required image:
     ```sh
     docker push registry-intl.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest
     ```

### Step 3: Pull and Run the Docker Image on ECS (ECS Instance)

This step details pulling the Docker image from ACR to an ECS instance and running it with appropriate configurations.

1. **Log in to ECS Instance**:
   - Access your ECS instance, e.g., via Alibaba Cloud console's Terminal Connect feature.

2. **Ensure Docker Is Installed**:
   - Confirm Docker is installed on the ECS instance, typically handled by a user data script during instance setup.

3. **Authenticate to ACR on ECS**:
   - Log in to your ACR from the ECS instance to access the Docker image:
     ```sh
     sudo docker login --username=your-username@your-alibaba-cloud-id registry-intl-vpc.eu-central-1.aliyuncs.com
     ```

4. **Pull the Docker Image**:
   - Retrieve the Docker image from ACR to your ECS instance:
     ```sh
     sudo docker pull registry-intl-vpc.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest
     ```

5. **Run the Docker Image**:
   - Depending on your specific needs, select the appropriate Docker command:
     - **For POC or full configurations**:
       ```sh
       sudo docker run --network host --tmpfs /tmp --tmpfs /run --tmpfs /mnt -v redis_vol:/var/lib/redis -v etc_vol:/etc --privileged --rm -it registry-intl-vpc.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest /bin/bash
       ```
       Here, the `--network host` flag allows the container to share the host's networking namespace, `--tmpfs` creates temporary file storage in RAM, and `-v` binds volumes for persistent data storage. The `--privileged` flag gives the container extended permissions, which might be necessary for certain applications or tests.

     - **For basic testing with a simpler setup** (e.g., using the `nginx:latest` image):
       ```sh
       sudo docker run -it --rm nginx:latest
       ```


### Step 5: Verify the Setup (ECS Instance, Local Machine)

Confirm that your Docker containers are operating as expected:

1. **Check Docker Container Status (ECS Instance)**:
    - Use `sudo docker ps` to view active containers. Look for your container's ID, image, status, and port mappings to confirm it's running correctly.

2. **Access the Running Containers**:
   - **Nginx Setup**:
     - Access the Nginx server using the public static IPv4 addresses (EIPs) of your ECS instance. Navigate to:
       ```
       http://<Primary_EIP>
       http://<Secondary_EIP>
       ```
     - You should see the Nginx welcome page, confirming the server is accessible.

   - **POC Docker Image**:
     - The UI for the POC Docker image may be restricted to client-specific access.
