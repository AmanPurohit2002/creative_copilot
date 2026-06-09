import { useState } from 'react';
import './IdeaInput.css';

export default function IdeaInput({ onSubmit, isLoading }) {
  const [idea, setIdea] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (idea.trim() && !isLoading) {
      onSubmit(idea.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const examples = [
    'a 15s Instagram reel for a festive saree sale',
    'a 30s YouTube pre-roll for a fitness app launch',
    'a 60s TVC for a luxury watch brand during Diwali',
    'a 10s Story ad for a new bubble tea shop opening',
  ];

  return (
    <div className="idea-input">
      <div className="idea-input__hero">
        <div className="idea-input__badge">✨ AI-Powered Creative Studio</div>
        <h1 className="idea-input__title">
          Turn your <span className="idea-input__gradient-text">ad idea</span> into
          <br />a complete storyboard
        </h1>
        <p className="idea-input__subtitle">
          Describe your ad in one line — we'll generate a brief, creative concepts,
          shot-by-shot script, and visual storyboard panels.
        </p>
      </div>

      <form className="idea-input__form" onSubmit={handleSubmit}>
        <div className="idea-input__input-wrapper">
          <textarea
            id="idea-textarea"
            className="idea-input__textarea"
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your ad idea in one line..."
            rows={2}
            disabled={isLoading}
            autoFocus
          />
          <button
            type="submit"
            className="idea-input__submit"
            disabled={!idea.trim() || isLoading}
          >
            {isLoading ? (
              <span className="idea-input__spinner" />
            ) : (
              <>
                Generate Brief
                <span className="idea-input__arrow">→</span>
              </>
            )}
          </button>
        </div>
      </form>

      <div className="idea-input__examples">
        <p className="idea-input__examples-label">Try an example:</p>
        <div className="idea-input__examples-list">
          {examples.map((example, i) => (
            <button
              key={i}
              className="idea-input__example-chip"
              onClick={() => setIdea(example)}
              disabled={isLoading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
