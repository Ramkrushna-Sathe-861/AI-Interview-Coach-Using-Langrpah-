import { jsx as _jsx } from "react/jsx-runtime";
/*
  main.tsx

  Entry point for the frontend React application.

  What this file does (step-by-step):
  1. Imports React and the function to create a root renderer.
  2. Imports the top-level `App` component (defined in src/App.tsx).
  3. Imports global styles.
  4. Finds the <div id="root"> in index.html and mounts the React app there.

  For beginners: React renders UI by attaching itself to a DOM node. All
  components that make up the page are children of `App` and are managed by
  React. Editing `App.tsx` is where you'll usually add new UI.
*/
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles.css';
const container = document.getElementById('root');
const root = createRoot(container);
root.render(_jsx(React.StrictMode, { children: _jsx(App, {}) }));
