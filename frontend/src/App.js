import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
export default function App() {
    return (_jsxs("div", { className: "container layout", children: [_jsx(Sidebar, {}), _jsxs("div", { className: "main", children: [_jsx(Header, {}), _jsx(Dashboard, {})] })] }));
}
