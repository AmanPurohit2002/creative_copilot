import './LoadingState.css';

export default function LoadingState({ message = 'Generating...', submessage = '' }) {
  return (
    <div className="loading-state">
      <div className="loading-state__spinner">
        <div className="loading-state__ring" />
        <div className="loading-state__ring loading-state__ring--2" />
        <div className="loading-state__ring loading-state__ring--3" />
      </div>
      <p className="loading-state__message">{message}</p>
      {submessage && <p className="loading-state__submessage">{submessage}</p>}
      <div className="loading-state__dots">
        <span className="loading-state__dot" />
        <span className="loading-state__dot" />
        <span className="loading-state__dot" />
      </div>
    </div>
  );
}

export function SkeletonCard({ lines = 3 }) {
  return (
    <div className="skeleton-card">
      <div className="skeleton-line skeleton-line--title" />
      {Array.from({ length: lines }, (_, i) => (
        <div
          key={i}
          className="skeleton-line"
          style={{ width: `${85 - i * 15}%` }}
        />
      ))}
    </div>
  );
}

export function SkeletonGrid({ count = 3, lines = 3 }) {
  return (
    <div className="skeleton-grid">
      {Array.from({ length: count }, (_, i) => (
        <SkeletonCard key={i} lines={lines} />
      ))}
    </div>
  );
}
