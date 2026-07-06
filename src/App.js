import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [quizzes, setQuizzes] = useState([]);
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch('/api/topics')
      .then(res => res.json())
      .then(data => setTopics(data))
      .catch(err => console.error('Error fetching topics:', err));
  }, []);

  const handleFetchQuizzes = () => {
    let url = '/api/quizzes';
    if (selectedTopic) {
      url += `?topic=${selectedTopic}`;
    }
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setQuizzes(data);
        setCurrentQuiz(null); // Clear current quiz when fetching new list
      })
      .catch(err => console.error('Error fetching quizzes:', err));
  };

  const handleViewQuiz = (quizId) => {
    fetch(`/api/quizzes/${quizId}`)
      .then(res => res.json())
      .then(data => setCurrentQuiz(data))
      .catch(err => console.error('Error fetching quiz:', err));
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleSubmitQuiz = () => {
    if (!currentQuiz) return;
    fetch('/api/quizzes/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ quiz_id: currentQuiz.id, answers: answers }),
    })
      .then(res => res.json())
      .then(data => {
        alert('Quiz submitted! Check console for results/explanations.');
        console.log(data); // Display explanations or results
      })
      .catch(err => console.error('Error submitting quiz:', err));
  };

  const handleSearch = () => {
    fetch(`/api/search/quizzes?q=${searchQuery}`)
      .then(res => res.json())
      .then(data => {
        setQuizzes(data);
        setCurrentQuiz(null);
      })
      .catch(err => console.error('Error searching quizzes:', err));
  };

  return (
    <div className="App">
      <h1>Generative AI Quiz Master</h1>

      <div className="section">
        <h2>Topics</h2>
        <select value={selectedTopic} onChange={(e) => setSelectedTopic(e.target.value)}>
          <option value="">All Topics</option>
          {topics.map(topic => (
            <option key={topic} value={topic}>{topic}</option>
          ))}
        </select>
        <button onClick={handleFetchQuizzes}>Load Quizzes</button>
      </div>

      <div className="section">
        <h2>Search Quizzes</h2>
        <input
          type="text"
          placeholder="Enter keywords..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      <div className="section">
        <h2>Available Quizzes</h2>
        {quizzes.length > 0 ? (
          <ul>
            {quizzes.map(quiz => (
              <li key={quiz.id}>
                {quiz.title} ({quiz.topic})
                <button onClick={() => handleViewQuiz(quiz.id)}>View</button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No quizzes found.</p>
        )}
      </div>

      {currentQuiz && (
        <div className="section">
          <h2>{currentQuiz.title}</h2>
          <p>Topic: {currentQuiz.topic}</p>
          {currentQuiz.questions.map(question => (
            <div key={question.id} className="question-block">
              <p>{question.question_text}</p>
              {question.options.map(option => (
                <label key={option}>
                  <input
                    type="radio"
                    name={`question-${question.id}`}
                    value={option}
                    onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  />
                  {option}
                </label>
              ))}
            </div>
          ))}
          <button onClick={handleSubmitQuiz}>Submit Answers</button>
        </div>
      )}
    </div>
  );
}

export default App;
