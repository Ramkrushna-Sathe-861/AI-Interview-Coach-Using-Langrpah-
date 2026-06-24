import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
const NAV_ITEMS = [
    { label: 'Dashboard', icon: '🏠' },
    { label: 'Resume Intelligence', icon: '📄' },
    { label: 'Skill Gap Analyzer', icon: '📊' },
    { label: 'Learning Roadmap', icon: '🗺️' },
    { label: 'Mock Interview', icon: '🎙️' },
    { label: 'Feedback Center', icon: '💬' },
    { label: 'Agent Activity', icon: '🤖' },
    { label: 'Analytics & Reports', icon: '📈' },
    { label: 'Settings', icon: '⚙️' },
];
export default function Sidebar() {
    return (_jsxs("aside", { className: "sidebar", children: [_jsxs("div", { className: "sidebar-top", children: [_jsxs("div", { className: "brand", children: [_jsx("span", { className: "brand-mark", children: "IP" }), _jsxs("div", { children: [_jsx("div", { children: "InterviewPilot AI" }), _jsx("div", { className: "brand-subtitle", children: "Your AI Interview Coach" })] })] }), _jsx("ul", { className: "nav", children: NAV_ITEMS.map((item) => (_jsxs("li", { className: `nav-item ${item.label === 'Dashboard' ? 'active' : ''}`, children: [_jsx("span", { className: "nav-icon", children: item.icon }), _jsx("span", { children: item.label })] }, item.label))) })] }), _jsxs("div", { className: "sidebar-footer", children: [_jsxs("div", { className: "promo-card", children: [_jsx("div", { className: "promo-title", children: "Upgrade to Pro" }), _jsx("div", { className: "meta", children: "Unlock unlimited mock interviews, advanced analytics & more." }), _jsx("button", { className: "btn", children: "Upgrade Now \u2192" })] }), _jsxs("div", { className: "user-info", children: [_jsx("div", { className: "avatar", children: "AV" }), _jsxs("div", { children: [_jsx("div", { className: "user-name", children: "Aman Verma" }), _jsx("div", { className: "meta", children: "aman.verma@email.com" })] })] })] })] }));
}
