### Deploy an ECS Instance with 2 EIPs and 2 ENIs, and Run a Docker Image Using the SDK

### Prerequisites

1. **Alibaba Cloud Account**:
   - Ensure you have an Alibaba Cloud account with the necessary permissions to create and manage resources.

2. **SDK Installation on Local Machine**:
    - Install the Alibaba Cloud Python SDK:
        ```sh
        pip install aliyun-python-sdk-core
        pip install aliyun-python-sdk-ecs
        pip install aliyun-python-sdk-vpc
        ```

3. **Access Keys**:
    - Obtain your Access Key ID and Secret from the Alibaba Cloud console.

4. **Container Registry Setup**:
    - Go to the Alibaba Cloud Console.
    - Navigate to the **Container Registry** service.
    - Create a new personal Container Registry instance (no need for enterprise edition).
    - Create a new repository within your ACR instance. Note down the repository name, namespace and password.

5. **Docker**:
    - Ensure Docker is installed on your local machine and the ECS instance (done after logging in to ECS).

6. **Python Environment**:
   - Ensure Python is installed on your local machine.

Make sure all prerequisites are met before proceeding with the setup and deployment steps.

### Step 1: Running the Script (Local Machine)

1. **Create `config.json` on your local machine**:
   - Ensure the `config.json` file in the same directory as the script `create_ecs_instance.py` contains the necessary environment variables. Adjust the values to match your Alibaba Cloud account details:
     ```json
     {
       "access_key_id": "your-access-key-id",
       "access_key_secret": "your-access-key-secret",
       "region_id": "eu-central-1",
       "vpc_id": "your-vpc-id",
       "security_group_id": "your-security-group-id",
       "vswitch_id": "your-vswitch-id"
     }
     ```

2. **Download the Script**:
   - Save the Python script `create_ecs_instance.py` to your local machine and in the same folder as `config.json`.

3. **Run the Script**:
   - Execute the script in your terminal:
     ```sh
     python create_ecs_instance.py
     ```

4. **Monitor Output**:
   - The script will output the progress of each step, including creating the ECS instance, attaching ENIs, allocating EIPs, and associating the EIPs with the instance and ENIs.

This sequence ensures that your ECS instance is set up with two EIPs and network interfaces, where EIP_1 is attached to ENI_1 respectively eth0 and EIP_2 is attached to ENI_2 respectively eth1.


### Step 2: Pull the Docker Image Locally (Local Machine)

1. **Log in to Docker Hub**:
   - Open a terminal on your local machine.
   - Log in to Docker Hub:
     ```sh
     docker login
     ```
   - Provide your Docker Hub username and password when prompted.

2. **Pull the Docker Image from Docker Hub**:
   - Pull the desired Docker image (e.g., Nginx) to your local machine (e.g., linux/amd64):
     ```sh
     docker pull --platform linux/amd64 nginx:latest
     ```

3. **Tag the Docker Image for ACR**:
   - Tag the pulled image with your ACR repository details:
     ```sh
     docker tag nginx:latest registry-intl.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest
     ```

### Step 3: Push the Docker Image to ACR (from Local Machine)

1. **Log in to ACR from Your Local Machine**:
   - Log in to your ACR instance using the Docker CLI:
     ```sh
     docker login --username=your-username@your-alibaba-cloud-id registry-intl.eu-central-1.aliyuncs.com
     ```
   - Replace `your-username@your-alibaba-cloud-id` with your Alibaba Cloud account username and `registry-intl.eu-central-1.aliyuncs.com` with your ACR registry endpoint.

2. **Push the Docker Image to ACR**:
   - Push the tagged image to your ACR repository:
     ```sh
     docker push registry-intl.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest
     ```

### Step 4: Deploy the Docker Image on ECS (ECS Instance)

1. **Log in to ECS Instance**:
   - Log in to your ECS instance using the e.g., Alibaba Cloud console's Terminal Connect feature with temporary credentials.

2. **Install Docker on ECS**:
   - If Docker is not installed on your ECS instance, install it:
     ```sh
     sudo apt-get update
     sudo apt-get install -y docker.io
     sudo systemctl start docker
     ```

3. **Log in to ACR from ECS Instance**:
   - Log in to your ACR instance from the ECS instance using the Docker CLI (use password associated with pre-created ACR):
     ```sh
     sudo docker login --username=your-username@your-alibaba-cloud-id registry-intl.eu-central-1.aliyuncs.com
     ```

4. **Pull the Docker Image from ACR**:
   - Pull the Docker image from your ACR repository to the ECS instance:
     ```sh
     sudo docker pull registry-intl.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest
     ```

5. **Run the Docker Image on ECS**:
   - Run the pulled Docker image on the ECS instance:
     ```sh
     sudo docker run -d -p 80:80 --name mynginx registry-intl.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest
     ```

### Step 5: Verify the Setup (Local Machine)

- **Check Docker Container Status**:
    - Verify that the Docker container is running:
        ```sh
        sudo docker ps
        ```
    - You should see an output similar to this, indicating that the Nginx container is running:
        ```sh
        CONTAINER ID     IMAGE                                                                            COMMAND                  CREATED                STATUS                PORTS                               NAMES
        <container_id>   registry-intl.eu-central-1.aliyuncs.com/your-namespace/your-repository:latest    "nginx -g 'daemon of…"   <time_since_created>   Up <time_since_up>    0.0.0.0:80->80/tcp, :::80->80/tcp   mynginx
        ```
- **Access the Running Nginx Server**:
    - Use the public static IPv4 addresses (2 EIPs) associated with the ECS instance to access the running Nginx server (both are visible in the Alibaba Cloud console ECS section).
    - Open a web browser and navigate to the public IPv4 addresses:
        ```
        http://<Primary_EIP>
        http://<Secondary_EIP>
        ```
    - You should see the Nginx welcome page indicating that the Nginx server is running successfully for both EIPs.

This sequence ensures that you have the image correctly tagged and pushed to ACR, and then pulled and run on your ECS instance, with verification steps to confirm the setup is working correctly.
