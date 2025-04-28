import { useState, useEffect } from "react";
import { Card, Spin, Alert } from "antd";
import { getSchedulerStatus } from "../api/api";

const SchedulerStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      setLoading(true);
      try {
        const response = await getSchedulerStatus();
        setStatus(response.data);
        setError(null);
      } catch (err) {
        console.error("Fetch scheduler status error:", err);
        setError(
          `获取调度状态失败: ${
            err.response
              ? `HTTP ${err.response.status} - ${err.response.data?.detail || "未知错误"}`
              : err.message
          }`
        );
      } finally {
        setLoading(false);
      }
    };
    fetchStatus();
  }, []);

  return (
    <div className="h-screen w-screen p-6 bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">定时任务状态</h1>
      {loading && <Spin />}
      {error && <Alert message={error} type="error" className="mb-4" />}
      {status ? (
        <Card title="调度状态">
          <p>
            <strong>状态:</strong> {status.status}
          </p>
          <p>
            <strong>详情:</strong>{" "}
            {status.details ? JSON.stringify(status.details, null, 2) : "无"}
          </p>
        </Card>
      ) : (
        !loading && !error && <Alert message="暂无调度状态" type="info" />
      )}
    </div>
  );
};

export default SchedulerStatus;