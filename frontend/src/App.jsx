// import React, { useState } from "react";
// import axios from "axios";
// import "./App.css";

// function App() {
//   const [selectedFile, setSelectedFile] = useState(null);
//   const [imageURL, setImageURL] = useState("");
//   const [timeInput, setTimeInput] = useState("");
//   const [waterLevel, setWaterLevel] = useState(null);
//   const [loading, setLoading] = useState(false);

//   const handleFileChange = (e) => {
//     setSelectedFile(e.target.files[0]);
//   };

//   const handleUpload = async () => {
//     if (!selectedFile || !timeInput) return;

//     const formData = new FormData();
//     formData.append("file", selectedFile);

//     try {
//       setLoading(true);

//       // Upload ảnh
//       const uploadRes = await axios.post("http://localhost:8000/upload", formData);
//       setImageURL("http://localhost:8000" + uploadRes.data.url);

//       // Dự đoán mực nước
//       const predictForm = new FormData();
//       predictForm.append("time", timeInput);
//       const predictRes = await axios.post("http://localhost:8000/predict", predictForm);

//       setWaterLevel(predictRes.data.prediction);
//       setLoading(false);
//     } catch (err) {
//       console.error("Lỗi khi upload hoặc dự đoán:", err);
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <div className="left-box">
//         <h2>Nhập thông tin & tải ảnh</h2>
//         <input
//           type="date"
//           value={timeInput}
//           onChange={(e) => setTimeInput(e.target.value)}
//         />

//         <input type="file" onChange={handleFileChange} />
//         <button onClick={handleUpload} disabled={loading}>
//           {loading ? "Đang xử lý..." : "Tải ảnh & Dự đoán"}
//         </button>
//       </div>

//       <div className="right-box">
//         {imageURL && <img src={imageURL} alt="Đã tải lên" />}
//         {waterLevel !== null && <p>Mực nước: {waterLevel.toFixed(2)} m</p>}
//       </div>
//     </div>
//   );
// }

// export default App;

import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageURL, setImageURL] = useState("");
  const [timeInput, setTimeInput] = useState("");
  const [waterLevel, setWaterLevel] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    setError("");
    if (!selectedFile || !timeInput) {
      setError("Vui lòng chọn ảnh và nhập thời gian.");
      return;
    }

    try {
      setLoading(true);

      // 1. Upload ảnh
      const formData = new FormData();
      formData.append("file", selectedFile);
      const uploadRes = await axios.post("http://localhost:8000/upload", formData);
      setImageURL("http://localhost:8000" + uploadRes.data.url);
      console.log("URL ảnh được set:", "http://localhost:8000" + uploadRes.data.url);


      // 2. Gửi thời gian để dự đoán
      const predictForm = new FormData();
      predictForm.append("thoi_gian", timeInput); // 🔥 quan trọng: phải đúng tên "thoi_gian"

      const predictRes = await axios.post("http://localhost:8000/predict", predictForm);
      setWaterLevel(predictRes.data.prediction);
    } catch (err) {
      console.error("Lỗi khi upload hoặc dự đoán:", err);
      setError("Đã xảy ra lỗi. Kiểm tra lại định dạng thời gian hoặc dữ liệu.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {/* <div className="header-full">
  <div className="header-left">
    <p>Trung tâm nghiên cứu<br />Trí tuệ nhân tạo quốc tế AIRC</p>
  </div>
</div> */}


      <div className="left-box">
        <h2>📷 Tải ảnh viễn thám và nhập thời điểm</h2>
        <input
          type="date"
          value={timeInput}
          onChange={(e) => setTimeInput(e.target.value)}
        />
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "⏳ Đang xử lý..." : "🚀 Tải ảnh & Dự đoán"}
        </button>
        {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
      </div>

      <div className="right-box">
        {imageURL && <img src={imageURL} alt="Đã tải lên" />}
        {waterLevel !== null && (
          <p>📈 Mực nước dự đoán: <strong>{waterLevel.toFixed(2)} m</strong></p>
        )}
      </div>
    </div>
  );
}

export default App;
