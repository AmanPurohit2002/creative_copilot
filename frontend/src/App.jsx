import { useState, useCallback } from 'react';
import ProgressBar from './components/ProgressBar';
import IdeaInput from './components/IdeaInput';
import BriefView from './components/BriefView';
import ConceptPicker from './components/ConceptPicker';
import Storyboard from './components/Storyboard';
import LoadingState from './components/LoadingState';
import {
  generateBriefAndConcepts,
  generateScriptAndPanels,
} from './services/api';
import './App.css';

const LOADING_MESSAGES = {
  brief: {
    message: 'Agents are working autonomously...',
    submessage: 'Creative Director → Brainstormer → Reviewer (self-correcting loop)',
  },
  script: {
    message: 'Screenwriter & Storyboard Artist at work...',
    submessage: 'Writing shot-by-shot script and generating image panels',
  },
};

export default function App() {
  // Steps: 1=Idea, 2=Brief+Concepts (pick one), 3=Final Storyboard
  const [currentStep, setCurrentStep] = useState(1);
  const [idea, setIdea] = useState('');
  const [brief, setBrief] = useState(null);
  const [threadId, setThreadId] = useState(null);
  const [concepts, setConcepts] = useState([]);
  const [selectedConcept, setSelectedConcept] = useState(null);
  const [panels, setPanels] = useState([]);
  const [script, setScript] = useState([]);
  const [loadingPhase, setLoadingPhase] = useState(null);
  const [error, setError] = useState(null);

  // Agentic metadata
  const [revisionCount, setRevisionCount] = useState(0);
  const [reviewerReasoning, setReviewerReasoning] = useState('');

  const showError = useCallback((message) => {
    setError(message);
    setTimeout(() => setError(null), 8000);
  }, []);

  // Step 1 → 2: Submit idea, agents run autonomously (brief + brainstorm ↔ review loop)
  const handleIdeaSubmit = async (ideaText) => {
    setIdea(ideaText);
    setLoadingPhase('brief');
    setError(null);
    try {
      const data = await generateBriefAndConcepts(ideaText);
      setBrief(data.brief);
      setThreadId(data.thread_id);
      setConcepts(data.concepts);
      setRevisionCount(data.revision_count);
      setReviewerReasoning(data.reviewer_reasoning);
      setSelectedConcept(null);
      setCurrentStep(2);
    } catch (err) {
      showError(err.message);
    } finally {
      setLoadingPhase(null);
    }
  };

  // Step 2 → 3: Human picks concept, then agents finish autonomously (script + panels)
  const handleConceptSelected = async () => {
    if (selectedConcept === null) return;
    setLoadingPhase('script');
    setError(null);
    try {
      const data = await generateScriptAndPanels(concepts[selectedConcept], threadId);
      setScript(data.shots);
      setPanels(data.panels);
      setCurrentStep(3);
    } catch (err) {
      showError(err.message);
    } finally {
      setLoadingPhase(null);
    }
  };

  const goBack = (step) => {
    setCurrentStep(step);
  };

  return (
    <div className="app">
      <ProgressBar currentStep={currentStep} />

      {/* Error toast */}
      {error && (
        <div className="app__error-toast">
          <span className="app__error-icon">⚠️</span>
          <p>{error}</p>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <main className="app__main">
        {/* Step 1: Idea Input */}
        {currentStep === 1 && (
          loadingPhase === 'brief' ? (
            <LoadingState {...LOADING_MESSAGES.brief} />
          ) : (
            <IdeaInput
              onSubmit={handleIdeaSubmit}
              isLoading={loadingPhase === 'brief'}
            />
          )
        )}

        {/* Step 2: Brief + Concept Picker (human-in-the-loop) */}
        {currentStep === 2 && (
          loadingPhase === 'script' ? (
            <LoadingState {...LOADING_MESSAGES.script} />
          ) : (
            <div className="step-two-container">
              {/* Brief summary */}
              <BriefView
                brief={brief}
                idea={idea}
                onNext={() => {}} // We handle next via concept picker
                onBack={() => goBack(1)}
                isLoading={false}
                hideNextButton={true}
              />

              {/* Agentic activity indicator */}
              {revisionCount > 1 && (
                <div className="agent-activity">
                  <div className="agent-activity__badge">
                    🤖 Agents refined concepts {revisionCount} time{revisionCount > 1 ? 's' : ''}
                  </div>
                  {reviewerReasoning && (
                    <details className="agent-activity__details">
                      <summary>View Reviewer's reasoning</summary>
                      <p>{reviewerReasoning}</p>
                    </details>
                  )}
                </div>
              )}

              {/* Concept picker */}
              <ConceptPicker
                concepts={concepts}
                selectedConcept={selectedConcept}
                onSelect={setSelectedConcept}
                onNext={handleConceptSelected}
                onBack={() => goBack(1)}
                isLoading={loadingPhase === 'script'}
              />
            </div>
          )
        )}

        {/* Step 3: Final Storyboard */}
        {currentStep === 3 && (
          <Storyboard
            panels={panels}
            brief={brief}
            onBack={() => goBack(2)}
          />
        )}
      </main>

      {/* Footer */}
      {currentStep < 3 && (
        <footer className="app__footer">
          <p>
            Powered by <strong>LangGraph</strong> Multi-Agent Architecture + <strong>Groq</strong>
          </p>
        </footer>
      )}
    </div>
  );
}
