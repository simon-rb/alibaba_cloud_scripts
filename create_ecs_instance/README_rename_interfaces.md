### Rename eth0 and eth1 Without Getting Disconnected (ECS Instance)

This README explains how to run the `rename_interfaces.sh` script to rename network interfaces on an Alibaba Cloud ECS instance. You run it directly from your ECS instance.

#### Steps to Run the Script:

1. **Prepare the Script on Your ECS Instance**:
   - Create the script by opening a text editor and copying the content of the script into a new file. Use the following command to open a text editor:
     ```bash
     sudo nano /root/rename_interfaces.sh
     ```
   - Copy and paste the content of the script into the editor, save the file, and exit the editor.

2. **Make the Script Executable**:
   Ensure the script is executable by setting the appropriate permissions:
   ```bash
   sudo chmod +x /root/rename_interfaces.sh
   ```

3. **Run the Script**:
   Execute the script with administrative privileges to ensure it can modify network interface settings:
   ```bash
   sudo /root/rename_interfaces.sh
   ```

4. **Verify the Changes**:
   After running the script, verify that the network interfaces have been renamed successfully:
   ```bash
   ip addr show
   ```
   This command will display all network interfaces. Check to ensure `eth0` and `eth1` have been renamed to `output` and `input1` respectively.

By following these steps, you can rename the network interfaces on your ECS instance using the `rename_interfaces.sh` script.