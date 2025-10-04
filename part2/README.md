# Wells Data Visualization Web Application

This web application displays oil and gas well locations on an interactive map with detailed information popups.

## Features

- Interactive map using OpenLayers
- Well locations displayed as colored markers based on status:
  - Green: Active wells
  - Red: Inactive wells
  - Gray: Abandoned/Plugged wells
- Click on markers to view detailed information including:
  - Well information (API number, status, type, location)
  - Production data (oil and gas production)
  - Stimulation data (formation, stages, volume, pressure, etc.)

## Setup Instructions

### Quick Setup

Run the automated setup script:
```bash
cd /home/yutaoye/Desktop/dsci560-lab6/part2
./setup.sh
```

### Prerequisites

1. **Apache Web Server** with PHP support
2. **MySQL Database** with the wells database from Part 1
3. **PHP** with PDO MySQL extension

### Manual Installation Steps

1. **Copy files to web server directory:**
   ```bash
   sudo cp -r /home/yutaoye/Desktop/dsci560-lab6/part2/* /var/www/html/wells/
   ```

2. **Set proper permissions:**
   ```bash
   sudo chown -R www-data:www-data /var/www/html/wells/
   sudo chmod -R 755 /var/www/html/wells/
   ```

3. **Configure database connection:**
   Edit `api/config.php` and update database credentials if needed:
   ```php
   $host = 'localhost';
   $dbname = 'wells_db';
   $username = 'root';
   $password = 'your_password';
   ```

4. **Enable Apache modules:**
   ```bash
   sudo a2enmod rewrite
   sudo a2enmod headers
   sudo a2enmod deflate
   sudo a2enmod expires
   sudo systemctl restart apache2
   ```

5. **Ensure database is populated:**
   Make sure you have run the Part 1 setup to create and populate the database.

### Alternative Setup (Development Server)

For development/testing, you can use PHP's built-in server:

1. **Navigate to the part2 directory:**
   ```bash
   cd /home/yutaoye/Desktop/dsci560-lab6/part2
   ```

2. **Start PHP development server:**
   ```bash
   php -S localhost:8000
   ```

3. **Access the application:**
   Open your browser and go to `http://localhost:8000`

## Usage Instructions

1. **Access the application:**
   - Production: `http://your-server/wells/`
   - Development: `http://localhost:8000`

2. **Navigate the map:**
   - Use mouse to pan and zoom
   - Scroll wheel or touchpad to zoom in/out
   - Click and drag to move around
   - Touchpad gestures supported

3. **View well information:**
   - Click on any colored marker to see detailed information
   - Popup will display well data, production data, and stimulation data
   - Click elsewhere on the map to close the popup

4. **Marker colors indicate well status:**
   - **Green**: Active wells
   - **Red**: Inactive wells
   - **Gray**: Abandoned or plugged wells

## File Structure

```
part2/
├── index.html          # Main HTML page
├── app.js             # JavaScript application logic
├── demo.html          # Demo version with sample data
├── setup.sh           # Automated setup script
├── .htaccess          # Apache configuration
├── api/               # PHP API endpoints
│   ├── config.php     # Database configuration
│   ├── wells.php      # Wells data endpoint
│   └── stimulated.php # Stimulated data endpoint
└── README.md          # This file
```

## API Endpoints

- `GET /api/wells.php` - Returns all wells data
- `GET /api/stimulated.php` - Returns all stimulated data

## Troubleshooting

1. **Map not loading:**
   - Check browser console for JavaScript errors
   - Verify API endpoints are accessible
   - Ensure database connection is working

2. **No markers appearing:**
   - Check if database has data with valid coordinates
   - Verify API endpoints return data (visit directly in browser)

3. **Database connection errors:**
   - Check MySQL service is running
   - Verify database credentials in `api/config.php`
   - Ensure database exists and is populated

4. **CORS errors:**
   - Ensure `.htaccess` file is in place
   - Check Apache has mod_headers enabled

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Mapping**: OpenLayers 8.2.0
- **Backend**: PHP 7.4+
- **Database**: MySQL 8.0+
- **Web Server**: Apache 2.4+