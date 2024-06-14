### Rename eth0 and eth1 Without Getting Disconnected (ECS Instance)

1. **Edit the Script**:
   ```bash
   sudo nano /root/rename_interfaces.sh
   ```

2. **Update the Content**:
   ```bash
   #!/bin/bash

   # Bring down both interfaces
   ip link set eth0 down
   ip link set eth1 down
   
   # Rename the interfaces using a temporary name
   ip link set eth0 name output
   ip link set eth1 name input1
   
   # Bring up the renamed interfaces
   ip link set output up
   ip link set input1 up
   ```

3. **Save and Make the Script Executable**:
   ```bash
   sudo chmod +x /root/rename_interfaces.sh
   ```

4. **Run the Script**:
   ```bash
   sudo /root/rename_interfaces.sh
   ```

5. **Verify the Renamed Interfaces**:
   ```bash
   ip addr show
   ```

### Reset to Standard Naming Convention (ECS Instance)

1. **Create a Reset Script**:
   ```bash
   sudo nano /root/reset_interfaces.sh
   ```

2. **Add the Content**:
   ```bash
   #!/bin/bash

   # Bring down both interfaces
   ip link set output down
   ip link set input1 down

   # Rename the interfaces back to their original names
   ip link set output name eth0
   ip link set input1 name eth1

   # Bring up the renamed interfaces
   ip link set eth0 up
   ip link set eth1 up
   ```

3. **Save and Make the Script Executable**:
   ```bash
   sudo chmod +x /root/reset_interfaces.sh
   ```

4. **Run the Script**:
   ```bash
   sudo /root/reset_interfaces.sh
   ```
