import React from "react";
import "./loading.css"; // small css for dots (we'll inline style in styles.css too)

export default function LoadingDots({ text = "Thinking..." }) {
  return (
    <div className="loading-row">
      <div className="dots" aria-hidden />
      <div className="loading-text">{text}</div>
    </div>
  );
}
