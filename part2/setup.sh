#!/bin/bash

# Wells Data Visualization Setup Script

echo "=== Wells Data Visualization Setup ==="
echo

# Check if running as root for Apache setup
if [[ $EUID -eq 0 ]]; then
    APACHE_SETUP=true
    WEB_DIR="/var/www/html/wells"
else
    APACHE_SETUP=false
    echo "Note: Not running as root. Will setup for development server only."
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists php; then
    echo "❌ PHP is not installed. Please install PHP first."
    exit 1
fi

if ! command_exists mysql; then
    echo "❌ MySQL is not installed. Please install MySQL first."
    exit 1
fi

if $APACHE_SETUP && ! command_exists apache2; then
    echo "❌ Apache is not installed. Please install Apache first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo

# Setup for Apache (if running as root)
if $APACHE_SETUP; then
    echo "Setting up for Apache web server..."
    
    # Create web directory
    mkdir -p "$WEB_DIR"
    
    # Copy files
    cp -r ./* "$WEB_DIR/"
    
    # Set permissions
    chown -R www-data:www-data "$WEB_DIR"
    chmod -R 755 "$WEB_DIR"
    
    # Enable Apache modules
    echo "Enabling Apache modules..."
    a2enmod rewrite >/dev/null 2>&1
    a2enmod headers >/dev/null 2>&1
    a2enmod deflate >/dev/null 2>&1
    a2enmod expires >/dev/null 2>&1
    
    # Restart Apache
    systemctl restart apache2
    
    echo "✅ Apache setup complete"
    echo "📍 Application available at: http://localhost/wells/"
else
    echo "Setting up for development server..."
    echo "✅ Files are ready for development server"
    echo "📍 Run: php -S localhost:8000"
    echo "📍 Then visit: http://localhost:8000"
fi

echo
echo "=== Setup Instructions ==="
echo "1. Ensure your MySQL database 'wells_db' is created and populated"
echo "2. Update database credentials in api/config.php if needed"
echo "3. Access the application using the URL shown above"
echo
echo "=== Troubleshooting ==="
echo "- If you see database errors, check api/config.php"
echo "- If map doesn't load, check browser console for errors"
echo "- If no markers appear, verify database has coordinate data"
echo
echo "Setup complete! 🎉"