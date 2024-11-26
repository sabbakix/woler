import curses
import csv
import subprocess
import time

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

def ping_ip(ip_address, count=1):
    try:
        output = subprocess.check_output(['ping', '-c', str(count), ip_address], universal_newlines=True)
        return output
    except subprocess.CalledProcessError:
        return "Ping failed"

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
            message = (
                f"You have selected number {current_row + 1}\n"
                f"PC Name: {selected_row[0]}\n"
                f"MAC Address: {selected_row[1]}\n"
                f"IP Address: {selected_row[2]}"
            )
            stdscr.addstr(0, 0, message, curses.color_pair(1))
            stdscr.refresh()
            
            # Keep pinging and updating the message until a key is pressed
            while True:
                ping_result = ping_ip(selected_row[2], 1)
                stdscr.addstr(5, 0, f"Ping result:\n{ping_result}", curses.color_pair(1))
                stdscr.refresh()
                time.sleep(1)
                
                if stdscr.getch() != -1:
                    break

if __name__ == "__main__":
    curses.wrapper(main)