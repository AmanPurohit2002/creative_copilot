import './ProgressBar.css';

const STEPS = [
  { number: 1, label: 'Idea', icon: '💡' },
  { number: 2, label: 'Pick Concept', icon: '🎨' },
  { number: 3, label: 'Storyboard', icon: '🖼️' },
];

export default function ProgressBar({ currentStep }) {
  return (
    <div className="progress-bar">
      <div className="progress-bar__inner">
        {STEPS.map((step, index) => (
          <div key={step.number} className="progress-bar__step-wrapper">
            {/* Connector line */}
            {index > 0 && (
              <div
                className={`progress-bar__connector ${
                  currentStep > step.number - 1 ? 'progress-bar__connector--active' : ''
                }`}
              />
            )}

            {/* Step circle */}
            <button
              className={`progress-bar__step ${
                currentStep === step.number
                  ? 'progress-bar__step--active'
                  : currentStep > step.number
                  ? 'progress-bar__step--completed'
                  : 'progress-bar__step--upcoming'
              }`}
              aria-label={`Step ${step.number}: ${step.label}`}
              tabIndex={-1}
            >
              {currentStep > step.number ? (
                <span className="progress-bar__check">✓</span>
              ) : (
                <span className="progress-bar__icon">{step.icon}</span>
              )}
            </button>

            {/* Step label */}
            <span
              className={`progress-bar__label ${
                currentStep >= step.number ? 'progress-bar__label--active' : ''
              }`}
            >
              {step.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
