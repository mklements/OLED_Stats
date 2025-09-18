#!/bin/bash
# filepath: install_oled_stats.sh

# OLED Stats Display Installation Script
# Automates the installation process for Raspberry Pi OS Bookworm
# Usage: curl -fsSL https://raw.githubusercontent.com/4ngel2769/rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh | bash

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Function to check if running on Raspberry Pi
check_raspberry_pi() {
    if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
        print_error "This script is designed for Raspberry Pi only!"
        exit 1
    fi
    print_success "Raspberry Pi detected"
}

# Function to check if I2C is enabled
check_i2c_enabled() {
    if ! lsmod | grep -q i2c_bcm2835; then
        print_warning "I2C interface is not enabled. Please enable it manually using 'sudo raspi-config'"
        print_warning "Go to: 3 Interfacing Options -> I5 I2C -> Yes -> Ok -> Finish"
        read -p "Press Enter after enabling I2C and rebooting..."
    fi
}

# Function to detect OLED display
detect_oled() {
    print_status "Checking for OLED display at address 0x3c..."
    if i2cdetect -y 1 | grep -q "3c"; then
        print_success "OLED display detected at address 0x3c"
        return 0
    else
        print_error "OLED display not detected. Please check your connections:"
        print_error "  GND -> Pin 6 (Ground)"
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
    print_status "Starting OLED Stats Display installation..."
    
    # Check if running on Raspberry Pi
    check_raspberry_pi
    
    # Get the actual username
    USERNAME=$(get_username)
    HOME_DIR="/home/$USERNAME"
    
    print_status "Installing for user: $USERNAME"
    print_status "Home directory: $HOME_DIR"
    
    # Step 1: Update system
    print_status "Updating system packages..."
    sudo apt-get update -qq
    sudo apt-get upgrade -y -qq
    print_success "System updated"
    
    # Step 2: Install required packages
    print_status "Installing required packages..."
    sudo apt-get install -y python3-pip python3-venv git i2c-tools
    sudo apt-get install --upgrade python3-setuptools -y
    print_success "Required packages installed"
    
    # Check I2C
    check_i2c_enabled
    
    # Step 3: Create virtual environment
    print_status "Creating virtual environment..."
    cd "$HOME_DIR"
    
    # Remove existing virtual environment if it exists
    if [ -d "stats_env" ]; then
        print_warning "Existing stats_env found, removing..."
        rm -rf stats_env
    fi
    
    sudo -u "$USERNAME" python3 -m venv stats_env --system-site-packages
    print_success "Virtual environment created"
    
    # Step 4: Install Adafruit Blinka
    print_status "Installing Adafruit Blinka library..."
    sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install --upgrade adafruit-python-shell"
    
    # Download and run Blinka installer
    cd /tmp
    wget -q https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
    
    print_warning "The Blinka installer may prompt for a reboot. Choose 'N' when asked to reboot - we'll handle it at the end."
    sudo -E env PATH=$PATH python3 raspi-blinka.py
    
    print_success "Blinka library installed"
    
    # Step 5: Install CircuitPython libraries
    print_status "Installing CircuitPython libraries..."
    sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install --upgrade adafruit_blinka"
    sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install adafruit-circuitpython-ssd1306"
    sudo apt-get install -y python3-pil
    
    # Install psutil for the enhanced version
    sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && pip3 install psutil"
    print_success "CircuitPython libraries installed"
    
    # Step 6: Clone the repository
    print_status "Downloading OLED Stats scripts..."
    cd "$HOME_DIR"
    
    # Remove existing directory if it exists
    if [ -d "rpi_oled_stats" ]; then
        print_warning "Existing rpi_oled_stats directory found, removing..."
        sudo rm -rf rpi_oled_stats
    fi
    
    sudo -u "$USERNAME" git clone https://github.com/mklements/OLED_Stats.git rpi_oled_stats
    cd rpi_oled_stats
    
    # Download font files if they don't exist
    if [ ! -f "PixelOperator.ttf" ]; then
        print_status "Downloading PixelOperator font..."
        sudo -u "$USERNAME" wget -q "https://github.com/mklements/OLED_Stats/raw/main/PixelOperator.ttf"
    fi
    
    if [ ! -f "lineawesome-webfont.ttf" ]; then
        print_status "Downloading LineAwesome font..."
        sudo -u "$USERNAME" wget -q "https://github.com/mklements/OLED_Stats/raw/main/lineawesome-webfont.ttf"
    fi
    
    print_success "Scripts downloaded"
    
    # Step 7: Detect OLED display
    if ! detect_oled; then
        print_error "Cannot continue without OLED display. Please check connections and run script again."
        exit 1
    fi
    
    # Step 8: Test the scripts
    print_status "Testing OLED display scripts..."
    
    # Choose which script to run
    echo ""
    echo "Available script options:"
    echo "1) stats.py - Simple text-based display"
    echo "2) monitor.py - Display with icons"
    echo "3) psutilstats.py - Enhanced compatibility (recommended)"
    echo ""
    read -p "Which script would you like to use as default? (1-3): " SCRIPT_CHOICE
    
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
    
    # Test the selected script for 10 seconds
    print_status "Testing $DEFAULT_SCRIPT for 10 seconds..."
    sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && cd $HOME_DIR/rpi_oled_stats && timeout 10 python3 $DEFAULT_SCRIPT || true"
    print_success "Script test completed"
    
    # Step 9: Create startup script
    print_status "Creating startup script..."
    cat > "$HOME_DIR/oled_display_start.sh" << EOF
#!/bin/bash
source $HOME_DIR/stats_env/bin/activate
cd $HOME_DIR/rpi_oled_stats
python3 $DEFAULT_SCRIPT
EOF
    
    chmod +x "$HOME_DIR/oled_display_start.sh"
    chown "$USERNAME:$USERNAME" "$HOME_DIR/oled_display_start.sh"
    print_success "Startup script created"
    
    # Step 10: Setup auto-start
    print_status "Setting up auto-start on boot..."
    
    # Add to crontab for the user
    CRON_JOB="@reboot $HOME_DIR/oled_display_start.sh &"
    
    # Check if cron job already exists
    if ! sudo -u "$USERNAME" crontab -l 2>/dev/null | grep -q "oled_display_start.sh"; then
        (sudo -u "$USERNAME" crontab -l 2>/dev/null; echo "$CRON_JOB") | sudo -u "$USERNAME" crontab -
        print_success "Auto-start configured"
    else
        print_warning "Auto-start already configured"
    fi
    
    # Step 11: Final instructions
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
    echo "✓ Auto-start configured"
    echo "✓ OLED display detected and tested"
    echo ""
    echo "MANUAL COMMANDS:"
    echo "Start manually: $HOME_DIR/oled_display_start.sh"
    echo "Change script: Edit $HOME_DIR/oled_display_start.sh"
    echo ""
    echo "The display will start automatically on next boot."
    echo ""
    read -p "Would you like to reboot now to start the display? (y/n): " REBOOT_CHOICE
    
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
