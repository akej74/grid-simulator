# Grid Simulator
Simulates a Grid+ V2 device, used for testing the "Grid Control" application.

## Virtual serial ports
To be able to connect the simulator to the Grid Control application, you need to install a virtual serial port bridge. A nice free tool for this is [Free Virtual Serial Ports](https://freevirtualserialports.com/).

In Free Virtual Serial POrts, add a serial port bridge. This will add two new virtual serial ports (can be viewed in Device Manager in Windows), usually "COM1" and "COM2. 

Connect Grid Control to "COM1" and the simulator to "COM2". The two applications can now talk to each other.
