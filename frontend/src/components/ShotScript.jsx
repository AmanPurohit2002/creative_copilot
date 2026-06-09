import './ShotScript.css';

export default function ShotScript({ shots, onNext, onBack, isLoading }) {
  if (!shots || shots.length === 0) return null;

  return (
    <div className="shot-script">
      <div className="shot-script__header">
        <button className="shot-script__back" onClick={onBack}>
          ← Back
        </button>
        <div>
          <h2 className="shot-script__title">Shot-by-Shot Script</h2>
          <p className="shot-script__subtitle">
            {shots.length} shots — Review the script, then generate storyboard panels.
          </p>
        </div>
      </div>

      <div className="shot-script__timeline">
        {shots.map((shot, index) => (
          <div
            key={index}
            className="shot-script__shot"
            style={{ animationDelay: `${index * 0.08}s` }}
          >
            {/* Timeline node */}
            <div className="shot-script__node">
              <div className="shot-script__node-dot" />
              {index < shots.length - 1 && <div className="shot-script__node-line" />}
            </div>

            {/* Shot card */}
            <div className="shot-script__card">
              <div className="shot-script__card-top">
                <span className="shot-script__shot-badge">
                  Shot {shot.shot_number || index + 1}
                </span>
                <span className="shot-script__duration-pill">
                  ⏱️ {shot.duration}
                </span>
                <span className="shot-script__camera-badge">
                  📷 {shot.camera}
                </span>
              </div>

              <p className="shot-script__visual">{shot.visual}</p>

              <div className="shot-script__details">
                {shot.text_overlay && (
                  <div className="shot-script__detail">
                    <span className="shot-script__detail-label">📝 Text Overlay</span>
                    <p>{shot.text_overlay}</p>
                  </div>
                )}
                {shot.voiceover && (
                  <div className="shot-script__detail">
                    <span className="shot-script__detail-label">🎙️ Voiceover</span>
                    <p>{shot.voiceover}</p>
                  </div>
                )}
                {shot.audio && (
                  <div className="shot-script__detail">
                    <span className="shot-script__detail-label">🎵 Audio</span>
                    <p>{shot.audio}</p>
                  </div>
                )}
              </div>

              {shot.transition && shot.transition !== 'Cut' && (
                <div className="shot-script__transition">
                  ↓ {shot.transition}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="shot-script__actions">
        <button
          className="shot-script__next-btn"
          onClick={onNext}
          disabled={isLoading}
        >
          {isLoading ? (
            <span className="shot-script__spinner" />
          ) : (
            <>
              Generate Storyboard
              <span className="shot-script__arrow">→</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
