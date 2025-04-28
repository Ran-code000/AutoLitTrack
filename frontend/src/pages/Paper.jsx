import { useState } from "react";
import { Input, Table, Spin, Alert, Button } from "antd";
import { getPapers } from "../api/api";

const Papers = () => {
  const [keyword, setKeyword] = useState("");
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);


  const fetchPapers = async (kw) => {
    if (!kw || kw.trim().length < 2) {
      setError("请输入至少2个字符的有效关键词");
      setPapers([]);
      return;
    }

    if (!kw) return;
    setLoading(true);

    const timeout = setTimeout(() => {
      setError("请求超时，请检查网络或稍后再试");
      setLoading(false);
      setPapers([]);
    }, 5000);
    
    try {
      const response = await getPapers(kw);
      clearTimeout(timeout);

      if (!response.data || !response.data.papers) {
        throw new Error("服务器返回的数据格式不正确");
      }

      if (response.data.papers.length > 0) {
        setPapers(response.data.papers);
        setError(null);
      } else {
        setPapers([]);
        setError("没有找到相关文献，请尝试其他关键词");
      }
    } catch (err) {
      console.error("Fetch papers error:", err);
      setError(
        `获取文献失败: ${
          err.response
            ? `HTTP ${err.response.status} - ${err.response.data?.detail || "未知错误"}`
            : err.message
        }`
      );
      setPapers([]);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: "标题",
      dataIndex: "title",
      render: (text, record) => <a href={record.link}>{text}</a>,
    },
    { title: "发表时间", dataIndex: "published" },
    {
      title: "关键词",
      dataIndex: "keywords",
      render: (keywords) => (keywords ? keywords.join(", ") : ""),
    },
    {
      title: "摘要",
      dataIndex: "summary",
      render: (text) => (text ? text.slice(0, 100) + "..." : ""),
    },
  ];

  return (
    <div className="h-screen w-screen p-6 bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-gray-800">文献列表</h1>
        <div className="flex gap-4 mb-4">
        <Input
          placeholder="请输入关键词"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onPressEnter={() => fetchPapers(keyword)}
        />
        <Button
          type="primary"
          onClick={() => fetchPapers(keyword)}
          disabled={loading || !keyword}
        >
          搜索
        </Button>
      </div>
      {loading && <Spin />}
      {error && (
          <Alert
            message={error}
            type="error"
            className="mb-4"
            action={
              <Button size="small" onClick={() => fetchPapers(keyword)}>
                重试
              </Button>
            }
          />
        )}
      <Table
        columns={columns}
        dataSource={papers}
        rowKey="title"
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
};

export default Papers;