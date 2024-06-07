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

   # Rename the interfaces
   ip link set eth0 name input
   ip link set eth1 name output

   # Bring up the renamed interfaces
   ip link set input up
   ip link set output up
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
   ip link set input down
   ip link set output down

   # Rename the interfaces back to their original names
   ip link set input name eth0
   ip link set output name eth1

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
