import './ConceptPicker.css';

export default function ConceptPicker({
  concepts,
  selectedConcept,
  onSelect,
  onNext,
  onBack,
  isLoading,
}) {
  if (!concepts || concepts.length === 0) return null;

  const gradients = [
    'linear-gradient(135deg, #f97316, #ec4899)',
    'linear-gradient(135deg, #06b6d4, #3b82f6)',
    'linear-gradient(135deg, #10b981, #8b5cf6)',
  ];

  return (
    <div className="concept-picker">
      <div className="concept-picker__header">
        <button className="concept-picker__back" onClick={onBack}>
          ← Back
        </button>
        <div>
          <h2 className="concept-picker__title">Choose a Creative Direction</h2>
          <p className="concept-picker__subtitle">
            We've generated 3 distinct concepts. Pick the one that resonates most.
          </p>
        </div>
      </div>

      <div className="concept-picker__grid">
        {concepts.map((concept, index) => (
          <div
            key={index}
            className={`concept-picker__card ${
              selectedConcept === index ? 'concept-picker__card--selected' : ''
            }`}
            onClick={() => onSelect(index)}
            style={{ '--card-gradient': gradients[index] }}
          >
            {/* Gradient top bar */}
            <div
              className="concept-picker__card-accent"
              style={{ background: gradients[index] }}
            />

            {/* Selection indicator */}
            <div className="concept-picker__card-check">
              {selectedConcept === index ? '✓' : (index + 1)}
            </div>

            <h3 className="concept-picker__card-title">{concept.title}</h3>

            <div className="concept-picker__card-field">
              <span className="concept-picker__field-label">🎯 Theme</span>
              <p>{concept.theme}</p>
            </div>

            <div className="concept-picker__card-field">
              <span className="concept-picker__field-label">🎨 Visual Style</span>
              <p>{concept.visual_style}</p>
            </div>

            <div className="concept-picker__card-field">
              <span className="concept-picker__field-label">🎵 Music</span>
              <p>{concept.music_mood}</p>
            </div>

            <div className="concept-picker__card-field">
              <span className="concept-picker__field-label">⚡ Hook</span>
              <p>{concept.hook}</p>
            </div>

            <div className="concept-picker__card-field">
              <span className="concept-picker__field-label">📖 Narrative</span>
              <p>{concept.narrative}</p>
            </div>

            <div className="concept-picker__card-palette">
              <span className="concept-picker__field-label">🎨 Palette</span>
              <p>{concept.color_palette}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="concept-picker__actions">
        <button
          className="concept-picker__next-btn"
          onClick={onNext}
          disabled={selectedConcept === null || isLoading}
        >
          {isLoading ? (
            <span className="concept-picker__spinner" />
          ) : (
            <>
              Generate Script
              <span className="concept-picker__arrow">→</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
