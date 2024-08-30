const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3001;
const FASTAPI_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

// Serve the static files from the React app
app.use(express.static(path.join(__dirname, "../frontend/build")));

// Proxy API requests to the FastAPI backend
app.use(
  "/api",
  createProxyMiddleware({
    target: FASTAPI_BASE_URL,
    changeOrigin: true,
    pathRewrite: {
      "^/api": "",
    },
  })
);

// Handle any other routes with the React app
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/build/index.html"));
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
