import { Menu } from "antd";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <Menu mode="horizontal" theme="dark">
      <Menu.Item key="search">
        <Link to="/">搜索</Link>
      </Menu.Item>
      <Menu.Item key="papers">
        <Link to="/papers">文献列表</Link>
      </Menu.Item>
      <Menu.Item key="scheduler">
        <Link to="/scheduler">定时任务</Link>
      </Menu.Item>
    </Menu>
  );
};

export default NavBar;