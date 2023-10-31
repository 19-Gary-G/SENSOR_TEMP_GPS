import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import './Normalize.css';

const WeatherApp = () => {
  const [city, setCity] = useState('Cancun');
  const [temperature, setTemperature] = useState(null);
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetchWeather();
  }, [city]);

  const fetchWeather = async () => {
    const url = https;//es.wttr.in/${city}?format=j1;
    const response = await fetch(url);
    const weatherData = await response.json();

    const temperature = weatherData.current_condition[0].temp_C;
    const description = weatherData.current_condition[0].lang_es[0].value;

    setTemperature(temperature);
    setDescription(description);
  };

  const handleChange = (event) => {
    setCity(event.target.value);
  };

  return (
    <div className='Title'>
      <h1>Weather App</h1>

      <div className='container'>
        <input
          type="text"
          placeholder="Enter a city"
          onChange={handleChange}
          value={city}
        />

        {temperature && description && (
          <p>
            The current temperature in {city} is {temperature} °C. {description}.
          </p>
        )}
      </div>
    </div>
  );
};

ReactDOM.render(<WeatherApp />, document.getElementById('root'));

export default App;