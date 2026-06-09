import { useState } from 'react';
import { exportStoryboardPdf } from '../services/api';
import './Storyboard.css';

export default function Storyboard({ panels, brief, onBack }) {
  const [exporting, setExporting] = useState(false);

  if (!panels || panels.length === 0) return null;

  const handleExportPDF = async () => {
    if (exporting) return;
    setExporting(true);

    try {
      await exportStoryboardPdf(brief, panels);
    } catch (error) {
      console.error('PDF export failed:', error);
      alert('PDF export failed. Please try again.');
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="storyboard">
      <div className="storyboard__header">
        <button className="storyboard__back" onClick={onBack}>
          ← Back
        </button>
        <div className="storyboard__header-content">
          <div>
            <h2 className="storyboard__title">
              {brief?.title || 'Your Storyboard'}
            </h2>
            <p className="storyboard__subtitle">
              {panels.length} panels • {brief?.format} • {brief?.duration}
            </p>
          </div>
          <button
            className="storyboard__export-btn"
            onClick={handleExportPDF}
            disabled={exporting}
          >
            {exporting ? (
              <>
                <span className="storyboard__spinner" />
                Exporting...
              </>
            ) : (
              <>📄 Export PDF</>
            )}
          </button>
        </div>
      </div>

      <div className="storyboard__content">
        {/* PDF header — visible only in export */}
        <div className="storyboard__pdf-header">
          <h1>{brief?.title || 'Storyboard'}</h1>
          <p>{brief?.format} • {brief?.duration} • {brief?.platform}</p>
        </div>

        <div className="storyboard__grid">
          {panels.map((panel, index) => (
            <div
              key={index}
              className="storyboard__panel"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Image area */}
              <div className="storyboard__panel-image-wrapper">
                {panel.image_base64 ? (
                  <img
                    src={`data:image/jpeg;base64,${panel.image_base64}`}
                    alt={`Shot ${panel.shot_number}: ${panel.visual}`}
                    className="storyboard__panel-image"
                    loading="lazy"
                  />
                ) : (
                  <div className="storyboard__panel-placeholder">
                    <span>🎬</span>
                    <p>{panel.error || 'Image unavailable'}</p>
                  </div>
                )}

                {/* Overlay badges */}
                <div className="storyboard__panel-overlays">
                  <span className="storyboard__panel-shot-num">
                    {panel.shot_number || index + 1}
                  </span>
                  <span className="storyboard__panel-duration">
                    {panel.duration}
                  </span>
                </div>

                {/* Camera angle badge */}
                <div className="storyboard__panel-camera">
                  📷 {panel.camera}
                </div>
              </div>

              {/* Annotations */}
              <div className="storyboard__panel-info">
                <p className="storyboard__panel-visual">{panel.visual}</p>

                {panel.text_overlay && (
                  <div className="storyboard__panel-detail">
                    <span className="storyboard__panel-label">📝 Text</span>
                    <p>{panel.text_overlay}</p>
                  </div>
                )}

                {panel.voiceover && (
                  <div className="storyboard__panel-detail">
                    <span className="storyboard__panel-label">🎙️ VO</span>
                    <p>{panel.voiceover}</p>
                  </div>
                )}

                {panel.transition && panel.transition !== 'Cut' && (
                  <div className="storyboard__panel-transition">
                    → {panel.transition}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom export bar */}
      <div className="storyboard__bottom-bar">
        <div className="storyboard__bottom-info">
          <span>🎬 {panels.length} shots</span>
          <span>•</span>
          <span>📱 {brief?.platform}</span>
          <span>•</span>
          <span>⏱️ {brief?.duration}</span>
        </div>
        <button
          className="storyboard__export-btn storyboard__export-btn--large"
          onClick={handleExportPDF}
          disabled={exporting}
        >
          {exporting ? (
            <>
              <span className="storyboard__spinner" />
              Generating PDF...
            </>
          ) : (
            <>📄 Download PDF Storyboard</>
          )}
        </button>
      </div>
    </div>
  );
}
