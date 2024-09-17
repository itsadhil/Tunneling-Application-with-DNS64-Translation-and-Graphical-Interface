# Tunneling Application with DNS64 Translation and Graphical Interface

This project is a Python-based tunneling application that leverages DNS64 to translate IPv4 addresses into IPv6. It includes both client and server components, with a graphical interface (Tkinter) for sending and receiving packages, logging activities, and visualizing packet transfer progress in real-time.

## Features
- **DNS64 Translation**: Converts IPv4 addresses to IPv6 addresses.
- **Client-Server Communication**: The client sends packets, and the server translates and responds using DNS64.
- **Graphical Interface**: A Tkinter UI for packet sending/receiving and logging.
- **Real-Time Graphing**: Packet transfer progress is plotted dynamically using `matplotlib`.
- **Multithreading**: Both sending and receiving processes run on separate threads, ensuring the UI remains responsive.

## Dependencies
- Python 3.x
- `socket` (standard library)
- `ipaddress` (standard library)
- `tkinter` (standard library)
- `matplotlib`
- `threading` (standard library)

### Installing Dependencies
If you don't have `matplotlib` installed, you can install it using `pip`:

```bash
pip install matplotlib
```

# How to Use
**Running The Application**

1. Clone the repository or download the script.
2. Run the application: You can start the application by running the main Python file:
   ```bash
   python main.py
   ```
# Using the UI

1. Start the Application: Once the program starts, a Tkinter window will appear with options to start as either a sender (client) or receiver (server).

2. As Sender: Click on "Start as Sender" and enter the following:
   - Receiver IP: The IP address of the server (receiver).
   - Receiver Port: The port number on which the server is listening.
   - Packet Interval: Time (in seconds) between sending each packet.
   - Number of Packets: The total number of packets to send.

3. As Receiver: Click on "Start as Receiver" and enter:
   - Your IP: The server's IP (default is 0.0.0.0 to bind to all IPs).
   - Listening Port: The port number to listen on.

4. Graphing: The graph shows real-time progress of packet transmission or reception based on the packet count.

# Stopping The Sender

You can stop the sender mid-transmission by clicking "Stop Sending" in the sender window.

# Example Usage:

- Starting the Server (Receiver): Enter your IP and port, and click "Start Listening."
- Starting the Client (Sender): Provide the server IP and port, packet interval, and number of packets to send. Then click "Start Sending."

# Code Overview

**Classes**

- Package: A class representing a network package with data, source, and destination IPs
- DNS64: Implements DNS64 functionality, translating IPv4 addresses to IPv6 and vice versa.
- Client: A client that connects to the server and sends packages over the network. It uses DNS64 to handle address translation.
- Server: A server that listens for incoming packages, performs DNS64 translation, and responds to the client.
- TunnelUI: The Tkinter-based user interface for interacting with the application, including starting/stopping the client and server, and visualizing packet transfers.

**Threads**

The client and server operations run on separate threads to ensure that the UI remains responsive and the packet transmission is smooth.

**Graph Plotting**

matplotlib is used to plot the real-time progress of packet transfer in both sender and receiver modes. The graph updates with each packet sent/received.

# Future improvements

- Add support for IPv6-to-IPv4 translation.
- Improve error handling and display more detailed logs.
- Add the option to log transmissions to a file.



