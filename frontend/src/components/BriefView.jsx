import './BriefView.css';

const BRIEF_FIELDS = [
  { key: 'title', label: 'Campaign Title', icon: '🏷️' },
  { key: 'format', label: 'Format', icon: '📐' },
  { key: 'duration', label: 'Duration', icon: '⏱️' },
  { key: 'platform', label: 'Platform', icon: '📱' },
  { key: 'audience', label: 'Target Audience', icon: '👥' },
  { key: 'tone', label: 'Tone & Mood', icon: '🎭' },
  { key: 'product', label: 'Product', icon: '📦' },
  { key: 'goal', label: 'Goal', icon: '🎯' },
  { key: 'cta', label: 'Call to Action', icon: '📣' },
  { key: 'key_message', label: 'Key Message', icon: '💬' },
];

export default function BriefView({ brief, idea, onNext, onBack, isLoading, hideNextButton }) {
  if (!brief) return null;

  return (
    <div className="brief-view">
      <div className="brief-view__header">
        <button className="brief-view__back" onClick={onBack}>
          ← Back
        </button>
        <div>
          <h2 className="brief-view__title">Creative Brief</h2>
          <p className="brief-view__subtitle">
            Generated from: <em>"{idea}"</em>
          </p>
        </div>
      </div>

      <div className="brief-view__grid">
        {BRIEF_FIELDS.map((field) => {
          const value = brief[field.key];
          if (!value) return null;

          return (
            <div
              key={field.key}
              className={`brief-view__card ${
                field.key === 'title' || field.key === 'key_message'
                  ? 'brief-view__card--wide'
                  : ''
              }`}
            >
              <div className="brief-view__card-header">
                <span className="brief-view__card-icon">{field.icon}</span>
                <span className="brief-view__card-label">{field.label}</span>
              </div>
              <p className="brief-view__card-value">{value}</p>
            </div>
          );
        })}
      </div>

      {!hideNextButton && (
        <div className="brief-view__actions">
          <button
            className="brief-view__next-btn"
            onClick={onNext}
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="brief-view__spinner" />
            ) : (
              <>
                Generate Concepts
                <span className="brief-view__arrow">→</span>
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}
