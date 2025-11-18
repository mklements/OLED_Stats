#!/bin/bash

# OLED Stats Display Installation Script
# Version: v0.9
# Script Author: 4ngel2769 / @angeldev0
# Original OLED Stats Code: MKlement (mklements)
# Repository: https://github.com/4ngel2769/rpi_oled_stats
# Original Code: https://github.com/mklements/OLED_Stats
# Automates the installation process for Raspberry Pi OS Bookworm
# Usage: curl -fsSL https://raw.githubusercontent.com/4ngel2769/rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh | bash
# Usage with verbose: curl -fsSL https://raw.githubusercontent.com/4ngel2769/rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh | bash -s -- -v

set -e  # Exit on any error

# Script version
SCRIPT_VERSION="v0.9"
SCRIPT_AUTHOR="4ngel2769 / @angeldev0"
ORIGINAL_AUTHOR="MKlement (mklements)"

# Default verbosity level
VERBOSE=false

# ================================================================================
# THEME CONFIGURATION
# ================================================================================
# Available themes: STANDARD, HTB, PASTEL
COLOR_SCHEME="PASTEL"  # Default theme

# Color resets
# WHITE='\033[1;37m'
NC='\033[0m'

# ================================================================================
# STANDARD COLOR PALETTE
# ================================================================================
STANDARD_PRIMARY='\033[1;36m'           # Cyan bold for borders/boxes
STANDARD_SECONDARY='\033[1;35m'         # Magenta bold for titles
STANDARD_ACCENT='\033[1;33m'            # Yellow bold for labels
STANDARD_SUCCESS='\033[0;32m'           # Green for success
STANDARD_WARNING='\033[1;33m'           # Yellow for warnings
STANDARD_ERROR='\033[0;31m'             # Red for errors
STANDARD_INFO='\033[0;34m'              # Blue for info
STANDARD_HIGHLIGHT='\033[0;36m'         # Cyan for verbose
STANDARD_TEXT='\033[1;37m'              # White bold for text
STANDARD_SPECIAL='\033[1;32m'           # Green bold for special items

# ================================================================================
# HTB COLOR PALETTE (Hack The Box inspired)
# ================================================================================
HTB_PRIMARY="\033[38;5;19m"             # Deep blue for borders
HTB_SECONDARY="\033[38;5;82m"           # Bright neon green for titles
HTB_ACCENT="\033[38;5;226m"             # Bright yellow for labels
HTB_SUCCESS="\033[38;5;46m"             # Matrix green for success
HTB_WARNING="\033[38;5;214m"            # HTB orange for warnings
HTB_ERROR="\033[38;5;196m"              # Bright red for errors
HTB_INFO="\033[38;5;33m"                # Vivid blue for info
HTB_HIGHLIGHT="\033[38;5;51m"           # Bright cyan for verbose
HTB_TEXT="\033[38;5;250m"               # Light grey for text
HTB_SPECIAL="\033[38;5;118m"            # Lime for special items

# ================================================================================
# PASTEL COLOR PALETTE (Soft and pleasant)
# ================================================================================
PASTEL_PRIMARY="\033[38;5;159m"         # Soft cyan for borders
PASTEL_SECONDARY="\033[38;5;141m"       # Soft purple for titles
PASTEL_ACCENT="\033[38;5;110m"          # Pastel blue for version
PASTEL_SUCCESS="\033[38;5;120m"         # Soft green for success
PASTEL_WARNING="\033[38;5;215m"         # Soft orange for warnings
PASTEL_ERROR="\033[38;5;203m"           # Soft red for errors
PASTEL_INFO="\033[38;5;117m"            # Soft blue for info
PASTEL_HIGHLIGHT="\033[38;5;123m"       # Soft cyan for verbose
PASTEL_TEXT="\033[1;37m"                # White for text
PASTEL_SPECIAL="\033[38;5;114m"         # Nice green for special items
PASTEL_GOLD="\033[38;5;220m"            # Gold for credits

# ================================================================================
# DYNAMIC COLOR FUNCTIONS
# ================================================================================
get_color() {
    local color_name="$1"
    case "$COLOR_SCHEME" in
        "STANDARD")
            case "$color_name" in
                "PRIMARY") echo "$STANDARD_PRIMARY" ;;
                "SECONDARY") echo "$STANDARD_SECONDARY" ;;
                "ACCENT") echo "$STANDARD_ACCENT" ;;
                "SUCCESS") echo "$STANDARD_SUCCESS" ;;
                "WARNING") echo "$STANDARD_WARNING" ;;
                "ERROR") echo "$STANDARD_ERROR" ;;
                "INFO") echo "$STANDARD_INFO" ;;
                "HIGHLIGHT") echo "$STANDARD_HIGHLIGHT" ;;
                "TEXT") echo "$STANDARD_TEXT" ;;
                "SPECIAL") echo "$STANDARD_SPECIAL" ;;
                "GOLD") echo "$STANDARD_ACCENT" ;;
                *) echo "$NC" ;;
            esac
            ;;
        "HTB")
            case "$color_name" in
                "PRIMARY") echo "$HTB_PRIMARY" ;;
                "SECONDARY") echo "$HTB_SECONDARY" ;;
                "ACCENT") echo "$HTB_ACCENT" ;;
                "SUCCESS") echo "$HTB_SUCCESS" ;;
                "WARNING") echo "$HTB_WARNING" ;;
                "ERROR") echo "$HTB_ERROR" ;;
                "INFO") echo "$HTB_INFO" ;;
                "HIGHLIGHT") echo "$HTB_HIGHLIGHT" ;;
                "TEXT") echo "$HTB_TEXT" ;;
                "SPECIAL") echo "$HTB_SPECIAL" ;;
                "GOLD") echo "$HTB_ACCENT" ;;
                *) echo "$NC" ;;
            esac
            ;;
        "PASTEL")
            case "$color_name" in
                "PRIMARY") echo "$PASTEL_PRIMARY" ;;
                "SECONDARY") echo "$PASTEL_SECONDARY" ;;
                "ACCENT") echo "$PASTEL_ACCENT" ;;
                "SUCCESS") echo "$PASTEL_SUCCESS" ;;
                "WARNING") echo "$PASTEL_WARNING" ;;
                "ERROR") echo "$PASTEL_ERROR" ;;
                "INFO") echo "$PASTEL_INFO" ;;
                "HIGHLIGHT") echo "$PASTEL_HIGHLIGHT" ;;
                "TEXT") echo "$PASTEL_TEXT" ;;
                "SPECIAL") echo "$PASTEL_SPECIAL" ;;
                "GOLD") echo "$PASTEL_GOLD" ;;
                *) echo "$NC" ;;
            esac
            ;;
        *)
            echo "$NC"
            ;;
    esac
}

# Convenient color functions
c_primary() { get_color "PRIMARY"; }
c_secondary() { get_color "SECONDARY"; }
c_accent() { get_color "ACCENT"; }
c_success() { get_color "SUCCESS"; }
c_warning() { get_color "WARNING"; }
c_error() { get_color "ERROR"; }
c_info() { get_color "INFO"; }
c_highlight() { get_color "HIGHLIGHT"; }
c_text() { get_color "TEXT"; }
c_special() { get_color "SPECIAL"; }
c_gold() { get_color "GOLD"; }

set_theme() {
    local theme_num="$1"
    case "$theme_num" in
        1)
            COLOR_SCHEME="STANDARD"
            ;;
        2)
            COLOR_SCHEME="HTB"
            ;;
        3)
            COLOR_SCHEME="PASTEL"
            ;;
        *)
            echo "❌ Invalid theme number. Using default PASTEL theme."
            COLOR_SCHEME="PASTEL"
            ;;
    esac
}

# Function to show version information
show_version() {
    echo ""
    echo -e "$(c_primary)╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "$(c_primary)║$(c_secondary)              🚀 OLED Stats Installation Script                 $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║${NC} $(c_accent)Version:${NC} $SCRIPT_VERSION                                                  $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)Script Author:${NC} $SCRIPT_AUTHOR                          $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)Original Code:${NC} $ORIGINAL_AUTHOR                            $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)🔗 Repository:${NC}                                                 $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   https://github.com/4ngel2769/rpi_oled_stats                  $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)🔗 Original Code:${NC}                                              $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   https://github.com/mklements/OLED_Stats                      $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)📋 Description:${NC}                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   Automates OLED Stats Display installation for                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   Raspberry Pi running Raspberry Pi OS Bookworm                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_gold)🏆 Credits:${NC}                                                    $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   • Installation script by $SCRIPT_AUTHOR              $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   • Original OLED Stats by $ORIGINAL_AUTHOR                $(c_primary)║${NC}"
    echo -e "$(c_primary)╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    exit 0
}

# Function to show help information
show_help() {
    echo ""
    echo -e "$(c_primary)╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "$(c_primary)║$(c_secondary)                    📖 HELP & USAGE GUIDE                       $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║${NC} $(c_accent)Script:${NC} OLED Stats Installation Script $SCRIPT_VERSION                    $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)Author:${NC} $SCRIPT_AUTHOR                                 $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)Original:${NC} $ORIGINAL_AUTHOR                                 $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║${NC} $(c_info)🚀 USAGE:${NC}                                                      $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} curl -fsSL https://raw.githubusercontent.com/4ngel2769/        $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh       $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} | bash [OPTIONS]                                               $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_accent)⚙️  OPTIONS:${NC}                                                   $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   $(c_special)-v, --verbose${NC}      Enable detailed output                    $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   $(c_special)-t, --theme <1-3>${NC}  Set color theme (1=Standard, 2=HTB, 3=Pastel) $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   $(c_special)--version${NC}          Show version information                  $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   $(c_special)-h, --help${NC}         Show this help message                    $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_secondary)🎨 AVAILABLE THEMES:${NC}                                           $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   $(c_special)1${NC} - STANDARD  (Classic terminal colors)                     $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   $(c_special)2${NC} - HTB       (Hack The Box cybersec style)               $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}   $(c_special)3${NC} - PASTEL    (Soft and pleasant colors) [Default]        $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_secondary)💡 EXAMPLES:${NC}                                                   $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)📦 Standard installation:${NC}                                      $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} curl -fsSL https://raw.githubusercontent.com/4ngel2769/        $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh       $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} | bash                                                         $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)🎨 HTB theme with verbose:${NC}                                     $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} curl -fsSL https://raw.githubusercontent.com/4ngel2769/        $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh       $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} | bash -s -- --theme 2 --verbose                              $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)🔧 Standard theme installation:${NC}                               $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} curl -fsSL https://raw.githubusercontent.com/4ngel2769/        $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} rpi_oled_stats/refs/heads/main/autoinstall_oled_stats.sh       $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} | bash -s -- -t 1                                             $(c_primary)║${NC}"
    echo -e "$(c_primary)╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    exit 0
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -t|--theme)
            if [[ -n $2 && $2 =~ ^[1-3]$ ]]; then
                set_theme "$2"
                shift 2
            else
                echo "❌ Error: --theme requires a valid number (1-3)"
                echo "   1 = Standard, 2 = HTB, 3 = Pastel"
                exit 1
            fi
            ;;
        --theme=*)
            theme_value="${1#*=}"
            if [[ $theme_value =~ ^[1-3]$ ]]; then
                set_theme "$theme_value"
                shift
            else
                echo "❌ Error: --theme requires a valid number (1-3)"
                echo "   1 = Standard, 2 = HTB, 3 = Pastel"
                exit 1
            fi
            ;;
        --version)
            show_version
            ;;
        -h|--help)
            show_help
            ;;
        *)
            shift
            ;;
    esac
done

# Function to print colored output
print_status() {
    echo -e "$(c_info)[📋 INFO >>]${NC} $1"
}

print_success() {
    echo -e "$(c_success)[✅ SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "$(c_warning)[⚠️ WARNING]${NC} $1"
}

print_error() {
    echo -e "$(c_error)[❌ ERROR]${NC} $1"
}

print_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "$(c_highlight)[🔍 VERBOSE]${NC} $1"
    fi
}

print_version_info() {
    echo ""
    echo -e "$(c_primary)╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "$(c_primary)║$(c_secondary)                 🚀 Starting OLED Installation...               $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)Script Version:${NC} $SCRIPT_VERSION                                           $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)Script Author:${NC} $SCRIPT_AUTHOR                          $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_text)Original Code:${NC} $ORIGINAL_AUTHOR                            $(c_primary)║${NC}"
    echo -e "$(c_primary)╚════════════════════════════════════════════════════════════════╝${NC}"
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
    print_verbose "🔍 Checking if running on Raspberry Pi..."
    if ! grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
        print_error "🚫 This script is designed for Raspberry Pi only!"
        exit 1
    fi
    
    if [ "$VERBOSE" = true ]; then
        local pi_model
        pi_model=$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0')
        print_verbose "🍓 Detected: $pi_model"
    fi
    
    print_success "🍓 Raspberry Pi detected"
}

# Function to check if I2C is enabled
check_i2c_enabled() {
    print_verbose "🔍 Checking if I2C interface is enabled..."
    
    if ! lsmod | grep -q i2c_bcm2835; then
        print_warning "🔧 I2C interface is not enabled. Please enable it manually using 'sudo raspi-config'"
        print_warning "📋 Go to: 3 Interfacing Options -> I5 I2C -> Yes -> Ok -> Finish"
        read -p "⏳ Press Enter after enabling I2C and rebooting..." < /dev/tty
    else
        print_verbose "✅ I2C interface is enabled"
    fi
}

# Function to detect OLED display
detect_oled() {
    print_status "🔍 Checking for OLED display at address 0x3c..."
    print_verbose "🔧 Running i2cdetect to scan for devices..."
    
    if [ "$VERBOSE" = true ]; then
        echo "📊 I2C scan results:"
        sudo i2cdetect -y 1
    fi
    
    if sudo i2cdetect -y 1 | grep -q "3c"; then
        print_success "📟 OLED display detected at address 0x3c"
        return 0
    else
        print_error "❌ OLED display not detected. Please check your connections:"
        print_error "   🔌 GND -> Pin 9 (Ground)"
        print_error "   🔌 VCC -> Pin 1 (3.3V)"
        print_error "   🔌 SDA -> Pin 3 (GPIO 2)"
        print_error "   🔌 SCL -> Pin 5 (GPIO 3)"
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
    # Show version info at start
    print_version_info
    echo ""
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "🔧 Verbose mode enabled"
        print_verbose "🎨 Using $COLOR_SCHEME theme"
        print_verbose "📋 Script arguments:" "$@"
    fi
    
    print_status "🚀 Starting OLED Stats Display installation..."
    
    # Check if running on Raspberry Pi
    check_raspberry_pi
    
    # Get the actual username
    USERNAME=$(get_username)
    HOME_DIR="/home/$USERNAME"
    
    print_status "👤 Installing for user: $USERNAME"
    print_status "🏠 Home directory: $HOME_DIR"
    print_verbose "📁 Current working directory: $(pwd)"
    print_verbose "👤 Current user: $(whoami)"
    
    # Step 1: Update system
    print_status "⚙️  Updating system packages..."
    if [ "$VERBOSE" = true ]; then
        sudo apt-get update
        # sudo apt-get upgrade -y
    else
        sudo apt-get update -qq
        # sudo apt-get upgrade -y -qq
    fi
    print_success "📦 System updated"

    # Step 2: Install required packages
    print_status "⚙️  Installing required packages..."
    print_verbose "📦 Installing: python3-pip python3-venv git i2c-tools"
    
    if [ "$VERBOSE" = true ]; then
        sudo apt-get install -y python3-pip python3-venv git i2c-tools
        sudo apt-get install --upgrade python3-setuptools -y
    else
        sudo apt-get install -y python3-pip python3-venv git i2c-tools >/dev/null 2>&1
        sudo apt-get install --upgrade python3-setuptools -y >/dev/null 2>&1
    fi
    print_success "📦 Required packages installed"
    
    # Check I2C
    check_i2c_enabled
    
    # Step 3: Create virtual environment
    print_status "🐍 Creating Python virtual environment..."
    cd "$HOME_DIR"
    print_verbose "📁 Changed to directory: $HOME_DIR"
    
    # Remove existing virtual environment if it exists
    if [ -d "stats_env" ]; then
        print_warning "🗑️  Existing stats_env found, removing..."
        print_verbose "🗑️  Removing directory: $HOME_DIR/stats_env"
        rm -rf stats_env
    fi
    
    print_verbose "🐍 Creating virtual environment with system site packages..."
    sudo -u "$USERNAME" python3 -m venv stats_env --system-site-packages
    print_success "🐍 Virtual environment created"
    
    # Step 4: Skip Blinka installer and install libraries directly
    print_status "⚙️  Installing required Python libraries..."
    print_verbose "📦 Installing libraries directly in virtual environment..."
    
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
    
    print_success "🐍 Python libraries installed"
    
    # Step 5: Clone the repository
    print_status "📥 Downloading OLED Stats scripts..."
    cd "$HOME_DIR"
    
    # Remove existing directory if it exists
    if [ -d "rpi_oled_stats" ]; then
        print_warning "🗑️  Existing rpi_oled_stats directory found, removing..."
        print_verbose "🗑️  Removing directory: $HOME_DIR/rpi_oled_stats"
        sudo rm -rf rpi_oled_stats
    fi
    
    print_verbose "📥 Cloning repository from GitHub..."
    if [ "$VERBOSE" = true ]; then
        sudo -u "$USERNAME" git clone https://github.com/4ngel2769/rpi_oled_stats.git rpi_oled_stats
    else
        sudo -u "$USERNAME" git clone https://github.com/4ngel2769/rpi_oled_stats.git rpi_oled_stats >/dev/null 2>&1
    fi
    
    cd rpi_oled_stats
    print_verbose "📁 Changed to directory: $HOME_DIR/rpi_oled_stats"
    
    # Download font files if they don't exist
    if [ ! -f "PixelOperator.ttf" ]; then
        print_status "🔤 Downloading PixelOperator font..."
        print_verbose "📥 Font not found, downloading PixelOperator.ttf..."
        sudo -u "$USERNAME" wget -q "https://github.com/mklements/OLED_Stats/raw/main/PixelOperator.ttf"
    else
        print_verbose "✅ PixelOperator.ttf already exists"
    fi
    
    if [ ! -f "lineawesome-webfont.ttf" ]; then
        print_status "🔤 Downloading LineAwesome font..."
        print_verbose "📥 Font not found, downloading lineawesome-webfont.ttf..."
        sudo -u "$USERNAME" wget -q "https://github.com/mklements/OLED_Stats/raw/main/lineawesome-webfont.ttf"
    else
        print_verbose "✅ lineawesome-webfont.ttf already exists"
    fi
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "📁 Directory contents:"
        ls -la
    fi
    
    print_success "📦 Scripts downloaded"
    
    # Step 6: Detect OLED display
    if ! detect_oled; then
        print_warning "⚠️  OLED display not detected. The script will still create the startup configuration."
        print_warning "🔧 Please check your connections and the display should work after reboot."
    fi
    
    # Step 7: Choose and test the scripts
    print_status "🎮 Selecting OLED display script..."
    
    # Choose which script to run
    echo ""
    echo -e "$(c_primary)╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "$(c_primary)║$(c_secondary)                      📱 SCRIPT SELECTION                       $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)1)${NC} 📝 stats.py - Simple text-based display                     $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)2)${NC} 🎨 monitor.py - Display with icons                          $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)3)${NC} ⚡ psutilstats.py - Enhanced compatibility                  $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} $(c_special)1)${NC} 📝 status.py - Enhanced text-based display                  $(c_primary)║${NC}"
    echo -e "$(c_primary)╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    read -p "🎯 Which script would you like to use as default? (1-3): " SCRIPT_CHOICE < /dev/tty
    
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
        4)
            DEFAULT_SCRIPT="status.py"
            ;;
        *)
            print_warning "⚠️  Invalid choice, using psutilstats.py as default"
            DEFAULT_SCRIPT="psutilstats.py"
            ;;
    esac
    
    print_verbose "🎯 Selected script: $DEFAULT_SCRIPT"
    
    # Test the selected script for 5 seconds if OLED was detected
    if sudo i2cdetect -y 1 | grep -q "3c"; then
        print_status "🧪 Testing $DEFAULT_SCRIPT for 5 seconds..."
        print_verbose "🧪 Running test command: timeout 5 python3 $DEFAULT_SCRIPT"
        
        if [ "$VERBOSE" = true ]; then
            sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && cd $HOME_DIR/rpi_oled_stats && timeout 5 python3 $DEFAULT_SCRIPT || true"
        else
            sudo -u "$USERNAME" bash -c "source $HOME_DIR/stats_env/bin/activate && cd $HOME_DIR/rpi_oled_stats && timeout 5 python3 $DEFAULT_SCRIPT || true" >/dev/null 2>&1
        fi
        print_success "🧪 Script test completed"
    else
        print_status "⏭️  Skipping script test (OLED not detected)"
    fi
    
    # Step 8: Create startup script
    print_status "📝 Creating startup script..."
    print_verbose "📝 Creating startup script at: $HOME_DIR/oled_display_start.sh"
    
    cat > "$HOME_DIR/oled_display_start.sh" << EOF
#!/bin/bash
# OLED Stats Display Startup Script
# Generated by: OLED Stats Installation Script $SCRIPT_VERSION
# Script Author: $SCRIPT_AUTHOR
# Original Code: $ORIGINAL_AUTHOR
# Wait for system to fully boot
sleep 30
source $HOME_DIR/stats_env/bin/activate
cd $HOME_DIR/rpi_oled_stats
python3 $DEFAULT_SCRIPT
EOF
    
    chmod +x "$HOME_DIR/oled_display_start.sh"
    chown "$USERNAME:$USERNAME" "$HOME_DIR/oled_display_start.sh"
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "📝 Startup script contents:"
        cat "$HOME_DIR/oled_display_start.sh"
    fi
    
    print_success "📝 Startup script created"
    
    # Step 9: Setup auto-start
    print_status "⚙️  Setting up auto-start on boot..."
    
    # Add to crontab for the user
    CRON_JOB="@reboot $HOME_DIR/oled_display_start.sh &"
    print_verbose "⏰ Cron job: $CRON_JOB"
    
    # Check if cron job already exists
    if ! sudo -u "$USERNAME" crontab -l 2>/dev/null | grep -q "oled_display_start.sh"; then
        print_verbose "⏰ Adding cron job for auto-start..."
        (sudo -u "$USERNAME" crontab -l 2>/dev/null; echo "$CRON_JOB") | sudo -u "$USERNAME" crontab -
        print_success "⏰ Auto-start configured"
        
        if [ "$VERBOSE" = true ]; then
            print_verbose "⏰ Current crontab for $USERNAME:"
            sudo -u "$USERNAME" crontab -l
        fi
    else
        print_warning "⏰ Auto-start already configured"
    fi
    
    # Step 10: Final instructions
    print_success "🎉 Installation completed successfully!"
    echo ""
    echo -e "$(c_primary)╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "$(c_primary)║$(c_special)                    🎉 INSTALLATION COMPLETE!                   $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║${NC} ✅ Script version: $SCRIPT_VERSION                                        $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ Installation script by: $SCRIPT_AUTHOR              $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ Original OLED Stats code by: $ORIGINAL_AUTHOR           $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ System updated                                              $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ Required packages installed                                 $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ Virtual environment created at: $HOME_DIR/stats_env          $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ Scripts installed at: $HOME_DIR/rpi_oled_stats               $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ Default script set to: $DEFAULT_SCRIPT                           $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} ✅ Auto-start configured with 30-second boot delay             $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║$(c_accent)                      🛠️  MANUAL COMMANDS                       $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} 🚀 Start manually:                                             $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}    $HOME_DIR/oled_display_start.sh                              $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} 🔧 Change script:                                              $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}    Edit $HOME_DIR/oled_display_start.sh                         $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} 🔄 The display will start automatically 30 seconds             $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}    after boot.                                                 $(c_primary)║${NC}"
    echo -e "$(c_primary)╠════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "$(c_primary)║$(c_gold)                            🏆 CREDITS                          $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC}                                                                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} 🛠️  Installation script: $SCRIPT_AUTHOR                $(c_primary)║${NC}"
    echo -e "$(c_primary)║${NC} 🎨 Original OLED Stats: $ORIGINAL_AUTHOR                   $(c_primary)║${NC}"
    echo -e "$(c_primary)╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    if [ "$VERBOSE" = true ]; then
        print_verbose "💻 System information:"
        print_verbose "🐧 Kernel: $(uname -r)"
        print_verbose "🖥️  OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
        print_verbose "🐍 Python version: $(python3 --version)"
        print_verbose "💾 Disk space available: $(df -h $HOME_DIR | tail -1 | awk '{print $4}')"
    fi
    
    read -p "🔄 Would you like to reboot now to start the display? (y/n): " REBOOT_CHOICE < /dev/tty
    
    if [[ $REBOOT_CHOICE =~ ^[Yy]$ ]]; then
        print_status "🔄 Rebooting system..."
        sudo reboot
    else
        print_status "🚀 You can start the display manually with: $HOME_DIR/oled_display_start.sh"
        print_status "🔄 Or reboot to start automatically: sudo reboot"
    fi
}

# Run main function
main "$@"
