import { useState } from "react";
import { Input, Button, List, Spin, Alert } from "antd";
import { searchPapers } from "../api/api";

const Search = () => {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!keyword) return;
    setLoading(true);
    console.log("开始搜索，关键词:", keyword); // 添加
    try {
      console.log("准备发送API请求"); // 添加
      const response = await searchPapers(keyword);
      console.log("收到API响应:", response); // 添加
      setResults(response.data.results);
      setError(null);
    } catch (err) {
      console.error("搜索错误详情:", err); // 更详细
      if (err.response) {
        console.error("响应数据:", err.response.data);
        console.error("响应状态:", err.response.status);
        console.error("响应头:", err.response.headers);
      } else if (err.request) {
        console.error("请求已发出但无响应:", err.request);
      }
      setError(
        `搜索失败: ${
          err.response
            ? `HTTP ${err.response.status} - ${err.response.data?.detail || "未知错误"}`
            : err.message
        }`
      );
    } finally {
      console.log("搜索过程结束"); // 添加
      setLoading(false);
    }
  };

  return (
    <div className="h-screen w-screen p-6 bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">文献搜索</h1>
        <div className="flex gap-4 mb-4">
        <Input
          placeholder="请输入关键词"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onPressEnter={handleSearch}
        />
        <Button type="primary" onClick={handleSearch} disabled={loading}>
          搜索
        </Button>
      </div>
      {loading && <Spin tip="搜索中..." />}
      {error && <Alert message={error} type="error" className="mb-4" />}
      <List
        dataSource={results}
        renderItem={(paper) => (
          <List.Item>
            <List.Item.Meta
              title={<a href={paper.link}>{paper.title}</a>}
              description={
                <div>
                  <p>{paper.abstract.slice(0, 200)}...</p>
                  <p>
                    <strong>关键词:</strong> {paper.keywords.join(", ")}
                  </p>
                  <p>
                    <strong>摘要:</strong> {paper.summary}
                  </p>
                </div>
              }
            />
          </List.Item>
        )}
      />
    </div>
  );
};

export default Search;