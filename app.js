const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const upload = multer({ dest: "uploads/" });

app.post("/detect", upload.single("image"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No image uploaded" });
  }

  const imagePath = path.join(__dirname, req.file.path);

  const pythonProcess = spawn("python3", ["detect.py", imagePath]);

  let output = "";
  pythonProcess.stdout.on("data", (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error("Python error:", data.toString());
  });

  pythonProcess.on("close", () => {
    fs.unlinkSync(imagePath); // clean up
    try {
      res.json(JSON.parse(output));
    } catch (e) {
      res.status(500).json({ error: "Error processing image" });
    }
  });
});

app.get("/", (req, res) => {
  res.json({ status: "YOLO API running" });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
