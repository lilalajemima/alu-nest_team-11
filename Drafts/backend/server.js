const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

console.log("MongoDB URI: ", process.env.MONGO_URI);
mongoose.connect(process.env.MONGO_URI)
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.error(err));

app.get("/", (req, res) => {
    res.send("Backend is running");
});

app.get("/housingDB", (req, res) => {
    mongoose.connection.db.listCollections()
        .toArray((err, collections) => {
            if (err) {
                res.status(500).send('Error listing collections');
            } else {
                res.status(200).json(collections);
            }
        });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
