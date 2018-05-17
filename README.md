# IOX app - Serial to MQTT

This is a PaaS style application that runs on IOX. The purpose of this app is to transmit data from serial port (on the IR829) to a MQTT Topic. The app can also fetch data from a MQTT topic and push it to serial. The app also generates seperate log files for serial and MQTT communications.

## MQTT Parameters
Server: 173.39.91.122 (Local MQTT Broker hosted on EFM - running on mudit_vm. IP is assigned through DHCP and is subject to change)
### Topics
tqb/serial_data : Data received from the serial port is published to this topic.
tqb/recv_data : Data received on this topic is written to the serial port.

## Log Files
mqtt.log and serial.log

Note: Publishing log.reset (In any case e.g Log.Reset/LOG.RESET) on the topic tqb/recv_data resets (clears data) both the log files. 

## Building the app

In order to build the app, copy your code into a directory. Add a package.yaml file. Next, add a requirement.txt file for dependencies if required.
Next run the command `ioxclient package .`
A package.tar file will be created with your iox package.
Next you can either you IOX Local Manager on your router to upload the iox package or use the ioxclient CLI to upload and deploy the app.

## Note
1. The folder **concurrent_read_write** consists of the app which has the two-way communication functionality. The **serial_mqtt_iox_app** containes the app which merely reads from serial and publishes it to a MQTT topic.
2. Take note of the *requirements.txt* and *package.yaml files*. These are required for the ioxclient to create a iox package for the app. The requirements.txt contains the python dependencies required for the app to run eg. paho-mqtt , pyserial. These dependencies are automatically installed through pip while building the app. The package.yaml file containes certain parameters that are required by ioxclient.
3. The **KFX** directory contains code given to us by KFX Labs as a reference to run their demo. It contains codes (Specifically bus address) that are required to run the sensors, light and actuators.
4. The **serial_to_htpp** directory contains a modified version of the program that read from serial and publishes to mqtt (the program under **serial_mqtt_iox_app**). Instead of publishing the data received on serial to a MQTT server, we send a GET HTTP request to a cloud server maintained by Atoll systems which monitors sensor information. This program was used as a demo by Atoll systems during Cisco Launchpad 2018.

## Useful Links
1. ioxclient setup and app deployment through CLI : https://azetinetworks.atlassian.net/wiki/spaces/SC13/pages/90144794/Cisco+IR809+829+LXC+Container+Installation <br/>
2. Cisco Devnet Serial to MQTT app: https://github.com/CiscoDevNet/iox-app-serial-mqtt  <br/>
3. ioxclient Devnet doc (Also contains examples of Sample Docker, LXC and PaaS applications): https://developer.cisco.com/docs/iox/#!what-is-ioxclient/what-is-ioxclient  <br/>

