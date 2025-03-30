const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const fs = require("fs");

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.post("/write", (req, res) => {
    const { text } = req.body;

    fs.writeFile("user_input.txt", text, (err) => {
        if (err) {
            return res.status(500).json({ message: "Error writing file" });
        }
        res.json({ message: "File saved!" });
    });
});

app.listen(5000, () => console.log("Server running on port 5000"));
