const express = require("express");
const mongoose = require("mongoose");
const { GridFSBucket } = require("mongodb");
const cors = require("cors");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// ✅ MongoDB Connection
const mongoURI = "mongodb+srv://aaryasontakke0507:lV1yR2c5ichbdZ7h@cluster0.axpym.mongodb.net/polar_db?retryWrites=true&w=majority&appName=Cluster0";

mongoose
    .connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(async () => {
        console.log("✅ MongoDB connected successfully!");

        // ✅ Test fetching one row from the 'videos' collection
        try {
            const testVideo = await mongoose.connection.db.collection("videos").findOne();
            if (testVideo) {
                console.log("🎥 Sample video metadata found:", testVideo);
            } else {
                console.log("⚠️ No videos found in the database.");
            }
        } catch (fetchError) {
            console.error("❌ Error fetching test video:", fetchError);
        }
    })
    .catch((err) => {
        console.error("❌ MongoDB connection failed:", err);
    });

const conn = mongoose.connection;
let gridfsBucket;

conn.once("open", () => {
    gridfsBucket = new GridFSBucket(conn.db, { bucketName: "fs" });
    console.log("✅ GridFSBucket initialized!");
});

// 🎥 **Stream Video Using GridFS `_id` from `videos.url`**
app.get("/stream/:id", async (req, res) => {
    try {
        const gridfsId = req.params
        console.log(`✅ Extracted GridFS ID: ${gridfsId}`);

        if (!mongoose.Types.ObjectId.isValid(gridfsId)) {
            console.error("🚨 Invalid GridFS ID format:", gridfsId);
            return res.status(400).json({ message: "Invalid GridFS ID format" });
        }

        const gridfsObjectId = new mongoose.Types.ObjectId(gridfsId);
        console.log("✅ GridFS ObjectId:", gridfsObjectId); // ADD THIS LOG
        console.log("✅ GridFSBucket object:", gridfsBucket); // ADD THIS LOG

        // ✅ 2. Find the actual video file in GridFS using `_id`
        const file = await conn.db.collection("fs.files").findOne({ _id: gridfsObjectId }); // Corrected to fs.files
        console.log("✅ GridFS file metadata:", file); // ADD THIS LOG

        if (!file) {
            console.error("🚨 Video not found in GridFS:", gridfsId);
            return res.status(404).json({ message: "Video not found in storage" });
        }

        console.log("✅ Streaming video:", file.filename);
        res.set("Content-Type", "video/mp4");

        // ✅ 3. Stream the video
        console.log("✅ Opening download stream for GridFS ObjectId:", gridfsObjectId); // ADD THIS LOG
        const readStream = gridfsBucket.openDownloadStream(gridfsObjectId);
        console.log("✅ Read stream created:", readStream); // ADD THIS LOG
        readStream.pipe(res);
        console.log("✅ Piping read stream to response."); // ADD THIS LOG


    } catch (err) {
        console.error("❌ Error streaming video:", err); // Keep this, but it's good to have more context now.
        res.status(500).json({ error: err.message });
    }
});

// 🚀 Start Server
const PORT = 5002;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
