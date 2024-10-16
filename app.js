const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const path = require('path');

const app = express();

// Middleware to handle form data
app.use(bodyParser.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'public')));


// Set the view engine to EJS
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Route to handle form submission
app.post('/', (req, res) => {
    const { air_temp, process_temp, rotational_speed, torque, tool_wear, type } = req.body;

    // Dummy predict function (or replace this with an API call)
    const target = predict(air_temp, process_temp, rotational_speed, torque, tool_wear, type);

    // Render the result on the same page
    res.render('index', { target: target[0], failure: target[1] });
});

// Render the form on GET request
app.get('/', (req, res) => {
    res.render('index', { target: null, failure: null });
});


app.get('/predict', (req, res) => {
    // res.render('predict'); // Ensure you have a 'predict.ejs' or 'predict.html' file
    res.render('predict', { target: null, failure: null });
});

app.get('/chatbot', (req, res) => {
    res.render('chatbot'); // Ensure you have a 'chatbot.ejs' or 'chatbot.html' file
});



