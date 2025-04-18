const express = require('express');
const dotenv = require('dotenv');
const app = express();

dotenv.config();

app.use(express.static('.'));

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});