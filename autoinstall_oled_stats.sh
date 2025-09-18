#!/bin/bash

# OLED Stats Display Installation Script
# Automates the installation process for Raspberry Pi OS Bookworm
# Usage: curl -fsSL https://raw.githubusercontent.com/4ngel2769/rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh | bash
# Usage with verbose: curl -fsSL https://raw.githubusercontent.com/4ngel2769/rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh | bash -s -- -v

set -e  # Exit on any error

# Default verbosity level
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${CYAN}[VERBOSE]${NC} $1"
    fi
}

# Function to run commands with optional verbose output
run_command() {
    local cmd="$1"
    local description="$2"
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "Running: $cmd"
        eval "$cmd"
    else
        if [ -n "$description" ]; then
            eval "$cmd" >/dev/null 2>&1 || {
                print_error "$description failed"
                exit 1
            }
        else
            eval "$cmd" >/dev/null 2>&1
        fi
    fi
}

# Function to check if running on Raspberry Pi
check_raspberry_pi() {
    print_verbose "Checking if running on Raspberry Pi..."
    if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
        print_error "This script is designed for Raspberry Pi only!"
        exit 1
    fi
    
    if [ "$VERBOSE" = true ]; then
        local pi_model=$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0')
        print_verbose "Detected: $pi_model"
    fi
    
    print_success "Raspberry Pi detected"
}

# Function to check if I2C is enabled
check_i2c_enabled() {
    print_verbose "Checking if I2C interface is enabled..."
    
    if ! lsmod | grep -q i2c_bcm2835; then
        print_warning "I2C interface is not enabled. Please enable it manually using 'sudo raspi-config'"
        print_warning "Go to: 3 Interfacing Options -> I5 I2C -> Yes -> Ok -> Finish"
        read -p "Press Enter after enabling I2C and rebooting..." < /dev/tty
    else
        print_verbose "I2C interface is enabled"
    fi
}

# Function to detect OLED display
detect_oled() {
    print_status "Checking for OLED display at address 0x3c..."
    print_verbose "Running i2cdetect to scan for devices..."
    
    if [ "$VERBOSE" = true ]; then
        echo "I2C scan results:"
        sudo i2cdetect -y 1
    fi
    
    if sudo i2cdetect -y 1 | grep -q "3c"; then
        print_success "OLED display detected at address 0x3c"
        return 0
    else
        print_error "OLED display not detected. Please check your connections:"
        print_error "  GND -> Pin 9 (Ground)"
        print_error "  VCC -> Pin 1 (3.3V)"
        print_error "  SDA -> Pin 3 (GPIO 2)"
        print_error "  SCL -> Pin 5 (GPIO 3)"
        return 1
    fi
}

# Get username (handle both pi and custom usernames)
get_username() {
    if [ "$USER" = "root" ]; then
        # If running as root, get the actual user
        ACTUAL_USER=$(who am i | awk '{print $1}')
        if [ -z "$ACTUAL_USER" ]; then
            ACTUAL_USER="pi"  # Default fallback
        fi
    else
        ACTUAL_USER="$USER"
    fi
    echo "$ACTUAL_USER"
}

# Main installation function
main() {
    if [ "$VERBOSE" = true ]; then
        print_verbose "Verbose mode enabled"
        print_verbose "Script arguments:" "$@"
    fi
    
    print_status "Starting OLED Stats Display installation..."
    
    # Check if running on Raspberry Pi
    check_raspberry_pi
    
    # Get the actual username
    USERNAME=$(get_username)
    HOME_DIR="/home/$USERNAME"
    
    print_status "Installing for user: $USERNAME"
    print_status "Home directory: $HOME_DIR"
    print_verbose "Current working directory: $(pwd)"
    print_verbose "Current user: $(whoami)"
    
    # Step 1: Update system
    print_status "Updating system packages..."
    if [ "$VERBOSE" = true ]; then
        sudo apt-get update
        # sudo apt-get upgrade -y
    else
        sudo apt-get update -qq
        # sudo apt-get upgrade -y -qq
    fi
    print_success "System updated"

    # Step 2: Install required packages
    print_status "Installing required packages..."
    print_verbose "Installing: python3-pip python3-venv git i2c-tools"
    
    if [ "$VERBOSE" = true ]; then
        sudo apt-get install -y python3-pip python3-venv git i2c-tools
        sudo apt-get install --upgrade python3-setuptools -y
    else
        sudo apt-get install -y python3-pip python3-venv git i2c-tools >/dev/null 2>&1
        sudo apt-get install --upgrade python3-setuptools -y >/dev/null 2>&1
    fi
    print_success "Required packages installed"
    
    # Check I2C
    check_i2c_enabled
    
    # Step 3: Create virtual environment
    print_status "Creating virtual environment..."
    cd "$HOME_DIR"
    print_verbose "Changed to directory: $HOME_DIR"
    
    # Remove existing virtual environment if it exists
    if [ -d "stats_env" ]; then
        print_warning "Existing stats_env found, removing..."
        print_verbose "Removing directory: $HOME_DIR/stats_env"
        rm -rf stats_env
    fi
    
    print_verbose "Creating virtual environment with system site packages..."
    sudo -u "$USERNAME" python3 -m venv stats_env --system-site-packages
    print_success "Virtual environment created"
    
    # Step 4: Skip Blinka installer and install libraries directly
    print_status "Installing required Python libraries..."
    print_verbose "Installing libraries directly in virtual environment..."
    
    if [ "$VERBOSE" = true ]; then
        # Install libraries directly without the problematic Blinka installer
        sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install --upgrade adafruit-blinka"
        sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install adafruit-circuitpython-ssd1306"
        sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install psutil"
        sudo apt-get install -y python3-pil
    else
        sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install --upgrade adafruit-blinka" >/dev/null 2>&1
        sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install adafruit-circuitpython-ssd1306" >/dev/null 2>&1
        sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install psutil" >/dev/null 2>&1
        sudo apt-get install -y python3-pil >/dev/null 2>&1
    fi
    
    print_success "Python libraries installed"
    
    # Step 5: Clone the repository
    print_status "Downloading OLED Stats scripts..."
    cd "$HOME_DIR"
    
    # Remove existing directory if it exists
    if [ -d "rpi_oled_stats" ]; then
        print_warning "Existing rpi_oled_stats directory found, removing..."
        print_verbose "Removing directory: $HOME_DIR/rpi_oled_stats"
        sudo rm -rf rpi_oled_stats
    fi
    
    print_verbose "Cloning repository from GitHub..."
    if [ "$VERBOSE" = true ]; then
        sudo -u "$USERNAME" git clone https://github.com/4ngel2769/rpi_oled_stats.git rpi_oled_stats
    else
        sudo -u "$USERNAME" git clone https://github.com/4ngel2769/rpi_oled_stats.git rpi_oled_stats >/dev/null 2>&1
    fi
    
    cd rpi_oled_stats
    print_verbose "Changed to directory: $HOME_DIR/rpi_oled_stats"
    
    # Download font files if they don't exist
    if [ ! -f "PixelOperator.ttf" ]; then
        print_status "Downloading PixelOperator font..."
        print_verbose "Font not found, downloading PixelOperator.ttf..."
        sudo -u "$USERNAME" wget -q "https://github.com/mklements/OLED_Stats/raw/main/PixelOperator.ttf"
    else
        print_verbose "PixelOperator.ttf already exists"
    fi
    
    if [ ! -f "lineawesome-webfont.ttf" ]; then
        print_status "Downloading LineAwesome font..."
        print_verbose "Font not found, downloading lineawesome-webfont.ttf..."
        sudo -u "$USERNAME" wget -q "https://github.com/mklements/OLED_Stats/raw/main/lineawesome-webfont.ttf"
    else
        print_verbose "lineawesome-webfont.ttf already exists"
    fi
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "Directory contents:"
        ls -la
    fi
    
    print_success "Scripts downloaded"
    
    # Step 6: Detect OLED display
    if ! detect_oled; then
        print_warning "OLED display not detected. The script will still create the startup configuration."
        print_warning "Please check your connections and the display should work after reboot."
    fi
    
    # Step 7: Choose and test the scripts
    print_status "Selecting OLED display script..."
    
    # Choose which script to run
    echo ""
    echo "Available script options:"
    echo "1) stats.py - Simple text-based display"
    echo "2) monitor.py - Display with icons"
    echo "3) psutilstats.py - Enhanced compatibility (recommended)"
    echo ""
    read -p "Which script would you like to use as default? (1-3): " SCRIPT_CHOICE < /dev/tty
    
    case $SCRIPT_CHOICE in
        1)
            DEFAULT_SCRIPT="stats.py"
            ;;
        2)
            DEFAULT_SCRIPT="monitor.py"
            ;;
        3)
            DEFAULT_SCRIPT="psutilstats.py"
            ;;
        *)
            print_warning "Invalid choice, using psutilstats.py as default"
            DEFAULT_SCRIPT="psutilstats.py"
            ;;
    esac
    
    print_verbose "Selected script: $DEFAULT_SCRIPT"
    
    # Test the selected script for 5 seconds if OLED was detected
    if sudo i2cdetect -y 1 | grep -q "3c"; then
        print_status "Testing $DEFAULT_SCRIPT for 5 seconds..."
        print_verbose "Running test command: timeout 5 python3 $DEFAULT_SCRIPT"
        
        if [ "$VERBOSE" = true ]; then
            sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && cd $HOME_DIR/rpi_oled_stats && timeout 5 python3 $DEFAULT_SCRIPT || true"
        else
            sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && cd $HOME_DIR/rpi_oled_stats && timeout 5 python3 $DEFAULT_SCRIPT || true" >/dev/null 2>&1
        fi
        print_success "Script test completed"
    else
        print_status "Skipping script test (OLED not detected)"
    fi
    
    # Step 8: Create startup script
    print_status "Creating startup script..."
    print_verbose "Creating startup script at: $HOME_DIR/oled_display_start.sh"
    
    cat > "$HOME_DIR/oled_display_start.sh" << EOF
#!/bin/bash
# Wait for system to fully boot
sleep 30
source $HOME_DIR/stats_env/bin/activate
cd $HOME_DIR/rpi_oled_stats
python3 $DEFAULT_SCRIPT
EOF
    
    chmod +x "$HOME_DIR/oled_display_start.sh"
    chown "$USERNAME:$USERNAME" "$HOME_DIR/oled_display_start.sh"
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "Startup script contents:"
        cat "$HOME_DIR/oled_display_start.sh"
    fi
    
    print_success "Startup script created"
    
    # Step 9: Setup auto-start
    print_status "Setting up auto-start on boot..."
    
    # Add to crontab for the user
    CRON_JOB="@reboot $HOME_DIR/oled_display_start.sh &"
    print_verbose "Cron job: $CRON_JOB"
    
    # Check if cron job already exists
    if ! sudo -u "$USERNAME" crontab -l 2>/dev/null | grep -q "oled_display_start.sh"; then
        print_verbose "Adding cron job for auto-start..."
        (sudo -u "$USERNAME" crontab -l 2>/dev/null; echo "$CRON_JOB") | sudo -u "$USERNAME" crontab -
        print_success "Auto-start configured"
        
        if [ "$VERBOSE" = true ]; then
            print_verbose "Current crontab for $USERNAME:"
            sudo -u "$USERNAME" crontab -l
        fi
    else
        print_warning "Auto-start already configured"
    fi
    
    # Step 10: Final instructions
    print_success "Installation completed successfully!"
    echo ""
    echo "=========================================="
    echo "INSTALLATION SUMMARY"
    echo "=========================================="
    echo "✓ System updated"
    echo "✓ Required packages installed"
    echo "✓ Virtual environment created at: $HOME_DIR/stats_env"
    echo "✓ OLED Stats scripts installed at: $HOME_DIR/rpi_oled_stats"
    echo "✓ Default script set to: $DEFAULT_SCRIPT"
    echo "✓ Auto-start configured with 30-second boot delay"
    echo "✓ Installation completed"
    echo ""
    echo "MANUAL COMMANDS:"
    echo "Start manually: $HOME_DIR/oled_display_start.sh"
    echo "Change script: Edit $HOME_DIR/oled_display_start.sh"
    echo ""
    echo "The display will start automatically 30 seconds after boot."
    echo ""
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "System information:"
        print_verbose "Kernel: $(uname -r)"
        print_verbose "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
        print_verbose "Python version: $(python3 --version)"
        print_verbose "Disk space available: $(df -h $HOME_DIR | tail -1 | awk '{print $4}')"
    fi
    
    read -p "Would you like to reboot now to start the display? (y/n): " REBOOT_CHOICE < /dev/tty
    
    if [[ $REBOOT_CHOICE =~ ^[Yy]$ ]]; then
        print_status "Rebooting system..."
        sudo reboot
    else
        print_status "You can start the display manually with: $HOME_DIR/oled_display_start.sh"
        print_status "Or reboot to start automatically: sudo reboot"
    fi
}

# Run main function
main "$@"
