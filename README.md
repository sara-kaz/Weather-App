<div align='center'>
   
# Weather App 
![logo](https://img.icons8.com/?size=100&id=3RZmbgKAmbsY&format=png&color=000000)

</div>

A simple weather application developed in Python that allows you to get current weather data, forecast, and view information about the PM Accelerator.

## Features
- Get current weather by city name.
- View a 5-day weather forecast by city name.
- Retrieve weather information by latitude and longitude.
- Convert an address to latitude and longitude for location-based weather.
- Information button providing a description of the PM Accelerator.

## Getting Started

### Step 1: Clone the Repository Locally
1. **Clone the Repository:**
   - Open a terminal or command prompt.
   - Run the following command to clone the repository to your local machine:
     ```bash
     git clone https://github.com/sara-kaz/Weather-App.git
     ```

2. **Navigate to the Repository Folder:**
   - Change into the directory of your repository:
     ```bash
     cd Weather-App
     ```

### Step 2: Set Up Your Python Environment _(optional)_

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:

   - On **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

3. **Install Required Packages:**
   - Ensure Python is installed.
   - Use `pip` to install the necessary libraries:
     ```bash
     pip install requests Flask
     ```

### Step 3: Run the Flask Application

1. **Start the Application:**
   - In your terminal, navigate to the directory where `WeatherApp.py` is located, and run the script:
     ```bash
     python WeatherApp.py
     ```

2. **Access the Application:**
   - Open your web browser and visit `http://127.0.0.1:5000` to view and interact with the app.

### Step 4: Use the Application

1. **Check Current Weather:**
   - Enter a city name in the input field and click "Get Weather" to retrieve the current weather details.

2. **View 5-Day Forecast:**
   - Enter a city name and click "Get Forecast" to view the 5-day weather forecast.

3. **Search by Location:**
   - Enter latitude and longitude coordinates and click "Get Weather by Location" to retrieve the weather data for that location.
   - Use the "Convert Address" button to obtain latitude and longitude from an address.

4. **Learn About PM Accelerator:**
   - Click the "Info" button to view a description of the PM Accelerator program.

### Testing the Application

- Verify that entering a city name returns accurate weather data.
- Check that the 5-day forecast correctly displays for a given city.
- Ensure that searching by latitude and longitude retrieves the correct weather information.
- Test the address conversion feature for obtaining latitude and longitude coordinates.

## <img src="https://media.licdn.com/dms/image/v2/C560BAQERjWEoRZ15Tg/company-logo_200_200/company-logo_200_200/0/1656545579397/productmanagerinterview_logo?e=2147483647&v=beta&t=x54gWmD8-qQcBwCxttUih9FrSCKKpa-Az-0q7URRN80" width="40"/> About the PM Accelerator 

The Product Manager Accelerator Program is designed to support PM professionals through every stage of their career. From students seeking entry-level jobs to Directors aiming for leadership roles, our program has helped hundreds of students achieve their career aspirations. For more details, visit our official website or contact our support team.

<div align='center'>

  [![LinkedIn](https://img.icons8.com/?size=60&id=qNUNvR9aEWql&format=png&color=000000)](https://www.linkedin.com/school/productmanagerinterview/) 
  [![Website](https://img.icons8.com/?size=60&id=VJz2Ob51dvZJ&format=png&color=000000)](https://www.drnancyli.com/) 
  
</div>

---

### Summary of What Was Done

- **Weather Fetching:** Implemented functionality to retrieve current weather data and 5-day forecasts using the OpenWeatherMap API.
- **Search by Coordinates:** Added the ability to search for weather using latitude and longitude coordinates, with address-to-coordinates conversion.
- **PM Accelerator Info:** Integrated a section to display information about the Product Manager Accelerator program.
- **Error Handling:** Included error handling to display appropriate messages if the weather data cannot be retrieved.
- **UI Design:** Created a user-friendly HTML interface with CSS for styling and used FontAwesome for icons.
