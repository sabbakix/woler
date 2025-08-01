import curses
import csv
import subprocess
import platform
import socket

def is_port_open(host, port):
    """
    Check if a specific port is open on the given host.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex((host, port))
        return result == 0

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    
    # Enable keypad mode
    stdscr.keypad(True)
    
    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected row color
    
    # Set the background color
    stdscr.bkgd(' ', curses.color_pair(1))
    
    # Create a border around the window
    stdscr.border(0)
    
    # Add a title to the window
    stdscr.addstr(0, 2, " CSV Viewer ", curses.A_BOLD | curses.color_pair(1))
    
    # Read the CSV file
    file_path = 'list.csv'
    data = read_csv(file_path)
    
    current_row = 0
    
    while True:
        # Display the CSV content with line numbers
        for idx, row in enumerate(data):
            line = f"{idx + 1}. " + ', '.join(row)
            if idx == current_row:
                stdscr.addstr(idx + 2, 2, line, curses.color_pair(2))  # Highlight selected row
            else:
                stdscr.addstr(idx + 2, 2, line, curses.color_pair(1))  # Normal row color
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(data) - 1:
            current_row += 1
        elif key == ord('\n'):
            stdscr.clear()
            selected_row = data[current_row]
            port1 = 3389  # Example port to check
            message = (
                f"You have selected number {current_row + 1}\n"
                f"PC Name: {selected_row[0]}\n"
                f"MAC Address: {selected_row[1]}\n"
                f"IP Address: {selected_row[2]}\n\n"
                "Checking if port {port} is open on the selected IP address...\n"
            )
            stdscr.addstr(0, 0, message, curses.color_pair(1))
            stdscr.refresh()
            
            ip_address = selected_row[2]
            port_status = is_port_open(ip_address, port1)
            status_message = f"Port {port1} is {'open' if port_status else 'closed'}."
            stdscr.addstr(6, 0, status_message, curses.color_pair(1))
            stdscr.refresh()
            stdscr.getch()
            break

if __name__ == "__main__":
    curses.wrapper(main)