import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true, 
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
  //timeout: 5000,
});

export const searchPapers = async (keyword) => {
  console.log(`Requesting: http://127.0.0.1:8000/search?keyword=${encodeURIComponent(keyword)}`);
  return api.get("/search", { params: { keyword } });
};

export const getPapers = async (keyword) => {
  console.log(`Requesting: http://127.0.0.1:8000/papers?keyword=${encodeURIComponent(keyword)}`);
  return api.get("/papers", { params: { keyword } });
};

export const getSchedulerStatus = async () => {
  console.log("Requesting: http://127.0.0.1:8000/scheduler/status");
  return api.get("/scheduler/status");
};