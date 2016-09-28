import serial
import sys

LISTENING_PORT = "COM2"

def main():
    """Simulates a Grid+ V2 unit, by listening on a serial port for incoming data
    and sending appropriate responses.

    The simulator is used to the the "Grid Control" application.

    Example:
    One byte "C0" received (initialize grid), respond with "21" (grid initialized)

    Note that two virtual serial ports (connected to each other) must be defined using e.g.
    "Free Virtual Serial Ports" from https://freevirtualserialports.com/

    Configure "Grid Control" to use e.g. "COM1" and the simulator to use "COM2".

    Note: If you are using PyCharm, don't start the simulator with "Run" in the IDE,
    instead run it from the terminal. If not, the process could be stuck and needs to be killed in task manager.

    Press CTRL+C to exit the application.
    """

    # Configure serial port
    ser = serial.Serial()
    ser.baudrate = 4800
    ser.port = LISTENING_PORT  # Created by "Free Virtual Serial Ports" application
    ser.bytesize = serial.EIGHTBITS
    ser.stopbits = serial.STOPBITS_ONE
    ser.parity = serial.PARITY_NONE
    ser.timeout = None  # Read timeout in seconds
    ser.write_timeout = 2  # Write timeout in seconds

    ser.open()
    ser.flushOutput()
    ser.flushInput()

    print("Grid simulator started, listening on port " + LISTENING_PORT)

    try:
        while True:
            # Listen for incoming data
            waiting = ser.in_waiting
            data = []

            # If data is received
            if waiting > 0:
                # Read the bytes waiting in the buffer
                bytes = ser.read(waiting)

                # Print the waiting bytes
                for i, b in enumerate(bytes):
                    data.append(str(hex(b)))
                print("\nWaiting bytes " + str(waiting) + " " + str(data))

                # If one byte C0 received -> initialize Grid
                if waiting == 1:
                    if bytes[0] == int("0xc0", 16):
                        print("C0 received, initialize Grid")
                        print("Sending 0x21...")
                        ser.write(serial.to_bytes([0x21]))
                    else:
                        print("One byte received, unsupported data")

                # If two bytes received -> read fan rpm or voltage
                elif waiting == 2:
                    # If first byte is 8A -> read rpm, fan id is second byte
                    if bytes[0] == int("0x8a", 16):
                        print("Read rpm for fan " + str(bytes[1]) + " received")
                        # Respond with "dummy value" 260 rpm (1 * 256 (high byte) + 4 (low byte))
                        ser.write(serial.to_bytes([0xC0, 0x00, 0x00, 0x01, 0x04]))

                    # If first byte is 84 -> read voltage, fan id is second byte
                    elif bytes[0] == int("0x84", 16):
                        print("Read voltage for fan " + str(bytes[1]) + " received")
                        # Respond with "dummy value" 5.5V
                        ser.write(serial.to_bytes([0xC0, 0x00, 0x00, 0x05, 0x05]))
                    else:
                        print("Two bytes received, unsupported data")

                # If seven bytes received -> set fan voltage, fan id is second byte
                elif waiting == 7:
                    print("Set voltage for fan " + str(bytes[1]) + " received")
                    # Reply with 01 (success)
                    ser.write(serial.to_bytes([0x01]))
                else:
                    print("Unsupported number of bytes received")

    # Quit the running while loop by pressing CTRL+C
    except KeyboardInterrupt:
        print("Keyboard interrupt, exiting")
        sys.exit(0)


if __name__ == "__main__":
    main()


