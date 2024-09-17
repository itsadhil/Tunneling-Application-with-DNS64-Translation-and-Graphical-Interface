import socket
import ipaddress
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Class for package structure
class Package:
    def __init__(self, data, src_ip, dst_ip):
        self.data = data
        self.src_ip = src_ip
        self.dst_ip = dst_ip

# Class for DNS64 functionality
class DNS64:
    def __init__(self, ipv4_addr, ipv6_addr):
        self.ipv4_addr = ipv4_addr
        self.ipv6_addr = ipv6_addr

    def translate_addr(self, addr):
        ip_obj = ipaddress.ip_address(addr)
        if ip_obj.version == 4:
            return self.ipv6_addr
        elif ip_obj.version == 6:
            return self.ipv4_addr
        else:
            raise ValueError("Invalid address version")

# Client class that connects to the server and sends the package
class Client:
    def __init__(self, host, port, dns64, log_callback, graph_callback, interval=1, packet_count=10):
        self.host = host
        self.port = port
        self.dns64 = dns64
        self.log_callback = log_callback
        self.graph_callback = graph_callback
        self.interval = interval
        self.packet_count = packet_count
        self.is_sending = False
        self.client_socket = None  # Initially, no socket is created

    def get_local_ip(self):
        """Retrieve the local IPv4 address of the sender using a separate socket."""
        try:
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.connect(('8.8.8.8', 80))  # Dummy connection to get the local IP
            local_ip = temp_socket.getsockname()[0]
            temp_socket.close()
            return local_ip
        except Exception as e:
            self.log_callback(f"Error retrieving local IP: {str(e)}")
            return None

    def connect_to_system(self):
        """Creates a socket and connects to the server"""
        try:
            if self.client_socket is None:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.log_callback(f"Connecting to {self.host}:{self.port}")
            self.client_socket.connect((self.host, self.port))
            self.log_callback("Connection established")
        except Exception as e:
            self.log_callback(f"Connection failed: {str(e)}")
            self.client_socket = None

    def send_package(self, package, packet_num):
        """Sends a single package to the receiver"""
        try:
            if self.client_socket:
                self.log_callback(f"Sending package with IPv4: {package.src_ip}")
                self.client_socket.sendall(package.data)

                # Receive response
                response = self.client_socket.recv(1024)
                self.log_callback(f"Received response from server (IPv6): {response.decode()}")

                # Update the graph with current packet number
                self.graph_callback(packet_num)
            else:
                self.log_callback("No open socket to send the package")
        except Exception as e:
            self.log_callback(f"Error sending package: {str(e)}")

    def start_sending(self):
        """Starts sending multiple packages continuously"""
        self.is_sending = True
        self.connect_to_system()  # Connect only once, before sending multiple packets

        if self.client_socket:
            local_ipv4 = self.get_local_ip()
            if local_ipv4:
                for i in range(self.packet_count):
                    if not self.is_sending:
                        self.log_callback("Stopped sending packets.")
                        break

                    package_data = f"{local_ipv4} Packet {i + 1}".encode()
                    package = Package(package_data, local_ipv4, "::1")
                    self.send_package(package, i + 1)
                    self.log_callback(f"Sent packet {i + 1}/{self.packet_count}")
                    time.sleep(self.interval)

            self.is_sending = False

            # Close the socket only after all packets have been sent
            self.client_socket.close()
            self.client_socket = None
        else:
            self.log_callback("Failed to connect to the server")

    def stop_sending(self):
        """Stops the sending process"""
        self.is_sending = False


# Server class to listen for connections and respond
class Server:
    def __init__(self, host, port, dns64, log_callback, graph_callback):
        self.host = host
        self.port = port
        self.dns64 = dns64
        self.log_callback = log_callback
        self.graph_callback = graph_callback
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.packet_count = 0

    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.log_callback(f"Listening for connections on {self.host}:{self.port}")
            
            conn, addr = self.server_socket.accept()
            self.log_callback(f"Connected to {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    break

                self.packet_count += 1  # Increment packet count for graph update
                self.log_callback(f"Received data from client: {data.decode()}")

                # Translate the IPv4 to IPv6 using DNS64
                translated_ipv6 = self.dns64.translate_addr(data.decode().split()[0])
                self.log_callback(f"Translated IPv4 to IPv6: {translated_ipv6}")

                conn.sendall(str(translated_ipv6).encode())
                self.log_callback("Sent IPv6 back to the client")

                # Update the graph with the received packet number
                self.graph_callback(self.packet_count)

            conn.close()
        except Exception as e:
            self.log_callback(f"Server error: {str(e)}")
        finally:
            self.server_socket.close()


# Tkinter UI for logging and input, with graph plotting
class TunnelUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tunneling App with Graph")

        # Console log area
        self.log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.log_area.pack(padx=10, pady=10)

        # Sender/Receiver Input Frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        # Role selection buttons
        self.sender_button = tk.Button(self.input_frame, text="Start as Sender", command=self.start_as_sender)
        self.sender_button.grid(row=0, column=0, padx=5)

        self.receiver_button = tk.Button(self.input_frame, text="Start as Receiver", command=self.start_as_receiver)
        self.receiver_button.grid(row=0, column=1, padx=5)

        # Create a figure for plotting
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)
        self.ax.set_xlabel("Packet Number")
        self.ax.set_ylabel("Transmission Progress")
        self.packet_numbers = []

    def log(self, message):
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)

    def update_graph(self, packet_num):
        """Update the graph with the current packet number."""
        self.packet_numbers.append(packet_num)
        self.ax.clear()
        self.ax.plot(self.packet_numbers, label="Packet Transfer")
        self.ax.set_xlabel("Packet Number")
        self.ax.set_ylabel("Transmission Progress")
        self.ax.legend()
        self.canvas.draw()

    # Function to start as sender
    def start_as_sender(self):
        sender_window = tk.Toplevel(self.root)
        sender_window.title("Sender")

        tk.Label(sender_window, text="Receiver IP:").pack(pady=5)
        receiver_ip = tk.Entry(sender_window)
        receiver_ip.pack(pady=5)

        tk.Label(sender_window, text="Receiver Port:").pack(pady=5)
        receiver_port = tk.Entry(sender_window)
        receiver_port.pack(pady=5)

        tk.Label(sender_window, text="Packet Interval (seconds):").pack(pady=5)
        packet_interval = tk.Entry(sender_window)
        packet_interval.insert(0, "1")
        packet_interval.pack(pady=5)

        tk.Label(sender_window, text="Number of Packets:").pack(pady=5)
        packet_count = tk.Entry(sender_window)
        packet_count.insert(0, "10")
        packet_count.pack(pady=5)

        start_button = tk.Button(sender_window, text="Start Sending", command=lambda: self.start_sending(
            receiver_ip.get(), int(receiver_port.get()), float(packet_interval.get()), int(packet_count.get())))
        start_button.pack(pady=10)

        stop_button = tk.Button(sender_window, text="Stop Sending", command=self.stop_sending)
        stop_button.pack(pady=5)

    # Function to start as receiver
    def start_as_receiver(self):
        receiver_window = tk.Toplevel(self.root)
        receiver_window.title("Receiver")

        tk.Label(receiver_window, text="Your IP:").pack(pady=5)
        host_ip = tk.Entry(receiver_window)
        host_ip.insert(0, "0.0.0.0")  # default to bind to all IPs
        host_ip.pack(pady=5)

        tk.Label(receiver_window, text="Listening Port:").pack(pady=5)
        listen_port = tk.Entry(receiver_window)
        listen_port.pack(pady=5)

        start_button = tk.Button(receiver_window, text="Start Listening", command=lambda: self.start_listening(host_ip.get(), int(listen_port.get())))
        start_button.pack(pady=10)

    # Start the sending process
    def start_sending(self, host, port, interval, packet_count):
        dns64 = DNS64("192.168.56.1", "2409:40f4:2b:ac0c:390c:2f3d:af39:8ad6")
        self.client = Client(host, port, dns64, self.log, self.update_graph, interval, packet_count)

        # Connect to the receiver and send package
        Thread(target=lambda: self.client.start_sending()).start()

    def stop_sending(self):
        if hasattr(self, 'client'):
            self.client.stop_sending()

    # Start the listening process
    def start_listening(self, host, port):
        dns64 = DNS64("192.168.56.1", "2409:40f4:2b:ac0c:390c:2f3d:af39:8ad6")
        server = Server(host, port, dns64, self.log, self.update_graph)

        # Start server in a new thread to avoid blocking the UI
        Thread(target=server.start_server).start()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TunnelUI(root)
    root.mainloop()
